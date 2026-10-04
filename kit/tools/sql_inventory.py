#!/usr/bin/env python3
"""
Build the system-wide SQL inventory for the active kit project.

    python kit/tools/sql_inventory.py

Inputs   requirements/03-capabilities/*/_sql-scan.json   (facts, from sql_scan.py)
         requirements/03-capabilities/*/sql-usage.md     (optional review: purpose, rules, Status)
Outputs  requirements/00-overview/sql-inventory.md       (generated — do not edit)
         requirements/00-overview/sql-inventory.csv      (one row per component × object, for Excel)

Sections: summary · databases · object catalogue · usage matrix (direct + via stored procedures) ·
tables written by several components · stored procedures · defined-but-unused · used-but-undefined ·
cross-database / linked-server · dynamic SQL · review status.
Standard library only.
"""
from __future__ import annotations

import csv
import datetime as dt
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

KIT = Path(__file__).resolve().parents[2]


def md_table_rows(text: str, heading: str) -> list[dict]:
    """Rows of the first markdown table under '## <heading>' as dicts keyed by header."""
    m = re.search(rf"^##\s+{re.escape(heading)}.*?$(.*?)(?=^##\s|\Z)", text, re.M | re.S)
    if not m:
        return []
    lines = [l.strip() for l in m.group(1).splitlines() if l.strip().startswith("|")]
    if len(lines) < 2:
        return []
    split = lambda l: [c.strip() for c in re.split(r"(?<!\\)\|", l.strip().strip("|"))]
    header = split(lines[0])
    rows = []
    for l in lines[2:]:
        cells = split(l)
        rows.append({header[i]: (cells[i] if i < len(cells) else "") for i in range(len(header))})
    return rows


def key(name: str) -> str:
    return name.strip("` ").lower()


