#!/usr/bin/env python3
"""
Mechanical SQL scanner for one component (or all) of the active kit project.
Tuned for Microsoft SQL Server / T-SQL, but works for most SQL dialects and ORMs.

    python kit/tools/sql_scan.py <component-folder>      # e.g. cash-service
    python kit/tools/sql_scan.py --all

For each component (repo paths from requirements/component-map.md, relative to <TARGET>)
it writes, in requirements/03-capabilities/<folder>/ :
    _sql-scan.json   machine-readable findings (used by sql_inventory.py)
    _sql-scan.md     human-readable findings (input for the curated sql-usage.md)

What it finds
  * SQL in code strings      SELECT/INSERT/UPDATE/DELETE/MERGE/TRUNCATE -> objects + access (C/R/U/D)
  * Stored-procedure calls   EXEC/EXECUTE, CommandType.StoredProcedure, SqlCommand("usp_x"),
                             {call x}, SimpleJdbcCall.withProcedureName, @Procedure, MyBatis CALLABLE
  * ORM usage / mappings     EF [Table]/ToTable/DbSet, JPA @Table/@Entity/Spring Data repositories,
                             Hibernate hbm.xml, Prisma models and prisma.<model>.<op>() calls
  * DDL definitions          CREATE/ALTER TABLE|VIEW|PROC|FUNCTION|TRIGGER|SYNONYM|SEQUENCE|TYPE in .sql,
                             plus the objects each procedure/view/function/trigger references
  * Packages / reports       SQL inside SSIS (.dtsx) and SSRS (.rdl/.rds) XML
  * Databases                Initial Catalog / Database / databaseName from connection strings
                             (server names and credentials are never recorded)
  * Cross-database           3-part [Db].[schema].[Obj] and 4-part [Server].[Db].[schema].[Obj] names
  * Dynamic SQL              sp_executesql / EXEC(@sql) / string-built SQL  -> flagged, Low confidence

The scan is a candidate list: an agent (or person) confirms each finding, adds business purpose,
entry points and rule IDs in sql-usage.md. Standard library only.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

KIT = Path(__file__).resolve().parents[2]

CODE_EXT = {".cs", ".vb", ".java", ".kt", ".scala", ".groovy", ".py", ".js", ".ts", ".tsx", ".jsx", ".go",
            ".php", ".rb", ".cpp", ".c", ".h", ".pas", ".prisma"}
SQL_EXT = {".sql", ".prc", ".tab", ".vw", ".fnc", ".trg", ".udf"}
XML_EXT = {".xml", ".dtsx", ".rdl", ".rds", ".hbm", ".config", ".edmx"}
CONFIG_EXT = {".json", ".config", ".properties", ".yml", ".yaml", ".ini", ".env.example", ".xml"}
SKIP_DIRS = {"node_modules", "bin", "obj", "dist", "build", "target", ".git", "packages", ".vs", ".idea",
             "__pycache__", ".gradle", "out", "coverage", "wwwroot\\lib", "vendor"}
MAX_FILE_BYTES = 3_000_000

IDENT = r"(?:\[[^\]]+\]|\"[^\"]+\"|`[^`]+`|[A-Za-z_#][\w$#@]*)"
QNAME = rf"(?:{IDENT}\s*\.\s*){{0,3}}{IDENT}"
SQL_KEYWORDS = {
    "select", "from", "where", "set", "values", "into", "join", "on", "as", "and", "or", "not", "null", "inner",
    "left", "right", "outer", "cross", "full", "group", "order", "by", "having", "top", "distinct", "case", "when",
    "then", "else", "end", "exists", "in", "is", "like", "between", "union", "all", "with", "nolock", "output",
    "inserted", "deleted", "dual", "table", "openjson", "openquery", "openrowset", "string_split", "unnest",
    "lateral", "apply", "pivot", "unpivot", "default", "begin", "declare", "return", "if", "while", "using",
    "matched", "the", "a", "an", "this", "your", "our", "their", "to", "of", "for",
}
ACCESS_PATTERNS = [
    ("C", re.compile(rf"\bINSERT\s+(?:INTO\s+)?({QNAME})", re.I)),
    ("U", re.compile(rf"\bUPDATE\s+(?:TOP\s*\(\s*\d+\s*\)\s*)?({QNAME})\s+SET\b", re.I)),
    ("D", re.compile(rf"(?<!ON )(?<!ON\t)\bDELETE\s+(?:TOP\s*\(\s*\d+\s*\)\s*)?(?:FROM\s+)?({QNAME})", re.I)),
    ("D", re.compile(rf"\bTRUNCATE\s+TABLE\s+({QNAME})", re.I)),
    ("CU", re.compile(rf"\bMERGE\s+(?:INTO\s+)?({QNAME})", re.I)),
    ("R", re.compile(rf"\bFROM\s+({QNAME})", re.I)),
    ("R", re.compile(rf"\bJOIN\s+({QNAME})", re.I)),
]
SQL_HINT = re.compile(r"\b(SELECT\s.+\sFROM|INSERT\s+INTO|UPDATE\s+\S+\s+SET|DELETE\s+FROM|MERGE\s+INTO|"
                      r"TRUNCATE\s+TABLE|FROM\s+\[?\w+\]?\.\[?\w+|EXEC(?:UTE)?\s+\[?\w)", re.I)
UPPER_SQL = re.compile(r"\b(SELECT|FROM|JOIN|INSERT|UPDATE|DELETE|MERGE|EXEC|EXECUTE|WHERE)\b")

PROC_PATTERNS = [
    re.compile(rf"\bEXEC(?:UTE)?\s+(?:@\w+\s*=\s*)?(?!sp_executesql\b)({QNAME})", re.I),
    re.compile(r"new\s+SqlCommand\s*\(\s*@?\"([\w\.\[\]]+)\"", re.I),
    re.compile(r"\{\s*\??=?\s*call\s+([\w\.\[\]]+)", re.I),
    re.compile(r"withProcedureName\s*\(\s*\"([\w\.]+)\"", re.I),
    re.compile(r"@Procedure\s*\(\s*(?:name\s*=\s*|procedureName\s*=\s*|value\s*=\s*)?\"([\w\.]+)\"", re.I),
    re.compile(r"procedureName\s*=\s*\"([\w\.]+)\"", re.I),
    re.compile(r"StoredProcedure(?:Query)?\s*\(\s*\"([\w\.\[\]]+)\"", re.I),
]
CMDTYPE_SP = re.compile(r"CommandType\s*\.\s*StoredProcedure|commandType\s*:\s*CommandType\.StoredProcedure|"
                        r"statementType\s*=\s*\"CALLABLE\"", re.I)
STRING_NAME = re.compile(r"\"((?:\[?\w+\]?\.)?\[?(?:usp|sp|proc|p)_?\w+\]?)\"", re.I)
DYNAMIC = re.compile(r"\bsp_executesql\b|\bEXEC(?:UTE)?\s*\(\s*@|\bEXEC(?:UTE)?\s*\(\s*'|"
                     r"(?:\"\s*\+\s*\w+\s*\+\s*\"|\$\"[^\"]*\b(?:FROM|WHERE|SELECT)\b[^\"]*\{)", re.I)

ORM_PATTERNS = [
    ("map", re.compile(r"\[Table\s*\(\s*\"([\w\.]+)\"(?:\s*,\s*Schema\s*=\s*\"(\w+)\")?")),
    ("map", re.compile(r"\.ToTable\s*\(\s*\"([\w\.]+)\"(?:\s*,\s*\"(\w+)\")?")),
    ("map", re.compile(r"@Table\s*\(\s*name\s*=\s*\"([\w\.]+)\"(?:.*?schema\s*=\s*\"(\w+)\")?")),
    ("map", re.compile(r"<class\s+[^>]*table\s*=\s*\"([\w\.]+)\"")),
    ("map", re.compile(r"^\s*model\s+(\w+)\s*\{")),               # Prisma
    ("dbset", re.compile(r"DbSet\s*<\s*(\w+)\s*>\s+(\w+)")),     # EF
    ("repo", re.compile(r"interface\s+(\w+)\s+extends\s+(?:Jpa|Crud|PagingAndSorting)Repository\s*<\s*(\w+)")),
]
PRISMA_CALL = re.compile(r"\b(?:prisma|tx|db|client)\.(\w+)\.(findMany|findUnique|findFirst|findUniqueOrThrow|"
                         r"findFirstOrThrow|count|aggregate|groupBy|create|createMany|update|updateMany|upsert|"
                         r"delete|deleteMany)\b")
PRISMA_ACCESS = {"findMany": "R", "findUnique": "R", "findFirst": "R", "findUniqueOrThrow": "R",
                 "findFirstOrThrow": "R", "count": "R", "aggregate": "R", "groupBy": "R", "create": "C",
                 "createMany": "C", "update": "U", "updateMany": "U", "upsert": "CU", "delete": "D", "deleteMany": "D"}
EF_CALL = re.compile(r"\b(?:_?context|_?db|_?dbContext|_?ctx)\.(\w+)\s*\.\s*(Where|First\w*|Single\w*|Any|Count|"
                     r"ToList\w*|Find\w*|Include|Select|Add\w*|Remove\w*|Update\w*|AsNoTracking|OrderBy\w*)\b")
EF_ACCESS = lambda op: "C" if op.startswith("Add") else "D" if op.startswith("Remove") else \
    "U" if op.startswith("Update") else "R"
REPO_CALL = re.compile(r"\b(\w+Repository|\w+Repo)\s*\.\s*(save\w*|find\w*|get\w*|delete\w*|remove\w*|exists\w*|count\w*)\s*\(")
REPO_ACCESS = lambda op: "CU" if op.startswith("save") else "D" if op.startswith(("delete", "remove")) else "R"

DDL = re.compile(rf"\b(CREATE|ALTER|CREATE\s+OR\s+ALTER)\s+(TABLE|VIEW|PROC(?:EDURE)?|FUNCTION|TRIGGER|SYNONYM|"
                 rf"SEQUENCE|TYPE|INDEX)\s+({QNAME})", re.I)
CTE = re.compile(r"(?:\bWITH|,)\s*([A-Za-z_]\w*)\s+AS\s*\(", re.I)
CONN_DB = re.compile(r"(?:Initial\s+Catalog|Database|databaseName)\s*=\s*([^;\"'\s<>]+)", re.I)
CONN_KEY = re.compile(r"\"(\w*(?:Conn|Connection|Db|Database)\w*)\"\s*:", re.I)


def norm_name(raw: str) -> tuple[str, list[str]]:
    parts = [p.strip().strip("[]\"`") for p in re.split(r"\s*\.\s*", raw.strip())]
    parts = [p for p in parts if p]
    return ".".join(parts), parts


def classify_parts(parts):
    # returns (server, database, schema, object)
    p = list(parts)
    while len(p) < 4:
        p.insert(0, "")
    return p[-4], p[-3], p[-2], p[-1]


def is_noise(name: str, ctes: set) -> bool:
    last = name.split(".")[-1]
    low = last.lower()
    return (not last or low in SQL_KEYWORDS or low in ctes or last.startswith("@") or last[0].isdigit()
            or len(last) < 2 or "(" in last or "'" in last or "{" in last or "$" == last[:1]
            or "+" in name or " " in last or "\"" in name)


# --------------------------------------------------------------------------- project helpers

def active_project():
    name = (KIT / "projects" / ".active").read_text(encoding="utf-8").strip()
    pdir = KIT / "projects" / name
    pm = (pdir / "project.md").read_text(encoding="utf-8")
    m = re.search(r"^\|\s*Target repo\s*\|\s*(.+?)\s*\|", pm, re.M)
    if not m:
        sys.exit("Target repo not found in project.md")
    return name, pdir, Path(m.group(1).strip())


def component_rows(pdir: Path) -> dict:
    cm = (pdir / "requirements" / "component-map.md").read_text(encoding="utf-8")
    rows = {}
    for line in cm.splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 5 or cells[0] in ("Component", "") or set(cells[0]) <= {"-"}:
            continue
        paths = re.findall(r"`([^`]+)`", cells[2])
        folder = cells[3].strip("` ")
        if paths and folder and folder not in ("—", "-", "TBD"):
            rows.setdefault(folder, {"component": cells[0], "type": cells[1], "paths": [], "prefix": cells[4]})
            rows[folder]["paths"] += [p.split(" (")[0] for p in paths]
    return rows


# --------------------------------------------------------------------------- scanning

def iter_files(target: Path, rel_paths: list[str]):
    seen = set()
    for rel in rel_paths:
        base = (target / rel).resolve()
        if base.is_file():
            candidates = [base]
        elif base.is_dir():
            candidates = base.rglob("*")
        else:
            print(f"  ! path not found in target: {rel}", file=sys.stderr)
            continue
        for f in candidates:
            if f in seen or not f.is_file():
                continue
            # skip build/dependency folders *inside* the component, never the path leading to it
            inner = f.relative_to(base).parts[:-1] if base.is_dir() else ()
            if any(part in SKIP_DIRS for part in inner):
                continue
            ext = f.suffix.lower()
            if ext in CODE_EXT | SQL_EXT | XML_EXT | CONFIG_EXT and f.stat().st_size <= MAX_FILE_BYTES \
                    and not f.name.endswith((".min.js", ".map")) and not f.name.startswith("_sql-scan"):
                seen.add(f)
                yield f


DEFAULT_SCHEMA = "dbo"   # MS SQL default; set via project.md "SQL default schema" or --default-schema
SQL_START = re.compile(r"(?:@?\"|'|`|\"\"\")\s*(SELECT|INSERT|UPDATE|DELETE|MERGE|WITH|EXEC|EXECUTE|TRUNCATE)\b", re.I)
SQL_CONT = re.compile(r"\b(FROM|JOIN|INTO|UPDATE|DELETE|MERGE|SELECT|EXEC|EXECUTE|WHERE|SET|VALUES)\b", re.I)
STRING_END = re.compile(r"[\"'`]\s*[;),]\s*(?://.*)?$|\"\"\"\s*[;)]?\s*$")
CLASS_NAME = re.compile(r"\bclass\s+(\w+)")


def qualify(srv, db, sch, obj, temp=False):
    if not sch and DEFAULT_SCHEMA and not temp:
        sch = DEFAULT_SCHEMA
    return ".".join(p for p in (sch, obj) if p), ".".join(p for p in (srv, db, sch, obj) if p)


def scan_component(target: Path, rel_paths: list[str]) -> dict:
    findings = {"usages": [], "procs": [], "orm_maps": [], "definitions": [], "databases": [],
                "dynamic": [], "cross_db": []}
    target = Path(target).resolve()  # normalise 8.3 short names, mapped drives, symlinks
    for f in iter_files(target, rel_paths):
        rel = f.relative_to(target).as_posix()
        try:
            text = f.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        ext = f.suffix.lower()
        is_sql = ext in SQL_EXT
        is_test = bool(re.search(r"(^|/)(tests?|spec|__tests__|\w+\.tests?)(/|$)", rel, re.I))
        lines = text.splitlines()
        ctes = {m.group(1).lower() for m in CTE.finditer(text)} if (is_sql or "WITH" in text.upper()) else set()
        current_def = None  # object being defined in a .sql file

        # connection strings (database names only)
        if ext in CONFIG_EXT or ext in CODE_EXT:
            for i, line in enumerate(lines, 1):
                for m in CONN_DB.finditer(line):
                    db = m.group(1).strip()
                    if db and not db.startswith(("$", "{", "%")):
                        keys = list(CONN_KEY.finditer(line[:m.start()]))  # nearest key before the value
                        findings["databases"].append({"database": db, "key": keys[-1].group(1) if keys else "",
                                                      "source": f"{rel}:{i}"})

        sql_window = 0          # lines remaining in a multi-line SQL string
        recent_procs: dict[str, int] = {}
        for i, line in enumerate(lines, 1):
            src = f"{rel}:{i}"
            stripped = line.strip()
            if not stripped or stripped.startswith(("//", "--", "#", "*", "/*")) and not is_sql:
                continue
            if is_sql and stripped.startswith("--"):
                continue

            # DDL definitions
            if is_sql:
                for m in DDL.finditer(line):
                    kind = m.group(2).upper().replace("PROCEDURE", "PROC")
                    name, parts = norm_name(m.group(3))
                    if kind == "INDEX" or is_noise(name, set()):
                        continue
                    srv, db, sch, obj = classify_parts(parts)
                    current_def = {"object": qualify(srv, db, sch, obj)[0], "type": kind,
                                   "source": src, "references": defaultdict(set)}
                    findings["definitions"].append(current_def)

            started = bool(SQL_START.search(line)) and not is_sql
            if started:
                sql_window = 40
            in_block = sql_window > 0 and SQL_CONT.search(line)
            sqlish = is_sql or ext in {".dtsx", ".rdl", ".rds", ".xml", ".hbm"} or bool(in_block) or \
                (SQL_HINT.search(line) and UPPER_SQL.search(line) and re.search(r"[\"'`]|@\"|\"\"\"|<\w", line))
            if sql_window:
                sql_window = 0 if STRING_END.search(line) else sql_window - 1

            # stored procedure calls
            proc_names = []
            for pat in PROC_PATTERNS:
                for m in pat.finditer(line):
                    if pat is PROC_PATTERNS[0] and not sqlish:
                        continue
                    proc_names.append(m.group(1))
            if CMDTYPE_SP.search(line):
                window = "\n".join(lines[max(0, i - 6):i + 3])
                for m in STRING_NAME.finditer(window):
                    proc_names.append(m.group(1))
            for raw in proc_names:
                name, parts = norm_name(raw)
                if is_noise(name, ctes) or name.lower() in ("sp_executesql",):
                    continue
                srv, db, sch, obj = classify_parts(parts)
                short, full = qualify(srv, db, sch, obj)
                if i - recent_procs.get(full.lower(), -99) <= 8:
                    continue  # same call already recorded a few lines above (e.g. SqlCommand + CommandType)
                recent_procs[full.lower()] = i
                entry = {"object": short, "database": db, "server": srv, "source": src, "test": is_test}
                if current_def is not None and is_sql:
                    current_def["references"]["X"].add(full)  # EXEC inside a procedure: a dependency, not a call
                else:
                    findings["procs"].append(entry)
                if db:
                    findings["cross_db"].append({"object": short, "database": db, "server": srv, "source": src})

            # dynamic SQL
            if DYNAMIC.search(line) and (sqlish or "sp_executesql" in line.lower()):
                findings["dynamic"].append({"source": src, "excerpt": stripped[:140]})

            # table/view access in SQL text
            if sqlish:
                for acc, pat in ACCESS_PATTERNS:
                    for m in pat.finditer(line):
                        name, parts = norm_name(m.group(1))
                        if is_noise(name, ctes) or name.split(".")[-1].upper() in {"SELECT"}:
                            continue
                        srv, db, sch, obj = classify_parts(parts)
                        temp = obj.startswith("#")
                        short, full = qualify(srv, db, sch, obj, temp)
                        u = {"object": short, "database": db, "server": srv,
                             "access": acc, "via": "SQL in .sql file" if is_sql else "SQL in code",
                             "source": src, "test": is_test, "temp": temp}
                        if db:
                            findings["cross_db"].append({"object": short, "database": db, "server": srv,
                                                         "source": src})
                        if current_def is not None and is_sql:
                            if not temp:
                                current_def["references"][acc].add(full)
                            continue  # inside a definition: a dependency of that object, not a component usage
                        findings["usages"].append(u)

            # ORM mappings
            for kind, pat in ORM_PATTERNS:
                for m in pat.finditer(line):
                    if kind == "map":
                        tbl = m.group(1)
                        schema = m.group(2) if m.lastindex and m.lastindex >= 2 else ""
                        entity = ""
                        if "model" in pat.pattern:
                            entity = tbl
                        else:  # entity class: EF fluent Entity<T>() on the same line, or the next class declaration
                            em = re.search(r"Entity\s*<\s*(\w+)\s*>", line[:m.start()])
                            if em:
                                entity = em.group(1)
                            else:
                                for nxt in lines[i - 1:i + 4]:
                                    cm = CLASS_NAME.search(nxt)
                                    if cm:
                                        entity = cm.group(1); break
                        findings["orm_maps"].append({"entity": entity, "table": tbl, "schema": schema or "",
                                                     "kind": "prisma model" if "model" in pat.pattern else "mapping",
                                                     "source": src})
                    elif kind == "dbset":
                        findings["orm_maps"].append({"entity": m.group(1), "table": m.group(2), "schema": "",
                                                     "kind": "EF DbSet", "source": src})
                    elif kind == "repo":
                        findings["orm_maps"].append({"entity": m.group(2), "table": "", "schema": "",
                                                     "kind": f"repository {m.group(1)}", "source": src})

            # ORM calls
            for m in PRISMA_CALL.finditer(line):
                findings["usages"].append({"object": m.group(1)[0].upper() + m.group(1)[1:], "database": "",
                                           "server": "", "access": PRISMA_ACCESS[m.group(2)],
                                           "via": f"ORM .{m.group(2)}()", "source": src, "test": is_test,
                                           "temp": False})
            for m in EF_CALL.finditer(line):
                findings["usages"].append({"object": m.group(1), "database": "", "server": "",
                                           "access": EF_ACCESS(m.group(2)), "via": f"EF .{m.group(2)}",
                                           "source": src, "test": is_test, "temp": False})
            for m in REPO_CALL.finditer(line):
                findings["usages"].append({"object": m.group(1), "database": "", "server": "",
                                           "access": REPO_ACCESS(m.group(2)), "via": f"repository .{m.group(2)}()",
                                           "source": src, "test": is_test, "temp": False})

    for d in findings["definitions"]:
        d["references"] = {k: sorted(v) for k, v in d["references"].items()}
    return findings


# --------------------------------------------------------------------------- output

def orm_resolver(orm_maps: list[dict]):
    """Map ORM names (EF DbSet property, Spring Data repository variable, Prisma model) to real tables."""
    entity_table, dbset_entity, repo_entity = {}, {}, {}
    for m in orm_maps:
        if m["kind"] in ("mapping", "prisma model") and m["entity"]:
            entity_table[m["entity"].lower()] = qualify("", "", m["schema"], m["table"].split(".")[-1])[0] \
                if m["kind"] == "mapping" else m["table"]
        elif m["kind"] == "EF DbSet":
            dbset_entity[m["table"].lower()] = m["entity"]
        elif m["kind"].startswith("repository "):
            repo_entity[m["kind"].split(" ", 1)[1].lower()] = m["entity"]

    def resolve(u: dict) -> tuple[str, bool]:
        name, via = u["object"], u["via"]
        ent = None
        if via.startswith("EF"):
            ent = dbset_entity.get(name.lower())
        elif via.startswith("repository"):
            ent = repo_entity.get(name.lower())
        elif via.startswith("ORM"):
            ent = name
        if ent and ent.lower() in entity_table:
            return entity_table[ent.lower()], True
        if via.startswith("EF") and ent:  # EF convention: table = DbSet property name
            return qualify("", "", "", name)[0], True
        return name, False
    return resolve


def summarise(f: dict) -> dict:
    resolve = orm_resolver(f["orm_maps"])
    objs = defaultdict(lambda: {"access": set(), "via": set(), "sources": [], "database": "", "test_only": True})
    for u in f["usages"]:
        if u.get("temp"):
            continue
        if not u["via"].startswith("SQL"):
            resolved, ok = resolve(u)
            u = dict(u, object=resolved, via=u["via"].split(" .")[0] + (" (resolved)" if ok else " (unresolved name)"))
        key = (u["database"].lower(), u["object"].lower())
        o = objs[key]
        o["name"], o["database"] = u["object"], u["database"]
        o["access"].update(u["access"])
        o["via"].add(u["via"])
        o["sources"].append(u["source"])
        o["test_only"] &= u["test"]
    procs = defaultdict(lambda: {"sources": [], "database": ""})
    for p in f["procs"]:
        key = (p["database"].lower(), p["object"].lower())
        procs[key]["name"], procs[key]["database"] = p["object"], p["database"]
        procs[key]["sources"].append(p["source"])
    return {"objects": objs, "procs": procs}


def write_outputs(folder_dir: Path, comp: dict, f: dict, commit: str):
    folder_dir.mkdir(parents=True, exist_ok=True)
    s = summarise(f)
    data = {"component": comp["component"], "paths": comp["paths"], "commit": commit,
            "objects": [{"object": o["name"], "database": o["database"], "access": "".join(sorted(o["access"])),
                         "via": sorted(o["via"]), "count": len(o["sources"]), "sources": o["sources"][:50],
                         "test_only": o["test_only"]} for o in s["objects"].values()],
            "procedures_called": [{"object": p["name"], "database": p["database"], "count": len(p["sources"]),
                                   "sources": p["sources"][:50]} for p in s["procs"].values()],
            "definitions": f["definitions"], "orm_maps": f["orm_maps"],
            "databases": f["databases"], "dynamic_sql": f["dynamic"], "cross_db": f["cross_db"]}
    (folder_dir / "_sql-scan.json").write_text(json.dumps(data, indent=1), encoding="utf-8")

    def tbl(header, rows):
        out = ["| " + " | ".join(header) + " |", "|" + "---|" * len(header)]
        out += ["| " + " | ".join(str(c).replace("|", "\\|") for c in r) + " |" for r in rows]
        return "\n".join(out) if rows else "_None found._"

    md = [f"# SQL scan — {comp['component']}", "",
          "> **Generated by `kit/tools/sql_scan.py`. Do not edit.** Mechanical candidate list; confirm each item "
          "and add purpose, entry points and rules in `sql-usage.md`.", "",
          f"**Paths scanned:** {', '.join('`' + p + '`' for p in comp['paths'])} · **Commit:** `{commit[:7] or 'n/a'}`", "",
          "## Objects accessed", "",
          tbl(["Object", "Database", "Access", "Via", "Hits", "First sources", "Test only"],
              [[f"`{o['object']}`", o["database"] or "—", o["access"], ", ".join(o["via"]), o["count"],
                "<br>".join(f"`{x}`" for x in o["sources"][:3]), "yes" if o["test_only"] else ""]
               for o in sorted(data["objects"], key=lambda x: x["object"].lower())]), "",
          "## Stored procedures called", "",
          tbl(["Procedure", "Database", "Hits", "First sources"],
              [[f"`{p['object']}`", p["database"] or "—", p["count"], "<br>".join(f"`{x}`" for x in p["sources"][:3])]
               for p in sorted(data["procedures_called"], key=lambda x: x["object"].lower())]), "",
          "## Objects defined here (DDL)", "",
          tbl(["Object", "Type", "Reads", "Writes", "Executes", "Source"],
              [[f"`{d['object']}`", d["type"], ", ".join(d["references"].get("R", [])),
                ", ".join(sorted(set(d["references"].get("C", [])) | set(d["references"].get("U", []))
                                 | set(d["references"].get("D", [])) | set(d["references"].get("CU", [])))),
                ", ".join(d["references"].get("X", [])), f"`{d['source']}`"] for d in data["definitions"]]), "",
          "## ORM mappings", "",
          tbl(["Entity", "Table", "Schema", "Kind", "Source"],
              [[m["entity"] or "—", m["table"] or "—", m["schema"] or "—", m["kind"], f"`{m['source']}`"]
               for m in data["orm_maps"]]), "",
          "## Databases referenced (connection strings)", "",
          tbl(["Database", "Config key", "Source"],
              [[d["database"], d["key"] or "—", f"`{d['source']}`"] for d in data["databases"]]), "",
          "## Cross-database / linked-server references", "",
          tbl(["Object", "Database", "Linked server", "Source"],
              [[f"`{c['object']}`", c["database"], c["server"] or "—", f"`{c['source']}`"] for c in data["cross_db"]]), "",
          "## Dynamic SQL (review manually — objects may be missing above)", "",
          tbl(["Source", "Excerpt"], [[f"`{d['source']}`", f"`{d['excerpt']}`"] for d in data["dynamic_sql"]]), ""]
    (folder_dir / "_sql-scan.md").write_text("\n".join(md), encoding="utf-8")
    return data


def main(argv=None):
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(errors="replace")
        except (AttributeError, ValueError):
            pass
    ap = argparse.ArgumentParser(description="Mechanical SQL scanner for kit components.")
    ap.add_argument("component", nargs="?", help="component folder from component-map.md")
    ap.add_argument("--all", action="store_true", help="scan every component in the component map")
    ap.add_argument("--dir", help="ad-hoc: scan this folder (no project needed); writes to --out")
    ap.add_argument("--out", help="ad-hoc output folder (default: current folder)")
    ap.add_argument("--default-schema", help="schema assumed for unqualified names (MS SQL: dbo; '' = none)")
    a = ap.parse_args(argv)
    global DEFAULT_SCHEMA
    if a.default_schema is not None:
        DEFAULT_SCHEMA = a.default_schema
    elif not a.dir:
        try:
            pm = (KIT / "projects" / (KIT / "projects" / ".active").read_text(encoding="utf-8").strip()
                  / "project.md").read_text(encoding="utf-8")
            m = re.search(r"^\|\s*SQL default schema\s*\|\s*([^|]*?)\s*\|", pm, re.M)
            if m:
                DEFAULT_SCHEMA = "" if m.group(1).lower() in ("", "(none)", "none", "-") else m.group(1)
        except OSError:
            pass
    if a.dir:
        d = Path(a.dir).resolve()
        f = scan_component(d, ["."])
        data = write_outputs(Path(a.out or ".").resolve(), {"component": d.name, "paths": [str(d)]}, f, "")
        print(f"objects={len(data['objects'])} procs={len(data['procedures_called'])} "
              f"defined={len(data['definitions'])} orm-maps={len(data['orm_maps'])} "
              f"dbs={len({x['database'] for x in data['databases']})} dynamic={len(data['dynamic_sql'])} "
              f"cross-db={len(data['cross_db'])}")
        return 0
    name, pdir, target = active_project()
    if not target.exists():
        sys.exit(f"Target repo not readable: {target}")
    rows = component_rows(pdir)
    pm = (pdir / "project.md").read_text(encoding="utf-8")
    cm = re.search(r"^\|\s*Commit analysed\s*\|\s*(\w+)", pm, re.M)
    commit = cm.group(1) if cm else ""
    todo = list(rows) if a.all else [a.component]
    if not a.all and a.component not in rows:
        sys.exit(f"Component folder '{a.component}' not in component-map.md. Known: {', '.join(rows)}")
    for folder in todo:
        comp = rows[folder]
        f = scan_component(target, comp["paths"])
        data = write_outputs(pdir / "requirements" / "03-capabilities" / folder, comp, f, commit)
        print(f"{folder:22} objects={len(data['objects']):3}  procs={len(data['procedures_called']):3}  "
              f"defined={len(data['definitions']):3}  orm-maps={len(data['orm_maps']):3}  "
              f"dbs={len({d['database'] for d in data['databases']}):2}  dynamic={len(data['dynamic_sql']):3}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
