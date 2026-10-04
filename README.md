# Business Requirements Reverse-Engineering Kit

A kit for extracting business requirements from a legacy codebase, so the product team can review them.
- **Two tools:** works with **Claude Code** and **GitHub Copilot (VS Code agent mode)**.
- **Read-only on your application:** you run it **from this kit repo**, point it at the application's repo, and every generated document stays here.
- **Built for scale:** a resumable plan, per-entry-point checkpoints, and claims that let parallel sessions share the work.

> **New here? Read the [User Manual](USER-MANUAL.md).** It covers setup, running against the whole mono repo or one component, the order to run commands and agents in, where every document is, the review process (which files product fills in), and how to regenerate.

## Layout

```
code-business-reverse/
├── kit/                               ← SINGLE SOURCE OF TRUTH (tool-neutral)
│   ├── RULES.md                       # project resolution, evidence, confidence, IDs, checkpoints
│   ├── procedures/re-*.md             # the 18 procedures (what each command does)
│   ├── templates/                     # rule, capability, process, entity, integration, journey,
│   │                                  # Q/defect, api-catalogue, batch-job, file-layout, plan
│   ├── examples/good-vs-bad-rules.md  # calibrates output quality
│   ├── tools/ado_wiki.py              # working files → Azure DevOps wiki pages (build / push)
│   ├── tools/export_doc.py            # Markdown → Word (.docx) / PDF, offline (vendor/mermaid.min.js for diagrams)
│   └── skeleton/requirements/         # empty output structure, copied by /re-init
│
├── .claude/                           ← Claude Code wrappers (thin, point to kit/)
│   ├── commands/re-*.md               #   /re-init, /re-discover, … /re-next
│   └── agents/                        #   re-extractor, re-verifier (subagents)
├── CLAUDE.md                          #   loads kit/RULES.md
│
├── .github/                           ← GitHub Copilot wrappers (thin, point to kit/)
│   ├── copilot-instructions.md        #   always-on instructions
│   ├── prompts/re-*.prompt.md         #   /re-init, /re-discover, … /re-next in Copilot Chat
│   └── agents/*.agent.md              #   re-extractor, re-verifier custom agents
├── reverse-kit.code-workspace.example #   VS Code multi-root workspace: kit + target repo
│
├── projects/
│   ├── .active                        # which project the commands work on
│   └── <name>/
│       ├── project.md                 # target repo path + commit analysed
│       ├── deliverables/              # ← stakeholder document: .md (+ .docx / .pdf per preference)
│       └── requirements/              # ← ALL generated output for that application
│           ├── component-map.md, 00-overview/ … 05-user-journeys/, _review/
│           └── _run/                  # plan.md, claims/, run-log.md (large codebases)
└── trial-results.md
```

**To change behaviour, edit `kit/` only.** The `.claude/` and `.github/` files just say "follow `kit/procedures/<name>.md`".

**Example output:** `projects/stockbroker/` is the full result of a trial on a demo app. Start with `requirements/_review/2026-10-04-accuracy-vs-product-spec.md`.

## Commands (same names in both tools)

| Command | Purpose |
|---|---|
| `/re-init <name> <repo-path>` | Register or switch the application to analyse |
| `/re-discover` | Inventory components, stack and wiring (staged for large repos) |
| `/re-plan` | Build the resumable work plan: sizes, waves, dependencies |
| `/re-next [verify\|status\|<component>]` | Claim and process the next unit of work. Run it repeatedly. |
| `/re-domain` | Database → entities, lifecycles, DB-resident rules |
| `/re-service <component>` | Microservice / connectivity → capability and rules |
| `/re-api <component>` | Web-services layer → API catalogue and rules |
| `/re-batch <component> [inventory\|BJ range]` | Nightly batch → schedule, job files, file layouts |
| `/re-ui <front-end\|back-office>` | Journeys, screen validations, roles |
| `/re-integration <counterparty>` | Third-party contracts |
| `/re-process "<process>"` | End-to-end process across components |
| `/re-verify <folder>` | Independent check against the cited code (fresh session) |
| `/re-review-pack <scope>` | Plain-language pack for product |
| `/re-apply-review <pack>` | Write product decisions back |
| `/re-publish [draft\|baseline] [docx\|pdf\|both]` | Generate the stakeholder Business Requirements Specification (+ Word/PDF) |
| `/re-export [file] [docx\|pdf\|both]` | Export any generated Markdown (BRS, review pack, process) to Word and/or PDF |
| `/re-coverage` | Recount, consolidate, consistency and citation checks |
| `/re-wiki [build\|push\|publish] [--dry-run]` | Publish to an Azure DevOps wiki: one page per component, sub-pages when large (cloud or on-prem) |

