# /re-batch — Phase 2c – inventory nightly batch jobs (schedule, dependencies) and extract each job's input selection, rules, outputs, file layouts and re-run behaviour. Resumable; supports job ranges.

**ARGUMENTS:** `<batch component folder> [inventory | BJ-001..BJ-020 | BJ-007]` — the text supplied with the command.

Follow `kit/RULES.md`. Start with §0: resolve `<OUT>` and `<TARGET>`. Before starting, read `kit/examples/good-vs-bad-rules.md`.
Templates: `kit/templates/batch-job.md`, `file-layout.md`, `capability.md`.

**Arguments:** `ARGUMENTS`. The first word is the batch component; the rest is the scope.
- **No scope:** run the inventory if it isn't done, then extract all unticked jobs.
- **`inventory`:** run the inventory only.
- **A job or range:** extract only those jobs. Use this to split work across sessions or parallel agents.

Folder: `<OUT>/03-capabilities/<folder>/` containing:
- `jobs/BJ-NNN-<name>.md`
- `file-layouts/FL-NNN-<name>.md`
- `batch-schedule.md`
- `capability.md`
- `rules.md` (shared rules only, job number `000`)
- `_progress.md`

## A. Inventory (once)

1. **Find every job:**
   - job/step definitions (Spring Batch, Quartz, Hangfire, cron expressions, scripts, SQL jobs)
   - batch HTTP endpoints called by an external scheduler
   - console/main entry points
   - scheduler config in the repo (crontab, XML/YAML schedules, Control-M / Autosys exports)
   - **If the scheduler lives outside the repo**, say so. Raise a question asking for the schedule export, and infer the order from code and naming meanwhile, at Medium/Low confidence.
2. **Assign IDs up front.** One `BJ-NNN` per job and one `FL-NNN` per file produced or consumed. Pre-assigning IDs lets ranges run in parallel without collisions.
   - Write the checklist to `_progress.md`: ID, job name, entry point `path:line`, files.
3. **Write `batch-schedule.md`:**
   - **Table:** run order, BJ ID, name, schedule/time, depends on, business-day rules, what happens to downstream jobs on failure.
   - **Mermaid flowchart** of the dependency chain for the nightly run.
   - Note the business-date handling: where the "business date" comes from, how it rolls, and holiday handling.
4. **Shared rules.** Shared batch libraries (common selection filters, business-date logic, common writers) get extracted once into `rules.md` as `BR-<PREFIX>-000-NN`.
5. **Update the coverage tracker** (Batch jobs table): one row per job, status `Not started`.

## B. Per job (one at a time, within the scope)

For each unticked job, create `jobs/BJ-NNN-<name>.md` from the template and fill it in.

1. **Business purpose.** State what business outcome the job produces. Infer it from what the job selects and writes, not from the class name alone.
2. **Schedule and triggering:** schedule, entry point, dependencies, parameters, business date.
3. **Input selection.** This is where batch rules hide.
   - Find every query, reader or file read.
   - Translate each WHERE / JOIN / filter condition into business language, e.g. `status IN ('A','S') AND bal < 0 AND last_txn_dt < :bizDate - 30` → "Active or suspended clients with a negative balance and no transactions in the last 30 days".
   - Each meaningful condition becomes a rule. Cite the query `path:line`, whether it's SQL in code, a mapper XML or a stored procedure.
4. **Processing.** Per record or per group:
   - calculations, rounding, FX
   - classification, state changes
   - aggregation, thresholds
   - calls to services
5. **Outputs:**
   - **Table writes:** target entity, and which fields change in business terms. Is it an insert, update, delete or archive?
   - **Files:** create or update `file-layouts/FL-NNN-<name>.md` from the template, including field derivations. If the file goes to a third party, link the `INT-NNN` and add the job to that integration doc.
   - events, emails, reports
6. **Record-level exceptions:** skip-and-log, reject, abort, or route to ops. Also: where failed records go, and who sees them.
7. **Re-run, restart and idempotency:**
   - What happens if it runs twice for the same business date?
   - What happens after it fails half-way?
   - **Possible duplicates or double postings → defect.**
8. **Controls:** counts, totals, trailer checks, completion flags, alerting.
9. **Rules, questions and defects** go **in the job file** (IDs `BR/Q/D-<PREFIX>-<JJJ>-NN`). Check the places listed in RULES §6, and cite tests.
10. **Save, then tick the job** in `_progress.md`. Add glossary terms. If you are running in parallel, write them to `_glossary-candidates.md` instead.

## C. When all jobs are ticked

1. **Write `capability.md`:**
   - purpose: what the nightly batch achieves for the business
   - responsibilities grouped by business area
   - the entry-point table pointing to the job files
   - data touched, and configuration
2. **Update the coverage-tracker rows.** Status `Extracted`.
3. **Final message:**
   - job count by output type (tables / files / both)
   - jobs with re-run risks
   - jobs whose selection logic looks surprising
   - files sent to third parties
   - top questions
   - a reminder to run `/re-verify <OUT>/03-capabilities/<folder>` in a fresh session (or with a range of job files)

If you are running low on context, finish the current job and save. Tell the user to run `/clear` and re-run the command with the same scope; it will resume.