def main():
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(errors="replace")
        except (AttributeError, ValueError):
            pass
    name = (KIT / "projects" / ".active").read_text(encoding="utf-8").strip()
    req = KIT / "projects" / name / "requirements"
    cap = req / "03-capabilities"
    comps = []
    for d in sorted(p for p in cap.iterdir() if p.is_dir()):
        scan = d / "_sql-scan.json"
        if not scan.exists():
            continue
        data = json.loads(scan.read_text(encoding="utf-8"))
        review = (d / "sql-usage.md").read_text(encoding="utf-8") if (d / "sql-usage.md").exists() else ""
        comps.append((d.name, data, review))
    if not comps:
        sys.exit("No _sql-scan.json found. Run: python kit/tools/sql_scan.py --all")

    # Global ORM resolver (DbContext / repositories may live in a shared library)
    entity_table, dbset_entity, repo_entity = {}, {}, {}
    for _, data, _ in comps:
        for m in data.get("orm_maps", []):
            if m["kind"] in ("mapping", "prisma model") and m["entity"]:
                entity_table[m["entity"].lower()] = (f"{m['schema']}.{m['table']}" if m["schema"] else m["table"])
            elif m["kind"] == "EF DbSet":
                dbset_entity[m["table"].lower()] = m["entity"]
            elif m["kind"].startswith("repository "):
                repo_entity[m["kind"].split(" ", 1)[1].lower()] = m["entity"]

    def resolve(obj: str, via: list[str]) -> str:
        if not any("unresolved" in v for v in via):
            return obj
        ent = dbset_entity.get(obj.lower()) or repo_entity.get(obj.lower()) or obj
        return entity_table.get(ent.lower(), obj)

    defs = {}                     # object key -> definition
    usage = defaultdict(dict)     # object key -> {component: {"access", "via", "purpose", "status", "db"}}
    proc_calls = defaultdict(dict)
    display = {}
    databases = defaultdict(set)
    cross, dynamic = [], defaultdict(list)
    review_stats = defaultdict(lambda: {"confirmed": 0, "false": 0, "unreviewed": 0})

    for comp, data, review in comps:
        rv_obj = {key(r.get("Object", "")): r for r in md_table_rows(review, "Tables and views accessed")}
        rv_proc = {key(r.get("Procedure", "")): r for r in md_table_rows(review, "Stored procedures and functions called")}
        for d in data.get("definitions", []):
            k = key(d["object"]); defs[k] = dict(d, component=comp); display.setdefault(k, d["object"])
            for objs in d.get("references", {}).values():
                for o in objs:
                    display.setdefault(key(o), o)  # keep original casing for objects reached via procedures
        for o in data.get("objects", []):
            obj = resolve(o["object"], o["via"])
            k = key(obj)
            r = rv_obj.get(k) or rv_obj.get(key(o["object"])) or {}
            status = (r.get("Status") or "").lower()
            if status.startswith("false"):
                review_stats[comp]["false"] += 1
                continue
            review_stats[comp]["confirmed" if status.startswith("confirm") else "unreviewed"] += 1
            display.setdefault(k, obj)
            cur = usage[k].setdefault(comp, {"access": set(), "via": set(), "purpose": "", "status": "", "db": ""})
            cur["access"].update(o["access"]); cur["via"].update(o["via"])
            cur["purpose"] = cur["purpose"] or r.get("Business purpose", "")
            cur["status"] = "Confirmed" if status.startswith("confirm") else (cur["status"] or "Unreviewed")
            cur["db"] = cur["db"] or o.get("database", "")
            cur["access"].update(re.findall(r"[CRUD]", r.get("Access (C/R/U/D)", "").upper()))  # reviewer additions
            r["_matched"] = True
        for rk, r in rv_obj.items():  # rows a reviewer added that the scan could not see
            status = (r.get("Status") or "").lower()
            if r.get("_matched") or not rk or status.startswith("false"):
                continue
            display.setdefault(rk, r.get("Object", rk).strip("` "))
            cur = usage[rk].setdefault(comp, {"access": set(), "via": set(), "purpose": "", "status": "", "db": ""})
            cur["access"].update(re.findall(r"[CRUD]", r.get("Access (C/R/U/D)", "").upper()))
            cur["via"].add("manual review")
            cur["purpose"] = r.get("Business purpose", "")
            cur["status"] = "Confirmed" if status.startswith("confirm") else "Unreviewed"
            review_stats[comp]["confirmed" if status.startswith("confirm") else "unreviewed"] += 1
        for p in data.get("procedures_called", []):
            k = key(p["object"])
            r = rv_proc.get(k, {})
            status = (r.get("Status") or "").lower()
            if status.startswith("false"):
                continue
            display.setdefault(k, p["object"])
            proc_calls[k][comp] = {"count": p["count"], "purpose": r.get("Business purpose", ""),
                                   "status": "Confirmed" if status.startswith("confirm") else "Unreviewed"}
        for db in data.get("databases", []):
            databases[db["database"]].add(comp)
        for c in data.get("cross_db", []):
            cross.append(dict(c, component=comp))
        for dy in data.get("dynamic_sql", []):
            dynamic[comp].append(dy)

    # Indirect access through stored procedures (transitive over EXEC chains)
    def proc_effects(pk: str, seen=None) -> dict:
        seen = seen or set()
        if pk in seen or pk not in defs:
            return {}
        seen.add(pk)
        eff = defaultdict(set)
        for acc, objs in defs[pk].get("references", {}).items():
            for o in objs:
                if acc == "X":
                    for k2, a2 in proc_effects(key(o), seen).items():
                        eff[k2] |= a2
                else:
                    eff[key(o)] |= set(acc)
        return eff

    indirect = defaultdict(lambda: defaultdict(set))  # object -> component -> access via procs
    for pk, callers in proc_calls.items():
        for ok, accs in proc_effects(pk).items():
            display.setdefault(ok, ok)
            for comp in callers:
                indirect[ok][comp] |= accs

    comp_names = [c for c, _, _ in comps]
    objects = sorted(set(usage) | set(indirect) | {k for k, d in defs.items() if d["type"] in ("TABLE", "VIEW")},
                     key=lambda k: display.get(k, k).lower())
    type_of = lambda k: defs[k]["type"] if k in defs else ("PROC" if k in proc_calls else "unknown (not defined in scanned code)")

    # ---- outputs
    out_md = req / "00-overview" / "sql-inventory.md"
    out_csv = req / "00-overview" / "sql-inventory.csv"
    total_unrev = sum(v["unreviewed"] for v in review_stats.values())
    L = [f"# SQL Inventory — {name}", "",
         f"> **Generated by `kit/tools/sql_inventory.py` on {dt.date.today().isoformat()}. Do not edit.** "
         f"Facts come from `_sql-scan.json` (mechanical scan); purposes and review status come from each component's "
         f"`sql-usage.md`. Spreadsheet version: [sql-inventory.csv](sql-inventory.csv).", "",
         "## Summary", "",
         "| Components with SQL | Tables / views | Stored procedures called | Objects defined in repo | Databases | Cross-db refs | Dynamic SQL sites | Unreviewed usages |",
         "|---|---|---|---|---|---|---|---|",
         f"| {sum(1 for c in comp_names if any(c in usage[k] for k in usage) or any(c in v for v in proc_calls.values()))} "
         f"| {len(objects)} | {len(proc_calls)} | {len(defs)} | {len(databases)} | {len(cross)} "
         f"| {sum(len(v) for v in dynamic.values())} | {total_unrev} |", ""]

    L += ["## Databases", "", "| Database | Used by components |", "|---|---|"]
    L += [f"| {db} | {', '.join(sorted(cs))} |" for db, cs in sorted(databases.items())] or ["| _none found in config_ | |"]
    L += [""]

    L += ["## Object catalogue", "",
          "| Object | Type | Defined in | Used by (direct access) | Via stored procedures | Business purpose |",
          "|---|---|---|---|---|---|"]
    for k in objects:
        d = defs.get(k)
        direct = ", ".join(f"{c} ({''.join(sorted(v['access']))})" for c, v in sorted(usage.get(k, {}).items()))
        ind = ", ".join(f"{c} ({''.join(sorted(a))})" for c, a in sorted(indirect.get(k, {}).items()))
        purpose = next((v["purpose"] for v in usage.get(k, {}).values() if v["purpose"]), "")
        L.append(f"| `{display.get(k, k)}` | {type_of(k)} | {('`' + d['source'] + '`') if d else '—'} | {direct or '—'} | {ind or '—'} | {purpose} |")
    L += [""]

    L += ["## Usage matrix", "",
          "Letters = access (C create, R read, U update, D delete). `*` = only through a stored procedure. "
          "Columns are components.", "",
          "| Object | " + " | ".join(comp_names) + " |", "|---|" + "---|" * len(comp_names)]
    for k in objects:
        cells = []
        for c in comp_names:
            dacc = "".join(sorted(usage.get(k, {}).get(c, {}).get("access", set())))
            iacc = "".join(sorted(indirect.get(k, {}).get(c, set()) - set(dacc)))
            cells.append((dacc + (iacc.lower() + "*" if iacc else "")) or "")
        if any(cells):
            L.append(f"| `{display.get(k, k)}` | " + " | ".join(cells) + " |")
    L += [""]

    shared = []
    for k in objects:
        writers = {c for c, v in usage.get(k, {}).items() if v["access"] & set("CUD")}
        writers |= {c for c, a in indirect.get(k, {}).items() if a & set("CUD")}
        if len(writers) > 1:
            shared.append((k, writers))
    L += ["## Tables written by more than one component", "",
          "Shared writes create hidden coupling: a rule on this data may be enforced (or broken) in several places.", ""]
    L += (["| Object | Writing components |", "|---|---|"] +
          [f"| `{display.get(k, k)}` | {', '.join(sorted(w))} |" for k, w in shared]) if shared else ["_None._"]
    L += [""]

    L += ["## Stored procedures", "", "| Procedure | Defined in | Called by | Reads | Writes | Executes | Business purpose |",
          "|---|---|---|---|---|---|---|"]
    all_procs = sorted(set(proc_calls) | {k for k, d in defs.items() if d["type"] in ("PROC", "FUNCTION")},
                       key=lambda k: display.get(k, k).lower())
    for k in all_procs:
        d = defs.get(k, {}); refs = d.get("references", {})
        writes = sorted(set(refs.get("C", [])) | set(refs.get("U", [])) | set(refs.get("D", [])) | set(refs.get("CU", [])))
        purpose = next((v["purpose"] for v in proc_calls.get(k, {}).values() if v["purpose"]), "")
        L.append(f"| `{display.get(k, k)}` | {('`' + d['source'] + '`') if d else '**not in repo**'} | "
                 f"{', '.join(sorted(proc_calls.get(k, {}))) or '—'} | {', '.join(refs.get('R', [])) or '—'} | "
                 f"{', '.join(writes) or '—'} | {', '.join(refs.get('X', [])) or '—'} | {purpose} |")
    if not all_procs:
        L.append("| _none_ | | | | | | |")
    L += [""]

    referenced = set(usage) | set(proc_calls) | set(indirect)
    for d in defs.values():
        for objs in d.get("references", {}).values():
            referenced |= {key(o) for o in objs}
    unused = [k for k, d in defs.items() if k not in referenced and d["type"] in ("TABLE", "VIEW", "PROC", "FUNCTION")]
    undefined = [k for k in (set(usage) | set(proc_calls)) if k not in defs and defs]
    L += ["## Defined but never referenced (possible dead objects)", ""]
    L += [f"- `{display.get(k, k)}` ({defs[k]['type']}, `{defs[k]['source']}`)" for k in sorted(unused)] or ["_None._"]
    L += ["", "## Referenced but not defined in the scanned code", "",
          "Usually means the DDL lives outside the repo (export it into `projects/<name>/evidence/` and scan it), "
          "or the name is an ORM entity not mapped to a table."
          if defs else "No DDL was scanned, so this check is skipped. Scan the database project or exported DDL to enable it.", ""]
    L += [f"- `{display.get(k, k)}` — used by {', '.join(sorted(set(usage.get(k, {})) | set(proc_calls.get(k, {}))))}"
          for k in sorted(undefined)] or (["_None._"] if defs else [])
    L += [""]

    L += ["## Cross-database and linked-server references", ""]
    L += (["| Object | Database | Linked server | Component | Source |", "|---|---|---|---|---|"] +
          [f"| `{c['object']}` | {c['database']} | {c['server'] or '—'} | {c['component']} | `{c['source']}` |" for c in cross]) \
        if cross else ["_None._"]
    L += ["", "## Dynamic SQL (objects may be missing from this inventory)", ""]
    L += (["| Component | Sites | First source |", "|---|---|---|"] +
          [f"| {c} | {len(v)} | `{v[0]['source']}` |" for c, v in sorted(dynamic.items())]) if dynamic else ["_None._"]
    L += ["", "## Review status", "", "| Component | Confirmed | Unreviewed | False positives excluded |", "|---|---|---|---|"]
    L += [f"| {c} | {v['confirmed']} | {v['unreviewed']} | {v['false']} |" for c, v in sorted(review_stats.items())]
    out_md.write_text("\n".join(L) + "\n", encoding="utf-8")

    with out_csv.open("w", newline="", encoding="utf-8-sig") as fh:
        w = csv.writer(fh)
        w.writerow(["Object", "Type", "Database", "Component", "Access", "Indirect access (via procedures)",
                    "Via", "Business purpose", "Review status", "Defined in"])
        for k in objects:
            comps_k = set(usage.get(k, {})) | set(indirect.get(k, {}))
            for c in sorted(comps_k):
                v = usage.get(k, {}).get(c, {})
                w.writerow([display.get(k, k), type_of(k), v.get("db", ""), c, "".join(sorted(v.get("access", set()))),
                            "".join(sorted(indirect.get(k, {}).get(c, set()))), "; ".join(sorted(v.get("via", set()))),
                            v.get("purpose", ""), v.get("status", "Indirect only"), defs.get(k, {}).get("source", "")])
        for k in all_procs:
            for c, v in sorted(proc_calls.get(k, {}).items()):
                w.writerow([display.get(k, k), "PROC", "", c, "EXEC", "", "procedure call", v["purpose"], v["status"],
                            defs.get(k, {}).get("source", "")])
    print(f"Wrote {out_md} and {out_csv.name}: {len(objects)} objects, {len(all_procs)} procedures, "
          f"{len(shared)} shared-write objects, {total_unrev} unreviewed usages")


if __name__ == "__main__":
    main()
