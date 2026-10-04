#!/usr/bin/env python3
"""
Publish a kit project to an Azure DevOps wiki (cloud or Azure DevOps Server).

    python kit/tools/ado_wiki.py build [--project NAME] [--view business|engineering]
    python kit/tools/ado_wiki.py push  [--project NAME] [--dry-run] [--prune]

build  Turns projects/<name>/requirements (+ deliverables) into a page tree under
       projects/<name>/wiki/ : one page per component, sub-pages when a component is
       large. The folder uses code-wiki naming and .order files, so it can also be
       published as a "code wiki" from a Git repo with no API at all.
push   Creates / updates only the pages whose content changed, through the ADO REST API.

Configuration (later sources override earlier ones)
  1. ado.properties at the kit root      (local testing; NEVER commit — it is git-ignored)
       ado.org.url, ado.project, ado.pat, ado.wiki, ado.wiki.parent, ado.api.version
  2. projects/<name>/project.md rows     ADO org URL | ADO project | Wiki name |
                                         Wiki parent path | Wiki view | Wiki split threshold | ADO API version
  3. environment variables               ADO_ORG_URL, ADO_PROJECT, ADO_PAT, ADO_WIKI, ADO_WIKI_PARENT, ADO_API_VERSION
  4. command-line options
The personal access token is read ONLY from ADO_PAT or ado.properties (scope: Wiki Read & write).

Publishing switch (per project, project.md row "Wiki publishing"; only project.md can switch it on):
  off (default)  never upload; 'build', 'check' and 'push --dry-run' still work;
                 a one-off upload needs --confirm (explicit user request only)
  on-request     upload when the user runs push/publish
  auto           as on-request; /re-publish also triggers the upload
    python kit/tools/ado_wiki.py check        shows effective settings (never the token)
Standard library only; no packages to install.
"""
from __future__ import annotations

import argparse
import base64
import datetime as dt
import hashlib
import json
import os
import re
import shutil
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

KIT = Path(__file__).resolve().parents[2]
BAD_TITLE_CHARS = re.compile(r'[\\/#:*?"<>|\[\]]')
INTERNAL_FILES = {"_progress.md", "_verification.md", "_glossary-candidates.md", "README.md"}


# --------------------------------------------------------------------------- configuration

def read_kv(path: Path) -> dict:
    out = {}
    if path.exists():
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                out[k.strip()] = v.strip()
    return out


def project_md_fields(path: Path) -> dict:
    fields = {}
    if path.exists():
        for m in re.finditer(r"^\|\s*([^|]+?)\s*\|\s*([^|]*?)\s*\|\s*$", path.read_text(encoding="utf-8"), re.M):
            fields[m.group(1)] = m.group(2)
    return fields


