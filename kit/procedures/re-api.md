# /re-api — Phase 2b – catalogue the web-services (REST API) layer and extract its business rules – consumers, downstream targets, auth, validations, direct DB logic. Resumable.

**ARGUMENTS:** `<web-services component name or folder from component-map>` — the text supplied with the command.

Follow `kit/RULES.md`. Start with §0: resolve `<OUT>` and `<TARGET>`. Before starting, read `kit/examples/good-vs-bad-rules.md`.
Templates: `kit/templates/api-catalogue.md`, `capability.md`, `business-rule.md`, `questions-and-defects.md`.

**Component:** `ARGUMENTS`

The web-services layer connects the front-end to the back-office and/or straight to the database. Each endpoint needs to answer four questions:
- **Who** calls it?
- **What** business operation is it?
- **Where** does it go next?
- **Which rules** does it apply on the way?

1. **Look up the component** in `<OUT>/component-map.md` to get its path, folder and prefix. If it's missing, stop and ask for `/re-discover`.
2. **Prepare the folder** `<OUT>/03-capabilities/<folder>/`. If `_progress.md` exists, resume from the first unticked endpoint and continue the existing rule numbering.
3. **Inventory the endpoints** (only if `_progress.md` is new):
   - Find every route: controller/route annotations, route tables, gateway config, OpenAPI/Swagger files, WSDL if SOAP also exists.
   - Group them by **business area**, e.g. Clients, Trading, Cash, Stock, Reference data, Reports.
   - Write the checklist to `_progress.md` with `path:line`, and create `api-catalogue.md` from the template with one row per endpoint (Consumers, Downstream etc. still blank).
   - Set the coverage-tracker row to `In progress`.
4. **Extract cross-cutting behaviour once, before the endpoints.** Write it to the catalogue's Cross-cutting section, with rules where relevant:
   - authentication and session handling
   - authorisation model (roles, entitlements, data scoping such as "a user sees only their own clients")
   - common validation, filters / middleware / interceptors
   - error-message mapping
   - audit logging
   - idempotency
5. **For each unticked endpoint, one at a time:**
   1. **Consumers:** Grep the front-end, back-office, other services and batch jobs for the path (or for the generated client method). Record which screens or components call it.
      - **No consumer found** → raise a defect "possible unused endpoint". Mark any rules from it with "Reachability unconfirmed".
   2. **Downstream:** trace to the outcome.
      - **Calls to back-office or microservices:** record the target. Don't extract the target's rules.
      - **Direct DB access** (SQL, ORM queries, stored-procedure calls): the selection criteria, the updates and any procedure logic **are business rules**. Extract them here. For stored-procedure internals, reference the `database` component.
   3. **Set the Logic type:** Pass-through / Orchestration / Business logic / Data query.
   4. **Rules:**
      - request validation
      - authorisation per endpoint and data scoping
      - calculations and defaults
      - orchestration order, and what happens if a downstream call fails part-way (compensation or none)
      - response filtering (what data is hidden from whom)
      - error-message texts
   5. **Duplicates:** if the same check exists in the UI or in a downstream service, record every source. If the copies differ, raise a defect.
   6. **Tests:** cite controller/integration tests as evidence.
   7. **Save immediately:**
      - fill the catalogue row
      - append the rules to `rules.md`
      - tick the endpoint in `_progress.md`
      - add glossary terms, questions and defects
6. **When every endpoint is ticked**, write `capability.md`. Put each business area as a responsibility, and point to `api-catalogue.md` as the entry-point table.
7. **Update the coverage-tracker row:** endpoints found/done, rules by confidence, unused endpoints, status `Extracted`.
8. **Final message:**
   - counts per logic type
   - unused endpoints
   - endpoints that bypass back-office and write to the DB directly (high-interest for product)
   - top questions
   - a reminder to run `/re-verify <OUT>/03-capabilities/<folder>` in a fresh session

If you are running low on context, finish the current endpoint and save. Tell the user to run `/clear` and re-run the command; it will resume.
