# /re-discover — Phase 0 – inventory the target application repo; fill component map, system context, coverage tracker and seed glossary. No rule extraction.

**ARGUMENTS:** `[optional: sub-path to limit discovery]` — the text supplied with the command.

Follow `kit/RULES.md`. Start with §0: resolve `<OUT>` and `<TARGET>`.

**Task:** build an inventory of `<TARGET>` (or of `<TARGET>/ARGUMENTS` if a sub-path is given). **Do not extract business rules yet.**

**Large repos (more than about 20 deployable units): discover in stages so it survives interruptions.**
- First, only list the top-level folders and candidate components. Write them as a checklist to `<OUT>/_run/discovery-progress.md`.
- Then process them one top-level folder (or about 10 components) at a time. Append their rows to `component-map.md` and tick them, before moving on.
- On resume, read `discovery-progress.md` and continue from the first unticked item.
- Steps 4–6 (system context, coverage, glossary) run once every folder is ticked.
- After discovery, the next step is `/re-plan`, not a manual extraction order.

1. **Map the structure.** Glob two or three levels deep. Identify every deployable or meaningful unit:
   - websites
   - **web services / REST API layer** (the layer between the front-end and the back-office/DB)
   - microservices
   - **batch applications**: nightly jobs, job definitions, batch endpoints called by a scheduler, scheduler configs (crontab, Quartz, Spring Batch, Control-M/Autosys exports, Windows Task Scheduler XML)
   - connectivity / integration adapters
   - database assets (migrations, DDL, stored procedures, triggers, seed/reference data, ORM mappings)
   - batch / scheduled jobs
   - shared libraries
   - infrastructure config that reveals wiring (docker-compose, k8s manifests, gateway routes)
2. **For each component, find:**
   - **Tech stack:** language, framework, build file.
   - **How it is invoked:** REST controllers, message consumers, schedulers, file watchers, UI routes.
   - **What it talks to:** HTTP client base URLs, queue/topic names, connection-string keys, external hostnames, SFTP paths. Read config files and client classes.
   - **Rough number of entry points.** Count them with Grep, e.g. route annotations, consumer annotations, cron expressions, job definitions, UI route definitions.
   - **Web services:** does it call the back-office, microservices, the database directly, or a mix?
   - **Batch:** is the scheduler in the repo or external? Roughly how many jobs? Which output folders and file patterns appear?
3. **Update `<OUT>/component-map.md`:**
   - One row per component.
   - Kebab-case folder name and a 2–4 letter prefix. Keep any prefixes that already exist.
   - Fill the External systems table: one `INT-NNN` per third party.
4. **Write `<OUT>/00-overview/system-context.md`:**
   - one-line business purpose per component (Medium confidence unless obvious)
   - a Mermaid flowchart of the real components, the DB and the third parties
   - an interaction table with evidence (`path:line`)
   - candidate end-to-end processes with their likely entry points
5. **Update `<OUT>/00-overview/coverage-tracker.md`.** One row per component: entry points found / 0 done, status `Not started`.
6. **Seed `<OUT>/00-overview/glossary.md`** with about 30 domain terms that recur in class, table and endpoint names. Give each an alias and a source. The definition is `TBC` unless the code makes it obvious.
7. **Final message:**
   - a short inventory table
   - a recommended extraction order:
     1. database/domain
     2. microservices, from fewest to most dependencies (`/re-service`)
     3. web services (`/re-api`)
     4. batch jobs (`/re-batch`)
     5. connectivity
     6. UIs
     7. processes, including a scheduled "end-of-day" process for the nightly batch
   - anything surprising, e.g. undocumented components, dead modules, multiple databases