def load_config(args) -> dict:
    name = args.project or (KIT / "projects" / ".active").read_text(encoding="utf-8").strip()
    proj_dir = KIT / "projects" / name
    if not proj_dir.exists():
        sys.exit(f"Project not found: {proj_dir}")
    props = read_kv(Path(args.props) if args.props else KIT / "ado.properties")
    pm = project_md_fields(proj_dir / "project.md")
    cfg = {
        "name": name, "dir": proj_dir,
        "org": props.get("ado.org.url", ""), "ado_project": props.get("ado.project", ""),
        "wiki": props.get("ado.wiki", ""), "parent": props.get("ado.wiki.parent", ""),
        "api": props.get("ado.api.version", "7.1"), "pat": props.get("ado.pat", ""),
        "view": "business", "split": 25,
        "publishing": "off", "publishing_default": True,
        "commit": pm.get("Commit analysed", ""),
    }
    for key, field in (("org", "ADO org URL"), ("ado_project", "ADO project"), ("wiki", "Wiki name"),
                       ("parent", "Wiki parent path"), ("view", "Wiki view"), ("api", "ADO API version")):
        v = pm.get(field, "").strip()
        if v and not v.startswith("("):
            cfg[key] = v
    if pm.get("Wiki split threshold", "").strip().isdigit():
        cfg["split"] = int(pm["Wiki split threshold"])
    for key, env in (("org", "ADO_ORG_URL"), ("ado_project", "ADO_PROJECT"), ("pat", "ADO_PAT"),
                     ("wiki", "ADO_WIKI"), ("parent", "ADO_WIKI_PARENT"), ("api", "ADO_API_VERSION")):
        if os.environ.get(env):
            cfg[key] = os.environ[env]
    # Publishing is a per-project decision: only project.md can switch it on (never ado.properties or env).
    pub = pm.get("Wiki publishing", "").strip().lower().split(" ")[0] if pm.get("Wiki publishing") else ""
    if pub:
        if pub not in ("off", "on-request", "auto"):
            sys.exit(f"Invalid 'Wiki publishing' value in project.md: '{pub}'. Use off, on-request or auto.")
        cfg["publishing"], cfg["publishing_default"] = pub, False
    for key in ("view", "parent", "wiki"):
        if getattr(args, key, None):
            cfg[key] = getattr(args, key)
    cfg["org"] = cfg["org"].rstrip("/")
    # Git Bash (MSYS) rewrites "/Some Path" arguments into "C:/Program Files/Git/Some Path": undo that.
    m = re.match(r"^[A-Za-z]:[/\\].*?[/\\]Git[/\\](.*)$", cfg["parent"])
    if m:
        print(f"  ! wiki parent looked like a Git Bash path; using '/{m.group(1)}'. "
              f"Tip: pass it without the leading slash, or set 'Wiki parent path' in project.md.", file=sys.stderr)
        cfg["parent"] = m.group(1)
    cfg["parent"] = cfg["parent"].replace("\\", "/")
    cfg["parent"] = "/" + cfg["parent"].strip("/") if cfg["parent"].strip("/") else ""
    return cfg


# --------------------------------------------------------------------------- page model

class Page:
    def __init__(self, title: str, content: str = "", source: Path | None = None):
        self.title = clean_title(title)
        self.content = content
        self.source = source
        self.children: list[Page] = []

    def add(self, page: "Page") -> "Page":
        existing = {c.title for c in self.children}
        base, k = page.title, 2
        while page.title in existing:
            page.title = f"{base} ({k})"; k += 1
        self.children.append(page)
        return page


def clean_title(t: str) -> str:
    t = re.sub(r"[`*_]", "", t)
    t = BAD_TITLE_CHARS.sub("-", t)
    t = re.sub(r"\s+", " ", t).strip(" .-")
    return t[:200] or "Untitled"


def fs_name(title: str) -> str:
    """Code-wiki file/folder naming: '-' -> %2D, space -> '-'."""
    return title.replace("-", "%2D").replace(" ", "-")


def wiki_link_path(path_titles: list[str]) -> str:
    return "/" + "/".join(urllib.parse.quote(fs_name(t), safe="%-") for t in path_titles)


def first_h1(text: str) -> str | None:
    m = re.search(r"^#\s+(.+)$", text, re.M)
    return m.group(1).strip() if m else None


def strip_h1(text: str) -> str:
    return re.sub(r"^#\s+.+\n+", "", text, count=1, flags=re.M)


# --------------------------------------------------------------------------- content transforms

def to_ado_markdown(text: str, view: str) -> str:
    # Mermaid fences -> ADO ':::' blocks
    text = re.sub(r"^```mermaid\s*\n(.*?)^```\s*$", lambda m: "::: mermaid\n" + m.group(1) + ":::",
                  text, flags=re.S | re.M)
    text = re.sub(r"<!--.*?-->\n?", "", text, flags=re.S)
    if view == "business":
        text = strip_engineering(text)
    return text


def strip_engineering(text: str) -> str:
    """Business view: drop Source / Technical note bullets (and their nested lines) from rule blocks."""
    out, skipping = [], False
    for line in text.splitlines():
        if re.match(r"^- \*\*(Source|Technical note):\*\*", line):
            skipping = True
            continue
        if skipping and (line.startswith("  ") and line.strip()):
            continue
        skipping = False
        out.append(line)
    return "\n".join(out)


