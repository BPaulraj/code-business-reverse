# Business Requirements Reverse-Engineering — Rules

These rules apply to every extraction, verification and review task run from this kit repo.
All output goes in `<OUT>/`. Templates are in `kit/templates/`.
Calibration examples are in `kit/examples/`. Read them before your first extraction.

## 0. Project resolution (do this first, every command)

The application being analysed lives **outside** this kit repo. Resolve two locations before doing anything else:

1. **Active project:** read `projects/.active`. It contains one project name, e.g. `stockbroker`. If it is missing, stop and ask the user to run `/re-init <name> <path-to-repo>`.
2. **`<OUT>`** = `projects/<name>/requirements`. All output goes here, and nowhere else.
3. **`<TARGET>`** = the **Target repo** path in `projects/<name>/project.md`. This is the application's code. It is **read-only**:
   - never create, edit or delete files there
   - never run git commands that change it (checkout, commit, stash, branch)
4. If `<TARGET>` can't be read, stop and ask the user to grant read access:
   - **Claude Code:** `/add-dir <TARGET>`, or restart with `claude --add-dir <TARGET>`.
   - **GitHub Copilot (VS Code):** add `<TARGET>` as a second folder in the workspace (see `reverse-kit.code-workspace.example`).

**All `path:line` citations are relative to `<TARGET>`**, e.g. `packages/server/src/modules/trades/tradesRoutes.ts:36`. Every path given in component maps and progress files is relative to `<TARGET>` too.

## 1. Goal

Extract the business requirements that the code implements **today**, written in business language, so the product team can confirm, correct or reject them.
Describe as-is behaviour only. Never invent should-be behaviour.

**Not extracted:**
- business purpose, personas, success metrics
- non-functional targets (performance, accessibility, browser support)

Code can't tell you these. Exception: security and data-integrity behaviour that *is* visible in code (hashing, masking, transactions, permissions) is extracted as rules.

## 2. Non-negotiables

1. **Cite evidence.** Every rule, process step, entity attribute and journey step needs at least one `Source:` with a repo-relative `path:line` or `path:start-end`. If there is no source, it is not a rule: raise a question instead.
   - **Always use the full repo-relative path, every time,** e.g. `services/cash/src/main/java/.../TransferService.java:42`, never just `TransferService.java:42`. Legacy repos often hold several files with the same name in different components, and short names can't be checked mechanically.
2. **Give a confidence level** for every rule:
   - **High**: the logic is explicit in code (a condition, a constraint, a validation that rejects).
   - **Medium**: inferred from naming, tests, comments, or config whose production value is unknown.
   - **Low**: a guess. It must also be raised as a question.
3. **Use business language.** The `Statement` uses glossary terms (`00-overview/glossary.md`). Class, method, table and field names belong only in `Source` and `Technical note`.
4. **Separate three things:**
   - The business rule goes in the rules file.
   - The implementation mechanism (locks, retries, caching, table names) goes in the rule's `Technical note`.
   - Suspicious behaviour (likely bug, dead code, hard-coded client IDs, contradictory copies of a rule) goes in `_defects.md`, linked from the rule.
5. **Never modify application code.** `<TARGET>` is read-only. Write only inside `<OUT>/`.
6. **Never guess silently.** When unsure, lower the confidence and raise a question.
7. **New items are `Draft`.** Only the product team moves an item to Confirmed / Changed / Rejected / Obsolete, via `/re-apply-review`. Never overwrite `Product comments`.
8. **Never renumber or delete IDs.** If an item turns out wrong, mark it `Superseded by <ID>` or `Withdrawn (reason)`.

## 3. IDs

| Kind | Format | Example |
|---|---|---|
| Business rule | `BR-<PREFIX>-NNN` | `BR-CLI-004` |
| Process (end-to-end) | `P-NNN` | `P-001` |
| External integration | `INT-NNN` | `INT-002` |
| User journey | `UJ-FO-NNN` / `UJ-BO-NNN` | `UJ-FO-007` |
| Entity | `ENT-<Name>` | `ENT-Client` |
| Open question | `Q-<PREFIX>-NNN` | `Q-CSH-012` |
| Suspected defect | `D-<PREFIX>-NNN` | `D-STK-003` |
| Batch job | `BJ-NNN` | `BJ-012` |
| File layout | `FL-NNN` | `FL-004` |
| Rule / question / defect **inside a batch job** | `BR-<PREFIX>-<JJJ>-NN` / `Q-…` / `D-…` | `BR-BAT-012-03` |
| Rule shared by many batch jobs | `BR-<PREFIX>-000-NN` | `BR-BAT-000-02` |

- **Batch job and file-layout IDs** are assigned up front during the batch inventory, so parallel extraction of job ranges never collides.
- **Rules inside a batch job** are numbered per job (`JJJ` = the job number).

