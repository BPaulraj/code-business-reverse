# /re-wiki — Publish the project to an Azure DevOps wiki (one page per component, sub-pages when large)

**ARGUMENTS:** `[build | push | publish] [--dry-run] [--prune] [business | engineering]`
- **Default** is `publish`: build, then push.
- **`build`** only generates the page tree locally, so you can preview it.
- **`push --dry-run`** shows what would change on the wiki, without changing anything.
- **`--prune`** deletes generated pages that no longer exist, for example a removed component.
- **`business`** (default) hides code citations and technical notes. **`engineering`** keeps them.

Follow `kit/RULES.md` §0 to resolve the active project. **This procedure never reads application code and never writes to `<TARGET>`.**

## What gets published

```
<Wiki parent path>/
└── <Product> Business Requirements      ← summary, confirmation status, contents
    ├── Business Requirements Specification
    ├── Overview  (+ Component Map, Glossary, Coverage)
    ├── Business Processes  (one page per P-NNN)
    ├── Domain Model        (one page per entity)
    ├── Components
    │   └── <Component>     ← capability page
    │       ├── Rules       (split into "Rules - <business area>" sub-pages above the split threshold)
    │       ├── API Catalogue / Nightly Schedule / Batch Jobs / File Layouts   (when present)
    │       └── Questions and Issues
    ├── User Journeys  (per application)
    ├── Integrations
    ├── Open Decisions
    └── Known Issues
```

Every page carries a "generated, do not edit" banner with the code commit and the date. Diagrams are converted to ADO's Mermaid syntax, and links between documents become wiki links.

## Publishing switch (check this first)

Uploading is controlled per project by the **`Wiki publishing`** row in `projects/<name>/project.md`:

| Value | Behaviour |
|---|---|
| `off` (default, also when the row is missing) | **Never upload** on your own initiative. `build` and `push --dry-run` are allowed. A real push happens only if the user **explicitly asked for it in this conversation** *and* confirms a one-off upload. Then run the push with `--confirm`, and don't change the setting. |
| `on-request` | Upload when the user runs `/re-wiki` (push or publish) |
| `auto` | As on-request, and `/re-publish` also runs this procedure at its end |

- Run `python kit/tools/ado_wiki.py check` to see the effective mode and settings. It never shows the token.
- The tool enforces the switch: a push on an `off` project exits with code 4 unless `--confirm` is given.
- **Never pass `--confirm` without the user's explicit agreement in the current conversation.**
- Only change the `Wiki publishing` value when the user asks you to.

## Steps

1. **Check the configuration.** The tool reads, in order: `ado.properties` at the kit root (local only, git-ignored; template: `ado.properties.example`), then the `project.md` rows, then environment variables, then command options.

   | Setting | project.md row | Env var | Example |
   |---|---|---|---|
   | Organisation / collection URL | `ADO org URL` | `ADO_ORG_URL` | `https://dev.azure.com/myorg` or `https://ado.mycorp.local/DefaultCollection` |
   | Project | `ADO project` | `ADO_PROJECT` | `Platform` |
   | Wiki name | `Wiki name` | `ADO_WIKI` | `Platform.wiki` (default: the first wiki found) |
   | Parent path | `Wiki parent path` | `ADO_WIKI_PARENT` | `Business Requirements` |
   | View | `Wiki view` | — | `business` / `engineering` |
   | Split threshold (rules per page) | `Wiki split threshold` | — | `25` |
   | API version | `ADO API version` | `ADO_API_VERSION` | `7.1` (cloud). Azure DevOps Server 2022: `7.0`. Server 2020: `6.0`. |
   | **Token** | **never in project.md** | `ADO_PAT` | Wiki (Read & write) scope |

   If a setting is missing, ask the user and record it in `project.md`, **except the token**. The token must be set by the user as `ADO_PAT`, or in `ado.properties` for local testing. **Never write a token into any tracked file, and never print it.**
2. **Make sure the content is current:** run `/re-coverage` (and `/re-publish`, if the specification should be included) before publishing.
3. **Build:** `python kit/tools/ado_wiki.py build`. Show the page tree it prints.
4. **Dry run** (always on the first publish to a wiki): `python kit/tools/ado_wiki.py push --dry-run`. Show what would be created or updated, and get the user's agreement before the first real push.
5. **Push:** `python kit/tools/ado_wiki.py push` (add `--prune` only if the user asked). Only changed pages are sent, so re-running is safe and cheap.
6. **Final message:** pages created, updated, unchanged and failed, the wiki URL, and any warnings.

## Notes

- **Alternative without the API (code wiki):** `projects/<name>/wiki/` already uses code-wiki file naming and `.order` files. Commit that folder to an ADO Git repo and use **Publish code as wiki** once. Every later push of the folder updates the wiki.
- **ADO's Mermaid version is older than GitHub's.** Simple flowcharts and sequence diagrams render. If a complex state diagram doesn't, simplify it in the source working file.
- **Comments on wiki pages are not read back.** Product decisions must still go through review packs and `/re-apply-review`.
- **Proxy / on-premises certificates:** set `HTTPS_PROXY` if needed. For internal certificate authorities, make sure Python trusts your corporate root certificate (e.g. `SSL_CERT_FILE`).