def split_rules(text: str, threshold: int):
    """Return (intro, [(group_title, body)]) when the rules file is large and has '## ' groups,
    or (intro, chunks) for large files without groups; None when no split is needed."""
    if len(re.findall(r"^### BR-", text, re.M)) <= threshold:
        return None
    parts = re.split(r"^(## .+)$", text, flags=re.M)
    intro, groups = parts[0], []
    for i in range(1, len(parts), 2):
        title = parts[i][3:].strip()
        body = parts[i + 1]
        if title.lower().startswith("summary") or "### BR-" not in body:
            intro += parts[i] + body
            continue
        groups.append((title, body))
    if groups:
        return intro, [(f"Rules - {t}", b) for t, b in groups]
    rules = re.split(r"(?=^### BR-)", text, flags=re.M)
    head, blocks = rules[0], rules[1:]
    chunks = []
    for i in range(0, len(blocks), threshold):
        part = blocks[i:i + threshold]
        ids = [re.match(r"### (BR-[\w-]+)", b).group(1) for b in part]
        chunks.append((f"Rules {ids[0]} to {ids[-1]}", "".join(part)))
    return head, chunks


# --------------------------------------------------------------------------- build

def build_tree(cfg) -> tuple[Page, dict]:
    req = cfg["dir"] / "requirements"
    deliv = cfg["dir"] / "deliverables"
    if not req.exists():
        sys.exit(f"No requirements folder: {req}")
    view, split = cfg["view"], cfg["split"]
    source_map: dict[Path, list[str]] = {}

    def read(p: Path) -> str:
        return p.read_text(encoding="utf-8")

    def page_from(p: Path, title: str | None = None, parent: Page | None = None) -> Page:
        t = read(p)
        pg = Page(title or first_h1(t) or p.stem, strip_h1(t), p)
        if parent:
            parent.add(pg)
        return pg

    root_title = f"{cfg['name'].replace('-', ' ').title()} Business Requirements"
    brs = deliv / "Business-Requirements-Specification.md"
    home = ""
    if brs.exists():
        b = read(brs)
        root_title = clean_title((first_h1(b) or root_title).split("—")[0].strip() + " Business Requirements")
        m = re.search(r"^## 1\..*?(?=^## 3\.)", b, re.S | re.M)
        home = m.group(0) if m else ""
    root = Page(root_title, home + "\n\n## Sections\n\n[[_TOSP_]]\n")

    if brs.exists():
        page_from(brs, "Business Requirements Specification", root)

    # Overview
    ov_dir = req / "00-overview"
    if (ov_dir / "system-context.md").exists():
        ov = page_from(ov_dir / "system-context.md", "Overview", root)
        ov.content += "\n\n[[_TOSP_]]\n"
        for f, t in (("component-map.md", "Component Map"), ("glossary.md", "Glossary"),
                     ("coverage-tracker.md", "Coverage")):
            src = (req / f) if f == "component-map.md" else (ov_dir / f)
            if src.exists():
                page_from(src, t, ov)

    def section(folder: Path, title: str, intro: str, pattern="*.md") -> Page | None:
        files = sorted(p for p in folder.glob(pattern) if p.name not in INTERNAL_FILES and not p.name.startswith("_"))
        if not files:
            return None
        sec = root.add(Page(title, intro + "\n\n[[_TOSP_]]\n"))
        for f in files:
            page_from(f, parent=sec)
        return sec

    section(req / "02-processes", "Business Processes", "End-to-end business processes, with failure paths.")
    section(req / "01-domain" / "entities", "Domain Model", "What the business manages and how each item changes state.")

    # Components
    cap = req / "03-capabilities"
    comp_dirs = sorted(d for d in cap.iterdir() if d.is_dir()) if cap.exists() else []
    if comp_dirs:
        comps = root.add(Page("Components", "One page per component. Large components have sub-pages.\n\n[[_TOSP_]]\n"))
        for d in comp_dirs:
            capf = d / "capability.md"
            title = (first_h1(read(capf)) or d.name).split("—")[0].strip() if capf.exists() else d.name
            cp = comps.add(Page(title, strip_h1(read(capf)) if capf.exists() else "", capf if capf.exists() else None))
            cp.content += "\n\n## Pages\n\n[[_TOSP_]]\n"
            rules = d / "rules.md"
            if rules.exists():
                t = read(rules)
                s = split_rules(t, split)
                if s:
                    intro, parts = s
                    rp = cp.add(Page("Rules", strip_h1(intro) + "\n\n[[_TOSP_]]\n", rules))
                    for gt, body in parts:
                        rp.add(Page(gt, body))
                else:
                    cp.add(Page("Rules", strip_h1(t), rules))
            for f, t in (("api-catalogue.md", "API Catalogue"), ("batch-schedule.md", "Nightly Schedule")):
                if (d / f).exists():
                    page_from(d / f, t, cp)
            for sub, t in (("jobs", "Batch Jobs"), ("file-layouts", "File Layouts")):
                if (d / sub).is_dir() and any((d / sub).glob("*.md")):
                    sp = cp.add(Page(t, "[[_TOSP_]]\n"))
                    for f in sorted((d / sub).glob("*.md")):
                        page_from(f, parent=sp)
            qd = [d / "_questions.md", d / "_defects.md"]
            body = "\n\n".join(strip_h1(read(f)).strip() for f in qd if f.exists() and "| " in read(f).split("|---", 1)[-1])
            if body.strip():
                qp = cp.add(Page("Questions and Issues", body))
                for f in qd:
                    source_map[f.resolve()] = []  # filled below
                qp.source = qd[0]
            source_map[d.resolve()] = []

    # User journeys and integrations
    uj = req / "05-user-journeys"
    if uj.exists():
        groups = [g for g in sorted(uj.iterdir()) if g.is_dir() and any(
            p for p in g.glob("*.md") if not p.name.startswith("_"))]
        if groups:
            ujp = root.add(Page("User Journeys", "What users see and do, screen by screen.\n\n[[_TOSP_]]\n"))
            for g in groups:
                gp = ujp.add(Page(g.name.replace("-", " ").title(), "[[_TOSP_]]\n"))
                for f in sorted(p for p in g.glob("*.md") if not p.name.startswith("_")):
                    page_from(f, parent=gp)
    section(req / "04-integrations", "Integrations", "Exchanges with third-party systems.")

    for f, t in (("06-open-questions.md", "Open Decisions"), ("07-suspected-defects.md", "Known Issues")):
        if (req / f).exists():
            page_from(req / f, t, root)

    # Map source files to page paths for link rewriting
    def walk(pg: Page, path: list[str]):
        if pg.source:
            source_map[Path(pg.source).resolve()] = path
        for c in pg.children:
            walk(c, path + [c.title])
    walk(root, [root.title])
    for d in comp_dirs:  # questions/defects files -> their component's Q&I page
        for f in ("_questions.md", "_defects.md"):
            p = (d / f).resolve()
            if p in source_map and not source_map[p]:
                q = (d / "_questions.md").resolve()
                source_map[p] = source_map.get(q) or []
    return root, source_map