- Component prefixes are listed in `<OUT>/component-map.md`.
- Folder-level prefixes: `DOM` (01-domain), `PRC` (02-processes), `INT` (04-integrations), `FO` / `BO` (05-user-journeys).
- **Next number** = the highest existing number for that prefix + 1. Grep before assigning.

## 4. Where questions, defects and glossary candidates go

- Write questions to the `_questions.md` of the folder you are working in, and defects to its `_defects.md`. That is one of:
  - the component folder under `03-capabilities/`
  - `01-domain/`
  - `02-processes/`
  - `04-integrations/`
  - `05-user-journeys/<front-office|back-office>/`
- **Exception: batch jobs.** Each `jobs/BJ-NNN-*.md` file holds its own rules, questions and defects in its own sections.
- The consolidated lists `06-open-questions.md` and `07-suspected-defects.md` are **generated** by `/re-coverage`. Don't edit them by hand.
- **Glossary:** in a normal single session, edit `00-overview/glossary.md` directly. When running as a parallel subagent, write additions to `_glossary-candidates.md` in your own folder instead. `/re-coverage` merges them.

## 5. What counts as a business rule

**A rule is** something a business person cares about, such as:
- a condition, constraint or calculation
- a state transition or a permission
- a limit, a time window or cut-off, a required order of steps
- a side effect

**A rule is not:**
- logging
- defensive null checks
- framework plumbing
- technical retries (unless the business can see them)
- pure DTO mapping

**Test:** could product, operations or compliance answer "yes, that's right" or "no, that's wrong" to this statement? If yes, it is a rule.

**One rule = one decision.** Split statements joined by "and".

## 6. Where rules hide (check all)

- **Entry points:**
  - API endpoints and controllers
  - message/queue consumers
  - scheduled jobs and batch processes
  - file watchers and inbound file processors
  - UI event handlers
- **Validation:**
  - annotations and validator classes
  - `if … throw / return error` and guard clauses
  - form schemas
- **State:**
  - status enums and columns
  - *every* place a status changes, which gives the allowed transitions
- **Calculations:**
  - amounts, fees, rounding and precision, FX
  - dates: cut-offs, business days, holiday calendars, time zones
- **Configuration:**
  - properties / yaml / json / env files and feature flags
  - reference-data tables
  - Record the key and the value found in the repo. If the production value is unknown, raise a question.
- **Database:**
  - constraints, triggers, stored procedures, views, defaults
  - reference/seed data in migrations
- **Queries (SQL in code, ORM criteria, mapper XML, stored-procedure calls):**
  - WHERE / JOIN / filter conditions decide *which* clients, accounts or trades are affected. Translate each meaningful condition into a business rule.
  - This matters most in web services that access the DB directly, and in batch jobs.
- **Web services (API layer):**
  - authorisation per endpoint and data scoping (who may see or change what)
  - request validation
  - orchestration order and partial-failure handling
  - response filtering
  - endpoints with no consumer (possible dead code)
- **Batch jobs:**
  - input selection criteria
  - business-date and holiday handling
  - per-record processing
  - output tables and files, with field derivations
  - record-level exception handling
  - re-run / idempotency behaviour
  - job dependencies
  - control totals
- **Messages:**
  - error messages and i18n/resource files. The text often states the rule outright.
- **Tests:**
  - test names and assertions are strong evidence of intent and can raise confidence.
- **Special cases:**
  - `if clientId == …`, magic numbers, hard-coded dates
  - Record the rule *and* raise a defect.
- **Compensation and rollback:**
  - what happens when step N fails after step N-1 has already succeeded.
  - **Side effects after the main transaction commits:** notifications, events, files or calls made *after* the commit. If one fails, the user gets an error for an operation that actually succeeded, and a retry duplicates it. Raise a defect.
  - **Duplicate-submission exposure:** is there an idempotency key, a lock (e.g. client lock), or a uniqueness check on the server? A disabled UI button alone doesn't count, because API callers and network retries bypass it.
- **Data protection:**
  - what is hashed, masked, encrypted, never stored, or never returned in responses (passwords, card and account numbers, personal data)
  - These are reviewable rules, not just technical notes.
- **Duplicates:**
  - the same check in UI, service and DB. Record every source.
  - If the copies differ, raise a defect.

## 6a. Shared and duplicated logic

- **Shared libraries called by two or more components** get their own row in the component map, their own folder and their own prefix (e.g. `core-library`, `LIB`). Rules are recorded there once. Callers reference the LIB IDs instead of re-extracting them.
- **Logic that was copy-pasted between components** (e.g. two channels with the same trade code):
  - Record each rule **once**, under the component that is primary or older.
  - In the other component's `rules.md`, add a **"Duplicated rules"** table: rule ID | where it is implemented again (full path) | difference.
  - Write rules only for the behaviour that differs.
  - Raise one defect for the duplication itself, because every change must be made twice and the copies drift.

