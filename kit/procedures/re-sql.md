# /re-sql — SQL inventory: tables, queries and stored procedures used by each component, plus the system-wide view

**ARGUMENTS:** `[<component-folder> | --all] [inventory]`
- **`<component-folder>`:** scan and review one component.
- **`--all`:** scan and review every component in the component map. Each one is resumable.
- **`inventory`:** only rebuild the system-wide inventory from what's already there.

Follow `kit/RULES.md`. Start with §0: resolve `<OUT>` and `<TARGET>`. **Never record credentials, passwords or server names from connection strings.**

## Why two levels

| Level | File | Written by | Use |
|---|---|---|---|
| Facts | `03-capabilities/<c>/_sql-scan.json` and `.md` | `kit/tools/sql_scan.py` (mechanical, exhaustive, repeatable) | Input for the review. Never edited. |
| Meaning | `03-capabilities/<c>/sql-usage.md` | You (this procedure), from `kit/templates/sql-usage.md` | Per component: purpose, entry points, rules, review status |
| System view | `00-overview/sql-inventory.md` and `.csv` | `kit/tools/sql_inventory.py` (generated) | Who touches which object, access through stored procedures, shared writes, dead or undefined objects, cross-database links |

## A. Prepare (first time on a project)

1. **Set the default schema.** `project.md` row `SQL default schema`: `dbo` for MS SQL Server (the default), `(none)` for engines without schemas.
2. **Make sure the database code is scannable.** If stored procedures, views and functions live only in the database (not in the repo), ask the user to export them into `projects/<name>/evidence/database/` and add a component-map row for that folder (type `Database`). Ways to export:
   - an SSDT database project
   - SSMS **Generate Scripts**
   - `sqlpackage /Action:Extract` (then unpack the model)
   - **SQL Agent job scripts and SSIS/SSRS files are useful too:** they contain the batch and report SQL.

## B. Per component

1. **Scan:** `python kit/tools/sql_scan.py <folder>` (or `--all`).
2. **Read `_sql-scan.md`, then create or update `sql-usage.md`** from `kit/templates/sql-usage.md`.
   - **Tables and views:** one row per scanned object, using the scanned name exactly. For each one:
     - confirm the access letters by opening the cited lines
     - add the **business purpose** in glossary terms, the **entry points** (`EP #n` from `_progress.md` or the API catalogue), and the **rules** that use this data (BR IDs)
     - set the **Status**: `Confirmed`, or `False positive` (it stays in the table but is excluded from the inventory)
   - **Add what the scanner can't see:**
     - writes nested inside ORM calls (e.g. creating a child record inside a parent create)
     - writes made by a shared library this component calls
     - tables reached through ORM naming conventions
     - SQL assembled at runtime
     
     Add each as a row with its citation.
   - **Stored procedures:** purpose, which entry points call it, and which rules it implements. If the procedure's definition was scanned, extract its rules into `03-capabilities/database/rules.md` (`BR-DB-…`), following RULES §6.
   - **Dynamic SQL:** review every site. Record what it builds and which objects it can touch. If you can't tell, record that with Low confidence, and raise a question.
   - **Cross-database / linked-server references:** say why each exists. Raise a question if it isn't clear.
3. **Checkpointing:** for components with many objects, save after every 20 rows. On resume, continue from the first scanned object with no row in `sql-usage.md`.

## C. System inventory

1. `python kit/tools/sql_inventory.py`
2. **Turn its findings into issues**, in the relevant `_defects.md` / `_questions.md`:
   - **Tables written by more than one component:** a defect, if it duplicates or splits a business rule.
   - **Defined but never referenced:** a defect ("possible dead object").
   - **Referenced but not defined:** a question ("is the definition outside the repo?"), or export the definitions and re-scan.
   - **Cross-database / linked-server dependencies:** a question if their purpose is unknown.
3. **Final message:**
   - the counts: objects, procedures, shared-write tables, unreviewed usages
   - the top coupling risks
   - the components still unreviewed