def rewrite_links(text: str, page_src: Path | None, source_map: dict, prefix: list[str] | None = None) -> str:
    def repl(m):
        label, target = m.group(1), m.group(2)
        if re.match(r"^(https?:|mailto:|#|/)", target):
            return m.group(0)
        if page_src is None:
            return label
        resolved = (Path(page_src).parent / target.split("#")[0]).resolve()
        path = source_map.get(resolved)
        return f"[{label}]({wiki_link_path((prefix or []) + path)})" if path else label
    return re.sub(r"(?<!!)\[([^\]]+)\]\(([^)]+)\)", repl, text)


def render(page: Page, source_map, cfg, stamp) -> str:
    prefix = [seg for seg in cfg["parent"].strip("/").split("/") if seg]
    body = rewrite_links(page.content, page.source, source_map, prefix)
    body = to_ado_markdown(body, cfg["view"])
    banner = (f"> 🔄 **Generated** by the reverse-engineering kit from project `{cfg['name']}` "
              f"(code commit `{cfg['commit'][:7] or 'n/a'}`, {stamp}, {cfg['view']} view). "
              f"**Do not edit this page**: changes are overwritten on the next publish. "
              f"Give feedback through the review packs.\n\n")
    toc = "[[_TOC_]]\n\n" if len(re.findall(r"^#{2,3} ", body, re.M)) >= 4 else ""
    return banner + toc + body.strip() + "\n"


