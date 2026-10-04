# /re-review-pack — Build a product-facing review pack (no code jargon) for one process, component or journey, with decision columns to fill in.

**ARGUMENTS:** `<P-NNN | component folder | UJ-… | BJ-NNN or BJ range | web-services business area>` — the text supplied with the command.

Follow `kit/RULES.md`. Start with §0: resolve `<OUT>` and `<TARGET>`.

**Scope:** `ARGUMENTS`

Create `<OUT>/_review/<YYYY-MM-DD>-<scope>.md` for a product reviewer who **does not read code**. Use plain language throughout.

1. **Header:**
   - scope
   - date
   - the source files this pack was built from (the reviewer won't use them, but `/re-apply-review` does)
   - how to fill it in: decision values are **Confirmed / Changed / Rejected (bug) / Obsolete (no longer used) / Unsure**
2. **What this does today:** a summary of at most 10 lines.
   - For a process, include its Mermaid sequence diagram.
   - For a component, list its responsibilities.
   - **For batch jobs:** for each job, say when it runs, which records it picks (in plain words), what it produces, and what happens if it runs twice.
   - **For a web-services business area:** list the operations and which screens use them.
3. **Rules table** in process-step order (or capability order):

   | ID | Rule (as the system behaves today) | Confidence | Decision | Correct wording / comment |
   |---|---|---|---|---|

   - Leave Decision and Comment blank.
   - Low-confidence rows: prefix the rule text with "⚠ Unsure:".
   - Exclude Withdrawn and Superseded items.
4. **Questions for you:** the open questions related to the scope, with an **Answer** column.
5. **Things that look wrong:** the related suspected defects, with a **Decision** column (Confirmed bug / Intended / Won't fix).
6. **Size limit.** Keep each pack to roughly 40 rules or fewer, about a 45-minute session. If the scope is larger, split it into part 1, part 2, and so on.
7. **Set Status to `In review`** for every included rule in its source file. Update the coverage tracker.
