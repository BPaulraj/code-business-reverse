# /re-domain — Phase 1 – extract business entities, lifecycles, DB-resident rules and glossary from the shared database assets.

**ARGUMENTS:** `[optional: path to DB assets]` — the text supplied with the command.

Follow `kit/RULES.md`. Start with §0: resolve `<OUT>` and `<TARGET>`. Templates: `kit/templates/entity.md`, `business-rule.md`.

**Task:** build the domain model from the shared database. DB assets: `ARGUMENTS`, or the `database` row in `<OUT>/component-map.md`.

1. **Locate DB assets:**
   - migrations / DDL
   - ORM entity classes
   - stored procedures, functions, triggers, views
   - seed / reference data
   If DB objects live outside the repo, say so in the final message and continue with ORM mappings.
2. **Pick the business entities.** Ignore join, audit, log, staging and technical tables, but list them under "Technical tables" in `<OUT>/03-capabilities/database/capability.md`.
3. **For each business entity**, create `<OUT>/01-domain/entities/<entity>.md` from the template:
   - definition, identifiers, key attributes with business meaning
   - relationships
   - **Lifecycle:**
     - Find the status/state column or enum.
     - Grep the whole of `<TARGET>` for every place it is set.
     - Derive the transition table and cite each setter.
     - A transition found only in DB scripts or batch jobs counts too.
   - reference data values that define business categories
   Write each entity file as soon as it is done.
4. **DB-resident business logic** (constraints, triggers, stored procedures, views that encode rules) becomes rules with the `DB` prefix in `<OUT>/03-capabilities/database/rules.md`. Use `capability.md` for a description of what logic lives in the DB.
5. **Update `<OUT>/00-overview/glossary.md`.** Map each term to its table, column and enum aliases.
6. Questions go to `<OUT>/01-domain/_questions.md`, defects to `<OUT>/01-domain/_defects.md`. Examples: orphan tables, status values never set, contradictory constraints.
7. **Update the coverage-tracker row** for the database.
8. **Final message:** entity count, a list of lifecycles found, the top questions for product.
