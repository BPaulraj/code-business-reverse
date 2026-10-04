# /re-verify — Independent verification pass – re-check extracted rules/steps against the cited code; correct, downgrade or withdraw. Run in a fresh session.

**ARGUMENTS:** `<requirements file or folder, e.g. <OUT>/03-capabilities/cash-service>` — the text supplied with the command.

Follow `kit/RULES.md`. Start with §0: resolve `<OUT>` and `<TARGET>`.

You are an **independent, sceptical reviewer**. You did not write these requirements. Assume about 1 in 5 items is wrong or incomplete, and find them.

**Target:** `ARGUMENTS`

First, check every citation in the target mechanically: does the file exist, is the line range inside it, is the path full rather than a bare file name? Fix or flag these before reading content.

For **every** rule, process step, entity transition or journey step in the target:

1. **Open each cited source.** If a source doesn't exist or points to unrelated code, flag the item.
2. **Check accuracy.** Does the statement match the code exactly?
   - conditions and thresholds
   - comparison boundaries (`>` vs `>=`)
   - values, units, rounding
   - roles, states, time windows
   - exceptions and early returns
3. **Check completeness.** Read about 30 lines around the cited code and up the call chain. Look for conditions, exemptions or configuration that change the behaviour but aren't mentioned.
4. **Check reachability** (RULES §7).
5. **Check language.**
   - Is the statement in business terms, using glossary terms?
   - Is it a single decision?
   - Could product say yes or no to it?
6. **Check confidence.** Does the evidence justify the level given?

**Fix in place:**
- Correct the wording. Add `Verifier YYYY-MM-DD: <what changed>` to the Technical note.
- Adjust confidence.
- Split compound rules into new IDs. Mark the original `Superseded by …`.
- Mark unsupported items `Withdrawn (no supporting code)` and raise a question if relevant.
- Add new defects and questions to the folder's `_defects.md` / `_questions.md`. For batch job files, add them to the job file's own sections instead.
- **Batch jobs, extra checks:**
  - Does the *business* translation of each selection query match the SQL exactly? Pay close attention to NULL handling, date boundaries, status lists, and joins that silently exclude records.
  - Are all outputs and file fields covered?
- **Web services, extra checks:**
  - Is the consumer evidence real?
  - Is the logic type correct?
  - Are the authorisation and data-scoping rules complete?
- **Never** change Status or Product comments.

**Log** to `_verification.md` in the target folder:
- date
- items checked / correct / corrected / downgraded / withdrawn
- a list of the changes with IDs

Update the coverage-tracker row status to `Verified`, but only if every item was checked.
**Final message:** the counts, and the most significant corrections.
