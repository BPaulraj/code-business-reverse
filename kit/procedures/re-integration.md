# /re-integration — Phase 3 – document what is exchanged with one third-party system (contract, timing, failure handling, reconciliation).

**ARGUMENTS:** `<counterparty name or INT-NNN, or connectivity component folder>` — the text supplied with the command.

Follow `kit/RULES.md`. Start with §0: resolve `<OUT>` and `<TARGET>`. Template: `kit/templates/integration.md`.

**Target:** `ARGUMENTS`

1. **Resolve the counterparty and its connectivity component** from the External systems table in `<OUT>/component-map.md`. If the connectivity component hasn't been extracted yet (no `rules.md` in its folder), run the `/re-service` procedure for it first. Its internal rules belong there, with its own prefix.
2. **Create or update `<OUT>/04-integrations/INT-NNN-<counterparty>.md`:**
   - **Business purpose**, and the business processes that depend on this integration.
   - **Direction, protocol and format, trigger or schedule.** Look for cron expressions, listeners, file paths, endpoint config.
   - **Message/file types** and their business meaning.
   - **Business-relevant field mapping.** Include only fields that carry business meaning or get transformed: code mappings, enrichment, defaulting, rounding, date/time-zone conversion.
   - **Acknowledgements, rejections, timeouts, duplicates.** What we do in each case, and what the business sees.
   - **Reconciliation and break handling.**
   - **Links** to the BR IDs in the connectivity component's `rules.md`.
3. **Questions** go to `<OUT>/04-integrations/_questions.md`. Always ask about anything that depends on the counterparty's behaviour, which the code can't show (e.g. "Do they resend on NACK?").
4. **Defects** go to `<OUT>/04-integrations/_defects.md`. Examples: silent swallowing of errors, missing retries, unmapped codes that fall to a default.
5. **Update the coverage tracker.** Final message: a summary and the top questions.