def cmd_build(cfg) -> Path:
    root, source_map = build_tree(cfg)
    out = cfg["dir"] / "wiki"
    out.mkdir(parents=True, exist_ok=True)
    for child in out.iterdir():  # clear contents, not the folder (it may be open in an editor/Explorer)
        try:
            shutil.rmtree(child) if child.is_dir() else child.unlink()
        except OSError as e:
            sys.exit(f"Cannot clear {child}: {e}. Close any program using the wiki folder and retry.")
    stamp = dt.date.today().isoformat()
    manifest = []

    def emit(pg: Page, folder: Path, titles: list[str]):
        content = render(pg, source_map, cfg, stamp)
        (folder / f"{fs_name(pg.title)}.md").write_text(content, encoding="utf-8")
        manifest.append({"path": "/" + "/".join(titles), "file": str((folder / f"{fs_name(pg.title)}.md").relative_to(out)),
                         "sha": hashlib.sha256(content.encode()).hexdigest()})
        if pg.children:
            sub = folder / fs_name(pg.title)
            sub.mkdir(exist_ok=True)
            (sub / ".order").write_text("\n".join(fs_name(c.title) for c in pg.children) + "\n", encoding="utf-8")
            for c in pg.children:
                emit(c, sub, titles + [c.title])

    emit(root, out, [root.title])
    (out / ".order").write_text(fs_name(root.title) + "\n", encoding="utf-8")
    (out / ".manifest.json").write_text(json.dumps({"root": root.title, "view": cfg["view"], "built": stamp,
                                                    "pages": manifest}, indent=1), encoding="utf-8")
    depth = max(p["path"].count("/") for p in manifest)
    print(f"Built {len(manifest)} pages (max depth {depth}) in {out}")
    for p in manifest[:60]:
        print("  " + "  " * (p["path"].count("/") - 1) + p["path"].rsplit("/", 1)[-1])
    if len(manifest) > 60:
        print(f"  … {len(manifest) - 60} more")
    return out


# --------------------------------------------------------------------------- push (REST API)