## Setup

First, confirm that your organisation allows AI-assisted analysis of the codebase with the tool you use. Then copy or clone this kit repo onto a machine that can reach the application's repo. **No files go into the application repo.**

### Option A — GitHub Copilot (VS Code)

1. Copy `reverse-kit.code-workspace.example` to `reverse-kit.code-workspace`. Set the second folder path to your mono repo, then use **File → Open Workspace from File**. Copilot can now read the mono repo. The `files.readonlyInclude` setting in the workspace file helps prevent accidental edits.
2. Open **Copilot Chat** and switch to **Agent** mode. The prompt files already request agent mode.
3. Type `/re-init platform D:\path\to\mono-repo`. All 18 `/re-*` prompts appear when you type `/`.
4. If prompts or instructions don't appear, check that your organisation's Copilot policy allows **prompt files** and **custom instructions**, and that VS Code is recent.

Copilot notes:
- **Subagents:** `re-extractor` and `re-verifier` are available as custom agents (`.github/agents/`). Pick one from the agent dropdown, or let the main agent delegate to it.
- **Fresh session** in the procedures means a **new chat**.
- **Quota:** agent-mode work consumes premium requests. A 75-service extraction is a lot of requests, so check your plan's allowance before scaling.
- **Copilot coding agent (cloud, issue-based) is not suitable** unless both this repo and the application repo are on GitHub and reachable by it. Use VS Code agent mode.

### Option B — Claude Code

1. `claude --add-dir "D:\path\to\mono-repo"` from this kit repo (or `/add-dir` inside a session).
2. Run `/re-init platform D:\path\to\mono-repo`.

**Optional hardening:** add a deny rule for `Edit` and `Write` on the mono-repo path in `.claude/settings.local.json`.

## Scaling to a large codebase (75+ microservices)

### How the work is broken down

| Level | Unit | Where progress is saved | What a crash loses |
|---|---|---|---|
| Programme | Waves of 5–15 components, grouped by business domain | `_run/plan.md` (row status) | Nothing; the status is already on disk |
| Component | One microservice, or one **slice** of a very large one | `_run/claims/<row>.claim`, then the plan row | Nothing; the next `/re-next` resumes the claimed component |
| Entry point | One endpoint, consumer, job or screen | Rules written first, then ticked in `_progress.md` | At most the one entry point in progress |
| Discovery | One top-level folder | `_run/discovery-progress.md` | At most one folder |

The flow is:

```
/re-init → /re-discover (staged) → /re-plan → [ /re-next → new chat ] × N → /re-next verify × N → /re-process … → /re-review-pack
```

### What happens if something fails part-way

- **Session dies, times out or hits a quota mid-component.** Start a new chat and run `/re-next`. It finds your claim, reads `_progress.md`, checks the last entry point for half-written rules, and continues. Nothing already ticked is redone.
- **The machine is lost.** Everything is in the kit repo. **Commit after every component** (the plan header can enable auto-commit) and push to your internal Git server. At most the uncommitted component is lost.
- **Several people or windows in parallel.** Each `/re-next` claims a different row. Claims older than 4 hours are reported as stale, so abandoned work is picked up again.
- **A component can't be done** (no access, unreadable generated code). It is marked `Failed` or `Blocked` with a reason, and the queue moves on.
- **The code changes during the months-long effort.** `project.md` and every `_progress.md` record the commit analysed. Re-extract changed components after updating the commit.

### Processing time and latency (estimates — measure in your pilot)

The timings vary with component size, code quality, model, and tool quotas. The kit measures them for you: `/re-next` writes minutes, entry points and rules for every row to `run-log.md`, and `/re-next status` reports the average time per size class. After about 5 components you'll have your own numbers.

**Planning ranges** (agent working time, not your time):

| Item | Rough range |
|---|---|
| Discovery for 75+ components | a few staged sessions |
| Medium microservice (about 20–40 endpoints) | 30–90 min to extract, plus 15–40 min to verify |
| Large microservice (split into slices) | several sessions |
| End-to-end process (summary-first) | 20–60 min each |

**A 75-service programme** is roughly 100–200 agent-hours of extraction and verification. With 3–5 parallel sessions, that's a few weeks of calendar time. In practice the bottleneck is **people**: spot-checking output and running product review sessions. Plan the waves around review capacity, not agent speed.

