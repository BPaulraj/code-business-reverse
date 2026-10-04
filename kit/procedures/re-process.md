# /re-process — Phase 5 – trace one end-to-end business process across UI, services, integrations and DB, linking existing rules. This is what product reviews first.

**ARGUMENTS:** `<process name, e.g. 'trade placement', or an entry point>` — the text supplied with the command.

Follow `kit/RULES.md`. Start with §0: resolve `<OUT>` and `<TARGET>`. Template: `kit/templates/process.md`.

**Process:** `ARGUMENTS`

1. **Find the starting point:**
   - Check `<OUT>/00-overview/system-context.md` (candidate processes) and the existing `<OUT>/02-processes/` files.
   - If a file for this process exists, update it. Otherwise assign the next `P-NNN`.
   - Identify the trigger: a UI action, inbound message, schedule or file.
2. **Trace the flow end to end** from the trigger, in execution order, across components:
   - UI → web services → back-office / services → events → integrations → DB
   - For each step, open the code (`path:line`) and note which component acts, what changes in business terms, and which rules apply.
   - **Large systems: work from the summary layer first.** For each component on the path, read its `capability.md` (entry points, dependencies, events) and `rules.md` summary table. Open source code **only** to confirm the hand-offs between components: the outbound call, the event published or consumed, the shared table. Don't re-read whole services. This keeps a 10-service process within one session.
   - **Overnight continuation:** check whether nightly batch jobs pick up records this process created (e.g. settlement, interest, statements, files to third parties). List them in the "Overnight continuation" section.
   - **Scheduled processes** (e.g. "End-of-day processing"): the trigger is the scheduler and the steps are the `BJ-NNN` jobs in `batch-schedule.md` order. For each step, include the job's purpose, its key rules, its outputs, and what happens to later jobs if it fails.
3. **Link, don't duplicate.** Reference existing BR IDs from the components' `rules.md`.
   - A rule that isn't extracted yet goes into the owning component's `rules.md`, with the next ID and Status Draft.
   - A component that hasn't been extracted at all goes under **Gaps**.
4. **For every step, ask "what if this fails?"**
   - What state is left behind by the earlier steps (e.g. cash already moved but the stock debit failed)?
   - Is there compensation, a retry, a manual ops queue, or nothing?
   - Missing or partial compensation is a defect.
5. **Concurrency and timing:**
   - double submission and locks (e.g. the client lock)
   - ordering of events
   - timeouts, cut-offs, end-of-day and batch interactions
6. **Draw a Mermaid sequence diagram** that uses the real component names.
7. **Save `<OUT>/02-processes/P-NNN-<name>.md`.** Questions go to `02-processes/_questions.md`, defects to `02-processes/_defects.md`.
8. **Update the Processes table** in the coverage tracker.
9. **Final message:** a five-line plain-English summary of the process, its gaps, and its key questions. Suggest `/re-review-pack P-NNN` once the involved components are verified.