## 7. Dead code and reachability

Before writing a rule, check that its code path is reachable:
- Is the endpoint called by a UI, another service or a route?
- Is the job scheduled?
- Is the flag switched on?

If reachability is unknown, confidence is at most **Medium** and you add "Reachability unconfirmed" to the technical note. If the path is clearly unreachable, raise a defect ("possible dead code") instead of a rule.

## 8. Checkpoints, resume and context discipline

Assume any session can stop at any moment (crash, timeout, network loss, quota, laptop closed). **Everything of value must already be on disk.**

- An **entry point** is any one of: an API endpoint, an event consumer, a scheduled job, a batch job, a file processor, or a UI screen.
- Work **one entry point at a time**. Don't hold a whole service in memory.
- **Checkpoint unit = one entry point.** For each entry point, in this order:
  1. Write all its rules, questions and defects. Every rule's `Used in` names the entry point number (e.g. `EP #7`).
  2. **Then** tick it in `_progress.md`.
  A stop can therefore lose at most the entry point in progress.
- **`_progress.md` header:** record the target commit, the date started, and the procedure used. If the target commit in `project.md` has changed since, flag it before continuing.
- **Resume check:** on resume, read `_progress.md`, then check the first unticked entry point:
  - If rules citing `EP #n` already exist in `rules.md`, the previous session stopped between writing and ticking. Review those rules, tick the entry point and move on. Don't duplicate them.
  - If `rules.md` ends mid-rule (missing fields), complete or remove that partial rule before continuing.
- **Context discipline:** locate code with Grep/Glob and read targeted line ranges. Never read whole directories or whole large files.
- **Calls into another component:** record the dependency and reference that component. Don't extract its rules from here.
- **Fresh context per component.** After finishing a component (or about 25 entry points of a large one), stop and recommend a fresh session. `_progress.md` makes the next session pick up exactly where this one stopped.

## 8a. Run bookkeeping (large codebases)

If `<OUT>/_run/plan.md` exists, every extraction or verification procedure also:
- **On start:** makes sure the row is claimed (`_run/claims/<row-id>.claim`). `/re-next` does this; if the procedure is run directly, create the claim. Sets the status to `Extracting` / `Verifying` and appends `START` to `_run/run-log.md`.
- **On finish:** updates the row (status, finished time, entry points done, rules, commit), appends `DONE … <minutes> <entry-points> <rules>` to the log, and deletes the claim.
- **On failure:** sets the status to `Failed` / `Blocked` with a reason, appends `FAIL`, and keeps the claim.

**Never edit another session's claimed row.** `_run/run-log.md` is append-only. It gives the timings used to estimate the remaining effort.

## 9. Output locations

| What | Where |
|---|---|
| Component inventory | `<OUT>/component-map.md` |
| SQL usage per component (facts / reviewed) | `<OUT>/03-capabilities/<component>/_sql-scan.json` + `.md` (generated) / `sql-usage.md` |
| System-wide SQL inventory | `<OUT>/00-overview/sql-inventory.md` + `.csv` (generated by `kit/tools/sql_inventory.py`) |
| Work plan, claims, run log | `<OUT>/_run/plan.md`, `<OUT>/_run/claims/`, `<OUT>/_run/run-log.md` |
| System context, glossary, coverage | `<OUT>/00-overview/` |
| Entities and lifecycles | `<OUT>/01-domain/entities/<entity>.md` |
| End-to-end processes | `<OUT>/02-processes/P-NNN-<name>.md` |
| Per-component capability and rules | `<OUT>/03-capabilities/<component>/capability.md`, `rules.md`, `_progress.md`, `_questions.md`, `_defects.md`, `_verification.md` |
| Web-services endpoint catalogue | `<OUT>/03-capabilities/<web-services folder>/api-catalogue.md` |
| Batch jobs | `<OUT>/03-capabilities/<batch folder>/jobs/BJ-NNN-<name>.md`, `batch-schedule.md` |
| File layouts (files produced or consumed) | `<OUT>/03-capabilities/<producing component>/file-layouts/FL-NNN-<name>.md` |
| External counterparties | `<OUT>/04-integrations/INT-NNN-<counterparty>.md` |
| User journeys, roles | `<OUT>/05-user-journeys/<front-office or back-office>/` |
| Review packs for product | `<OUT>/_review/` |

Component folder names are kebab-case, as in the component map (e.g. `client-service`).

## 10. Definition of done for a component

- [ ] Every entry point in `_progress.md` is ticked.
- [ ] `capability.md` is complete.
- [ ] Every rule has a Source and a Confidence.
- [ ] Glossary terms are added.
- [ ] The coverage-tracker row is updated (status `Extracted`).
- [ ] A verification pass has been run (`/re-verify`), and the tracker status is `Verified`.
