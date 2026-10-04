# /re-next — Take the next unit of work from the plan and do it

**ARGUMENTS:** optional, one of:
- *(empty)*: the next extraction
- `verify`: the next component that is extracted but not yet verified
- `<component>`: that specific row
- `status`: report only, change nothing

Follow `kit/RULES.md`. Start with §0, and follow §8 and §8a (checkpoints and run bookkeeping).

This is the command to run repeatedly, in as many sessions or windows as you like. Every session claims its own work, so parallel sessions don't collide. If a session dies, the work done so far is on disk, and the next `/re-next` resumes it.

## Steps

1. **Read `<OUT>/_run/plan.md`.** If it doesn't exist, stop and ask for `/re-plan`.
   - With `status`: print counts per status and per wave, active claims, stale claims, failures, and the average duration per size class from `run-log.md`. Then stop.
2. **Resume before starting anything new.** Look for a claim file in `<OUT>/_run/claims/` that this user created earlier and whose component is not finished. If one exists, resume that component.
3. **Otherwise pick a row:**
   - **Default:** the first `Queued` row in the lowest unfinished wave whose dependencies are at least `Extracted`. If dependencies aren't ready, take the next row and note why.
   - **`verify`:** the first `Extracted` row.
   - **Skip** any row that has a claim file younger than **4 hours**. A claim older than that is **stale**: report it, and take it over only if the user agrees or no other work is available.
4. **Claim the row.** Create `<OUT>/_run/claims/<row-id>.claim` containing: who (machine or user name if known), the session start time, the mode (extract or verify), and the target commit.
   - Create it as a **new file**. If it already exists, another session got there first: pick again.
   - Set the row's status to `Extracting` or `Verifying` and fill in `Started`.
   - Append `START <row-id> <mode> <timestamp>` to `run-log.md`.
5. **Do the work.** Run the row's procedure (`kit/procedures/<procedure>.md`) for that component or slice, exactly as written. For `verify`, run `re-verify` on its folder.
   - The procedure checkpoints itself through `_progress.md` (§8), so an interruption loses at most the entry point in progress.
6. **Finish:**
   - Set the status to `Extracted` (or `Verified`), fill in `Finished`, entry points done, rule counts and the commit analysed.
   - Append `DONE <row-id> <mode> <timestamp> <minutes> <entry-points> <rules>` to `run-log.md`.
   - Delete the claim file.
   - **Failure:** if the procedure can't finish (unreadable code, missing access, repeated tool errors), set the status to `Failed` or `Blocked` with a one-line reason. Append `FAIL …` to the log and keep the claim file, so the reason stays visible.
7. **Recommend checkpointing.** Suggest committing the kit repo: `git add projects/<name> && git commit -m "re: <row-id> extracted"`. Only run it if the user has said to auto-commit (see the plan header).
8. **Final message:**
   - what was done, and the counts
   - the remaining Queued rows in this wave, and overall
   - the instruction to start a **fresh session** (`/clear` in Claude Code; a new chat in Copilot) and run `/re-next` again
