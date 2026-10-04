# /re-ui — Phase 4 – extract user journeys, screen validations and role permissions from a website (front-office or back-office). Resumable.

**ARGUMENTS:** `<front-end | back-office>` — the text supplied with the command.

Follow `kit/RULES.md`. Start with §0: resolve `<OUT>` and `<TARGET>`. Templates: `kit/templates/user-journey.md`, `business-rule.md`.

**Application:** `ARGUMENTS`. Resolve the repo path and prefix (`FO` or `BO`) from `<OUT>/component-map.md`.
- Output folder: `<OUT>/05-user-journeys/<front-office|back-office>/`
- UI-level rules go to `<OUT>/03-capabilities/<folder>/rules.md`. Progress is tracked in that folder's `_progress.md`.

1. **Inventory screens:**
   - routes / pages / menus / navigation config
   - their role/permission guards
   Write them as a checklist in `_progress.md`. If `_progress.md` already exists, resume from the first unticked screen.
2. **Group screens into user journeys** by user goal (e.g. "Place a buy order", "Approve a cash withdrawal"). One `UJ-<FO|BO>-NNN-<name>.md` per journey.
3. **For each journey, one at a time:**
   - steps: screen, user action, system response, and the backend endpoint called
     - Usually the endpoint is in the web-services layer: link to its row in `api-catalogue.md`.
     - Otherwise link to the capability entry point of the component that serves it.
   - **Validations shown to the user:**
     - field rules (required, format, min/max, cross-field)
     - enable/disable and visibility logic
     - confirmation dialogs
     - the exact message texts (check i18n/resource files)
     Each validation becomes a rule with the FO/BO prefix.
   - **Duplicates:** if a UI rule also exists server-side, reference the server rule. If the two differ (different limits or conditions), raise a defect.
   - **Money-moving and irreversible actions** (trade, payment, transfer, cancel, delete): record whether there is an explicit review/confirm step and whether the button is disabled while processing. Raise a question if there is no confirmation.
   - Save, then tick the screens in `_progress.md`.
4. **Back-office only.** Pay special attention to:
   - maker-checker / approval flows
   - manual overrides and corrections
   - limits per role
   - audit trails
   - reports: what they show and their filter rules
   - batch operations screens: manual job triggers, re-runs, viewing failed records, uploading or downloading batch files. Link them to the `BJ-NNN` job files.
5. **Write `roles-and-permissions.md`** in the output folder: a matrix of role × action, with sources.
6. **Update the coverage tracker.** Final message: the journey list, notable validations, UI/server mismatches.
