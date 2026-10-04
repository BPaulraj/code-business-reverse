# /re-coverage — Recount everything, refresh the coverage tracker, merge glossary candidates, regenerate consolidated open-questions and defects lists.

**ARGUMENTS:** (none) — the text supplied with the command.

Follow `kit/RULES.md`. Start with §0: resolve `<OUT>` and `<TARGET>`.

1. **Recount from the files.** Don't trust the existing numbers.
   - Per component folder in `<OUT>/03-capabilities/`:
     - entry points found / ticked (`_progress.md`)
     - rules by Confidence and by Status
     - open questions, defects
     - whether `_verification.md` exists
   - **Web-services folders:** endpoints per business area and logic type, plus unused endpoints (from `api-catalogue.md`).
   - **Batch folders:** per job file in `jobs/`, the rules by Confidence and Status, questions, defects, and tick status. Rules, questions and defects *inside job files* count too.
   - Per process in `<OUT>/02-processes/`: step count and the Gaps section.
2. **Rewrite `<OUT>/00-overview/coverage-tracker.md`** with the fresh numbers. Keep the status flow and the last-updated dates.
3. **Merge glossary candidates.**
   - For any `_glossary-candidates.md` anywhere under `<OUT>/`, merge its terms into `00-overview/glossary.md`.
   - De-duplicate and keep all aliases. If two definitions conflict, raise a question.
   - Then empty the candidate file, keeping its header.
4. **Regenerate `<OUT>/06-open-questions.md`** from all `_questions.md` files **and** the Questions sections of batch job files. Group by area, open items first.
5. **Regenerate `<OUT>/07-suspected-defects.md`** from all `_defects.md` files **and** the Suspected defects sections of batch job files. Group by area, open items first.
6. **Batch rules index.** In each batch folder's `rules.md`, keep the shared `000` rules and regenerate an index table of all job rules: ID, job, title, Confidence, Status, with links to the job files.
6a. **SQL inventory:** if any `_sql-scan.json` exists, run `python kit/tools/sql_inventory.py` to regenerate `00-overview/sql-inventory.md` and `.csv`. Report unreviewed usages and shared-write tables.
7. **Consistency checks.** Report each of these:
   - duplicate IDs
   - BR / Q / D references that point to nothing
   - rules without a Source or Confidence
   - **Broken citations:** every `path:line` in Source fields must point to an existing file, with line numbers inside it. Check this mechanically, e.g. extract all `path:line-range` patterns with grep, then test `[ -f path ]` and compare against `wc -l`. Also report citations that use a bare file name instead of the full path.
   - Low-confidence rules without a linked question
   - components in the map with no folder
8. **Final message:**
   - a one-screen status summary
   - consistency problems found
   - the suggested next three actions
