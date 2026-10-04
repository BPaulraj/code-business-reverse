# /re-publish — Compile the stakeholder Business Requirements Specification from the working files

**ARGUMENTS:** optional, in any order:
- `draft` (default: include Draft and In-review items, clearly marked) or `baseline` (include only Confirmed/Changed items; everything else is listed as pending)
- `docx`, `pdf` or `both`: overrides the project's **Output formats** preference for this run

Follow `kit/RULES.md`. Start with §0: resolve `<OUT>` and `<TARGET>`.

## What this produces, and why

`<OUT>/` holds **working files**. They are organised by component, carry code citations, and serve the extraction and review team.
Stakeholders need **one document**:
- organised by **business capability and process**, not by code component
- in plain language, with no file paths, class or table names
- showing what has been confirmed by product and what hasn't

Write it to `projects/<name>/deliverables/Business-Requirements-Specification.md`.
- **The document is generated. Never hand-edit it.** Fix the working files and re-run `/re-publish`.
- **Keep each requirement's ID** (e.g. BR-WEB-027), so anyone can trace it back to the working files and the code.

## Inputs (read in this order; don't read source code)

1. `projects/<name>/project.md`: target and commit
2. `<OUT>/00-overview/`: system context, glossary, coverage tracker
3. `<OUT>/01-domain/entities/`
4. `<OUT>/02-processes/`
5. `<OUT>/03-capabilities/*/rules.md` and `capability.md`, plus `api-catalogue.md` (business columns only)
6. `<OUT>/04-integrations/`, `<OUT>/05-user-journeys/`
7. `<OUT>/06-open-questions.md`, `<OUT>/07-suspected-defects.md`, applied review packs in `<OUT>/_review/`

## Document structure

1. **Document control:** title, version (increment each run), date, target system and commit, generation mode (draft or baseline), and the confirmation status (counts of Confirmed / Changed / In review / Draft, with % confirmed). Below it, a banner stating that unconfirmed requirements describe current behaviour and not yet agreed intent.
2. **Executive summary:** at most 10 lines covering what the product does, for whom, through which channels, and the headline risks and open decisions.
3. **Product overview and scope:**
   - purpose (inferred, marked as such)
   - channels (e.g. web portal, public API, batch)
   - in scope, and **not present** (from the "Not present" rows and the gaps)
   - a one-diagram context view with no technical labels
4. **Actors and roles:** who uses the system and what each role may do.
5. **Business glossary:** from the glossary, with code aliases removed.
6. **Business information model:** for each entity, a definition, its key attributes in business terms, and its lifecycle (Mermaid state diagram).
7. **Business processes:** for each P-NNN, the goal, trigger, a numbered narrative, alternative and failure outcomes **as the business sees them**, and the sequence diagram with component names replaced by business roles where possible ("Client", "Portal", "Platform").
8. **Functional requirements by business capability.** Regroup the rules from all components into capabilities: account and access, funding, market data, trading, portfolio, documents, notifications, and so on, adapted to the system. For each capability, one table:

   | ID | Requirement (plain language) | Channel(s) | Status |

   - **Merge duplicates:** a rule implemented in several components appears **once**. List every channel that applies it.
   - Mark Low-confidence items "⚠ unverified".
9. **Channel differences:** what one channel offers or enforces differently from another (e.g. portal vs API).
10. **Data protection and control behaviours:** hashing, masking, atomicity, access scoping.
11. **Known issues and risks:** suspected defects rewritten as business impact, grouped as High / Medium / Low impact, each with its ID and decision status. These are clearly separated from requirements.
12. **Open decisions for product:** the open questions, grouped by capability.
13. **Appendices:**
    - **A. Traceability matrix:** requirement ID → working file → number of code citations. No paths.
    - **B. Coverage:** components analysed and verified.
    - **C. How to give feedback:** review packs, decision values.
    - **D. Data (if `00-overview/sql-inventory.md` exists):** databases, number of tables and procedures, and the tables written by more than one component (as business risk), linking to the inventory. No SQL text.

## Rules for writing

- **No code vocabulary:** no file paths, class names, table names or HTTP verbs, except API operation names in the API channel section, phrased as capabilities.
- **Keep wording faithful.** Rephrase for readability only. Never change a rule's meaning, never strengthen or weaken it, never drop its conditions or exceptions.
- **`baseline` mode:** section 8 contains only Confirmed/Changed rules. For Changed rules, use the product-approved wording from Product comments. Every other rule goes into a "Pending confirmation" list (ID and title).
- **Completeness check (mandatory before finishing):** extract every `### BR-…` ID from the working files, and every BR ID in the document. Every non-withdrawn rule must appear in the document (in `draft` mode in section 8 or 10; in `baseline` mode in section 8 or the pending list). Add any that are missing. Do the same for D- and Q- IDs (sections 11 and 12).
- **Export:** once the Markdown is written and passes the completeness check, produce the preferred formats. Formats come from the arguments, otherwise from **Output formats** in `project.md` (if unset, ask once and record the answer). Follow `kit/procedures/re-export.md` for the Markdown file. Markdown is always produced; it is the source.
- **Wiki:** read `Wiki publishing` in `project.md`.
  - **`auto`:** follow `kit/procedures/re-wiki.md` with `publish` (only changed pages are sent).
  - **`on-request`:** don't upload; end with "run `/re-wiki` to update the ADO wiki".
  - **`off` or missing:** don't upload and don't mention it, unless the user asked about the wiki.
- **Final message:** the document path(s), its version, its confirmation %, the number of requirements, issues and open decisions, the completeness check result, and the export result (files, diagrams rendered).