class Ado:
    def __init__(self, cfg):
        for k in ("org", "ado_project", "pat"):
            if not cfg[k]:
                sys.exit(f"Missing configuration: {k} (see the header of this script)")
        self.base = f"{cfg['org']}/{urllib.parse.quote(cfg['ado_project'])}/_apis/wiki/wikis"
        self.api = cfg["api"]
        self.auth = "Basic " + base64.b64encode((":" + cfg["pat"]).encode()).decode()

    def call(self, method, url, body=None, headers=None):
        h = {"Authorization": self.auth, "Accept": "application/json"}
        data = None
        if body is not None:
            data = json.dumps(body).encode("utf-8")
            h["Content-Type"] = "application/json"
        h.update(headers or {})
        req = urllib.request.Request(url, data=data, method=method, headers=h)
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                raw = r.read()
                return r.status, dict(r.headers), (json.loads(raw) if raw else {})
        except urllib.error.HTTPError as e:
            raw = e.read()
            try:
                payload = json.loads(raw)
            except ValueError:
                payload = {"message": raw[:300].decode("utf-8", "replace")}
            return e.code, dict(e.headers), payload

    def wiki_id(self, name):
        s, _, j = self.call("GET", f"{self.base}?api-version={self.api}")
        if s == 401 or s == 203:
            sys.exit("Authentication failed: check the PAT and its Wiki (Read & write) scope.")
        if s != 200:
            sys.exit(f"Could not list wikis ({s}): {j.get('message')}")
        wikis = j.get("value", [])
        if not wikis:
            sys.exit("No wiki exists in this project yet. Create the project wiki once in the ADO portal (Overview > Wiki).")
        for w in wikis:
            if not name or w["name"].lower() == name.lower():
                return w["id"], w["name"], w["type"]
        sys.exit(f"Wiki '{name}' not found. Available: {', '.join(w['name'] for w in wikis)}")

    def page_url(self, wid, path, extra=""):
        return f"{self.base}/{wid}/pages?path={urllib.parse.quote(path)}&api-version={self.api}{extra}"

    def get_page(self, wid, path):
        s, h, j = self.call("GET", self.page_url(wid, path, "&includeContent=true"))
        if s == 200:
            return j.get("content", ""), h.get("ETag") or h.get("etag")
        return None, None

    def put_page(self, wid, path, content, etag=None):
        headers = {"If-Match": etag} if etag else {}
        return self.call("PUT", self.page_url(wid, path), {"content": content}, headers)

    def delete_page(self, wid, path):
        return self.call("DELETE", self.page_url(wid, path))

    def list_tree(self, wid, path):
        s, _, j = self.call("GET", self.page_url(wid, path, "&recursionLevel=full"))
        out = []

        def walk(node):
            out.append(node["path"])
            for c in node.get("subPages", []):
                walk(c)
        if s == 200:
            walk(j)
        return out


def norm(s: str) -> str:
    return "\n".join(l.rstrip() for l in (s or "").replace("\r\n", "\n").strip().splitlines())


def cmd_push(cfg, dry_run: bool, prune: bool):
    out = cfg["dir"] / "wiki"
    mf = out / ".manifest.json"
    if not mf.exists():
        sys.exit("Nothing built yet: run 'build' first.")
    manifest = json.loads(mf.read_text(encoding="utf-8"))
    ado = Ado(cfg)
    wid, wname, wtype = ado.wiki_id(cfg["wiki"])
    parent = cfg["parent"]
    print(f"Wiki '{wname}' ({wtype}) in {cfg['ado_project']} | parent: {parent or '/'} | {len(manifest['pages'])} pages"
          + (" | DRY RUN" if dry_run else ""))
    if wtype == "codeWiki":
        print("  ! This is a code wiki: publish projects/<name>/wiki/ through Git instead of the API.")
        return 1

    # Ensure the parent path exists.
    if parent:
        acc = ""
        for seg in parent.strip("/").split("/"):
            acc += "/" + seg
            content, _ = ado.get_page(wid, acc)
            if content is None:
                print(f"  {'would create' if dry_run else 'create'} parent {acc}")
                if not dry_run:
                    s, _, j = ado.put_page(wid, acc, "Container page for generated business requirements.\n\n[[_TOSP_]]\n")
                    if s not in (200, 201):
                        sys.exit(f"Could not create {acc} ({s}): {j.get('message')}")

    created = updated = unchanged = failed = 0
    wanted = set()
    for p in manifest["pages"]:
        path = parent + p["path"]
        wanted.add(path)
        content = (out / p["file"]).read_text(encoding="utf-8")
        remote, etag = ado.get_page(wid, path)
        if remote is not None and norm(remote) == norm(content):
            unchanged += 1
            continue
        action = "update" if remote is not None else "create"
        if dry_run:
            print(f"  would {action} {path}")
            created += action == "create"; updated += action == "update"
            continue
        s, _, j = ado.put_page(wid, path, content, etag if remote is not None else None)
        if s in (200, 201):
            created += action == "create"; updated += action == "update"
            print(f"  {action}d {path}")
        else:
            failed += 1
            print(f"  ! {action} failed {path} ({s}): {j.get('message')}", file=sys.stderr)

    pruned = 0
    if prune:
        root_path = parent + "/" + manifest["root"]
        remote_paths = ado.list_tree(wid, root_path)
        for rp in sorted((x for x in remote_paths if x not in wanted), key=lambda x: -x.count("/")):
            if any(w.startswith(rp + "/") for w in wanted):
                continue
            print(f"  {'would delete' if dry_run else 'delete'} {rp}")
            if not dry_run:
                s, _, j = ado.delete_page(wid, rp)
                pruned += s in (200, 204)
    print(f"Done: {created} created, {updated} updated, {unchanged} unchanged, {failed} failed"
          + (f", {pruned} deleted" if prune else ""))
    root_url = f"{cfg['org']}/{urllib.parse.quote(cfg['ado_project'])}/_wiki/wikis/{urllib.parse.quote(wname)}"
    print(f"Open: {root_url}  →  {parent}/{manifest['root']}")
    return 1 if failed else 0


