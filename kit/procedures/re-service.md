# /re-service — Phase 2 – extract capability and business rules from ONE back-end component (microservice, connectivity adapter or back-end of a website). Resumable.

**ARGUMENTS:** `<component name or folder from component-map>` — the text supplied with the command.

Follow `kit/RULES.md`. Start with §0: resolve `<OUT>` and `<TARGET>`. Before starting, read `kit/examples/good-vs-bad-rules.md`.
Templates: `kit/templates/capability.md`, `business-rule.md`, `questions-and-defects.md`.

**Component:** `ARGUMENTS`

1. **Look up the component** in `<OUT>/component-map.md` to get its repo path, folder and prefix. If it's missing, stop and ask the user to run `/re-discover` or to add the row.
   - **Type "API layer"?** Use `/re-api` instead.
   - **Type "Batch"?** Use `/re-batch` instead.
   Tell the user, and follow that command's procedure.
2. **Prepare the folder** `<OUT>/03-capabilities/<folder>/`:
   - If `_progress.md` exists, read it and **resume from the first unticked entry point**. Also read the existing `rules.md` so you don't duplicate rules and you continue the numbering.
   - Otherwise create `_progress.md`, `rules.md`, `_questions.md` and `_defects.md` from the templates.
3. **Enumerate entry points.** If `_progress.md` is new, list every:
   - API endpoint
   - message/event consumer
   - scheduled job
   - inbound file processor
   - public method called by other components through a shared library
   Write them as a checklist in `_progress.md` with `path:line`. Set the coverage-tracker row to `In progress` with the entry-point count.
4. **For each unticked entry point, one at a time:**
   1. Trace the path from the entry point to its outcome: response, persisted state, published event, outbound call. Follow calls into shared libraries. When you reach a call to *another* component, record the dependency and stop there.
   2. Record rules using the template. Each rule is atomic, written in business language, with Source(s) and Confidence. Check all the places listed in RULES §6. Pay special attention to:
      - validations
      - status changes
      - calculations
      - config values
      - error-message text
      - special cases
      - what happens on failure and how it is compensated
   3. Find the tests for this entry point. Cite them as evidence and adjust confidence.
   4. Check reachability (RULES §7).
   5. **Save immediately:**
      - append the rules to `rules.md` and update its summary table
      - tick the entry point in `_progress.md`
      - add glossary terms
      - append questions and defects
5. **When every entry point is ticked**, write `capability.md`:
   - purpose and responsibilities
   - entry-point table
   - data, dependencies, events and business-relevant configuration
6. **Update the coverage-tracker row:** counts by confidence, open questions, defects, status `Extracted`.
7. **Final message:**
   - counts
   - the five findings most likely to surprise the product team
   - the questions most worth asking
   - a reminder to run `/re-verify <OUT>/03-capabilities/<folder>` in a **fresh session** (`/clear`)

If you are running low on context, finish the current entry point and save. Then tell the user to run `/clear` and the same command again; it will resume.