### Recommendations for a programme of this size

1. **Run a pilot wave of 3–5 services** across one domain (e.g. client, cash, stock). Tune `kit/RULES.md` and the examples, then measure the timings.
2. **Prioritise by business process, not alphabetically.** Run `/re-plan` with your top processes named, so the services they touch come first and product can review real processes early.
3. **Split huge services** (more than 100 endpoints or more than 100k lines) into slices. `/re-plan` does this automatically.
4. **Verify by wave**, in fresh sessions (`/re-next verify`), before the review packs for that wave.
5. **Commit and push after every component.**
6. **Keep product reviews flowing alongside extraction:** extract wave N+1 while product reviews wave N.

## Word and PDF output

The stakeholder document is always produced as Markdown, which renders on GitHub. Word and PDF are produced on top of it, according to the **Output formats** line in `projects/<name>/project.md` (e.g. `md, docx, pdf`). `/re-init` asks for this once. To override it for one run, use `/re-publish pdf`, or `/re-export <file> docx` for any document.

| Output | Built by | Needs |
|---|---|---|
| `.docx` | `kit/tools/export_doc.py` (python-docx) | Python 3.9+, `pip install -r kit/tools/requirements.txt`. Microsoft Word is optional: if present, it refreshes the table of contents and page numbers automatically. |
| `.pdf` | Edge or Chrome, headless print | A Chromium browser. Each one is tested first, and any that's blocked is skipped. Falls back to **Microsoft Word** if there's no working browser (`--pdf-engine word`). |
| Diagrams | Bundled Mermaid (`kit/tools/vendor/`), rendered by the browser | Offline, no internet. Vector graphics in the PDF, images in the DOCX. If a diagram fails, its source is shown and the error is reported. |

- **Corporate branding:** set **Word template** in `project.md` (or pass `template=<file.docx>`). Its heading, table and font styles are reused.
- **Product reviews in Word:** `/re-export <review-pack>.md docx`. Copy the decisions back into the Markdown pack before `/re-apply-review`.
- **Run it directly:** `python kit/tools/export_doc.py <file.md> --format both` (see `--help`).

## Azure DevOps wiki

`/re-wiki` publishes the project as a page tree in your ADO project wiki: an overview, processes, the domain model, **one page per component** (with **sub-pages per business area** when a component has more than 25 rules), user journeys, open decisions and known issues. It works with Azure DevOps Services (cloud) and Azure DevOps Server (on-prem).

**Off by default.** Nothing is uploaded unless the project switches it on with the `Wiki publishing` row in `project.md`:
- `off` (default): never uploads. Local preview only. A one-off push needs your explicit request and confirmation.
- `on-request`: uploads when you run `/re-wiki`.
- `auto`: also uploads after every `/re-publish`.

`python kit/tools/ado_wiki.py check` shows the effective settings.

1. Put the settings in `project.md`: `Wiki publishing`, `ADO org URL`, `ADO project`, `Wiki parent path` (and optionally `Wiki name`, `Wiki view`, `ADO API version`).
2. Set the token as an environment variable: `ADO_PAT` (scope **Wiki: Read & write**). For local testing only, copy `ado.properties.example` to `ado.properties` at the kit root and fill it in; it is git-ignored.
3. `/re-wiki build` to preview the tree in `projects/<name>/wiki/`, then `/re-wiki push --dry-run`, then `/re-wiki push`. Only changed pages are sent.

No API possible? Commit `projects/<name>/wiki/` to an ADO repo and use **Publish code as wiki**. The folder already has the right file names and `.order` files.

## Working tips

- **Version control the kit repo.** Product can then review requirements as PRs. The application repo is never touched.
- **Always verify in a fresh session or new chat.** The verifier must not share context with the extractor.
- **Evidence from outside the repo** (DDL exports, scheduler exports, production config, runbooks): put it in `projects/<name>/evidence/` and mention it in your prompt.
- **Old documents** are useful as a benchmark, but don't feed them in during extraction. In the demo trial, 19 of 20 documented rules were recovered from code alone (see `trial-results.md`).

## Quality checks before showing anything to product

- [ ] `/re-coverage` reports no consistency problems, including broken citations.
- [ ] Every rule has Source and Confidence. Low-confidence rules have linked questions.
- [ ] Spot-check 10 random High-confidence rules yourself against the code. If more than one is wrong, tighten `kit/RULES.md` and re-verify.
- [ ] Review packs contain no class or table names.