# --------------------------------------------------------------------------- main

def main(argv=None):
    for stream in (sys.stdout, sys.stderr):  # never crash on consoles that can't show '—' or '→'
        try:
            stream.reconfigure(errors="replace")
        except (AttributeError, ValueError):
            pass
    ap = argparse.ArgumentParser(description="Publish a kit project to an Azure DevOps wiki.")
    ap.add_argument("action", choices=["check", "build", "push", "publish"],
                    help="check = show effective settings; publish = build + push")
    ap.add_argument("--project", help="kit project name (default: projects/.active)")
    ap.add_argument("--view", choices=["business", "engineering"], help="business hides code citations")
    ap.add_argument("--parent", help="wiki parent path, e.g. '/Business Requirements'")
    ap.add_argument("--wiki", help="wiki name (default: the project wiki)")
    ap.add_argument("--props", help="path to an ado.properties file")
    ap.add_argument("--dry-run", action="store_true", help="push: show what would change, change nothing")
    ap.add_argument("--prune", action="store_true", help="push: delete generated pages that no longer exist")
    ap.add_argument("--confirm", action="store_true",
                    help="one-off push for a project whose 'Wiki publishing' is off (explicit user request only)")
    a = ap.parse_args(argv)
    cfg = load_config(a)
    mode = cfg["publishing"]

    if a.action == "check":
        print(f"Project            : {cfg['name']}")
        print(f"Wiki publishing    : {mode}" + ("  (default — no 'Wiki publishing' row in project.md)" if cfg["publishing_default"] else ""))
        print(f"ADO org URL        : {cfg['org'] or '(not set)'}")
        print(f"ADO project        : {cfg['ado_project'] or '(not set)'}")
        print(f"Wiki name          : {cfg['wiki'] or '(first wiki in the project)'}")
        print(f"Wiki parent path   : {cfg['parent'] or '/'}")
        print(f"Wiki view          : {cfg['view']}   | split threshold: {cfg['split']} rules")
        print(f"ADO API version    : {cfg['api']}")
        print(f"Access token       : {'present' if cfg['pat'] else 'NOT SET (set ADO_PAT)'}")
        return 0

    if a.action in ("push", "publish") and not a.dry_run and mode == "off" and not a.confirm:
        print(f"Wiki publishing is OFF for project '{cfg['name']}', so nothing was uploaded.\n"
              f"  • To enable it, set 'Wiki publishing' in projects/{cfg['name']}/project.md to on-request or auto.\n"
              f"  • For a one-off upload the user has explicitly asked for, re-run with --confirm.\n"
              f"  • 'build' (local preview) and 'push --dry-run' are always allowed.", file=sys.stderr)
        return 4

    if a.action in ("build", "publish"):
        cmd_build(cfg)
    if a.action in ("push", "publish"):
        if mode == "off" and a.confirm and not a.dry_run:
            print("  ! One-off push confirmed by the user (Wiki publishing is off for this project).")
        return cmd_push(cfg, a.dry_run, a.prune)
    return 0


if __name__ == "__main__":
    sys.exit(main())
