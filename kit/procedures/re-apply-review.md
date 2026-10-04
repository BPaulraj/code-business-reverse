# /re-apply-review — Apply a completed product review pack back into the requirement files (statuses, corrected wording, answers, defect decisions).

**ARGUMENTS:** `<path to filled review pack in <OUT>/_review/>` — the text supplied with the command.

Follow `kit/RULES.md`. Start with §0: resolve `<OUT>` and `<TARGET>`.

**Review pack:** `ARGUMENTS`

For each row in the pack, update the source file it came from:

1. **Rules:**
   - **Confirmed** → Status `Confirmed`.
   - **Changed** → Status `Changed`. Copy the reviewer's wording into Product comments, prefixed `Product YYYY-MM-DD:`. Keep the original Statement, because it documents as-is behaviour.
     - If the reviewer means the *code* is wrong (desired behaviour differs from actual), also raise a defect: "Code behaviour differs from confirmed requirement".
   - **Rejected (bug)** → Status `Rejected`. Raise a defect with status `Confirmed bug`.
   - **Obsolete** → Status `Obsolete`. Raise a defect: "Candidate for code removal".
   - **Unsure / blank** → back to `Draft`. Raise a question if the comment asks something.
   - Always copy the reviewer comment into Product comments, prefixed with the date.
2. **Questions:** copy the answer and set Status `Answered`.
   - If the answer changes a rule's meaning, add a note to that rule's Product comments.
   - Never rewrite the Statement unless the answer shows the extraction misread the code. In that case, correct it and note `Corrected after product answer Q-…`.
3. **Defects:** copy the decision. If it is **Intended**, create a rule for the behaviour (Status `Confirmed`) and link it.
4. **Mark the pack as applied.** Add `Applied YYYY-MM-DD` to the pack header.
5. **Run the `/re-coverage` procedure** to refresh the tracker and the consolidated lists.

**Final message:** a list of everything that changed, plus any items that need follow-up by engineering.
