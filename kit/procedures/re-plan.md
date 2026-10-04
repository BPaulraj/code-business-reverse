# /re-plan — Build or refresh the work plan for a large codebase

**ARGUMENTS:** optional. `refresh` re-reads the component map and adds new components without touching the status of existing rows. `waves=<n>` sets the target number of waves.

Follow `kit/RULES.md`. Start with §0: resolve `<OUT>` and `<TARGET>`. Template: `kit/templates/plan.md`.

**Purpose:** turn the component map into an ordered, resumable work queue (`<OUT>/_run/plan.md`), so that 75+ components can be processed over many sessions, by several people or parallel sessions, without losing progress or doing work twice.

## Steps

1. **Read `<OUT>/component-map.md`.** If it is empty or incomplete, stop and ask for `/re-discover` first.
2. **Size each component** cheaply, without reading its logic:
   - entry-point count: route annotations, consumers, jobs, screens (Grep counts only)
   - source line count of production code, excluding tests and generated code
   - a size class: **S** (≤ 10 entry points and ≤ 5k lines), **M** (≤ 40 and ≤ 30k), **L** (larger), **XL** (more than 100 entry points or more than 100k lines). XL components must be split.
3. **Split XL components** into slices, either by sub-package / module, or by entry-point ranges (e.g. `payments-service#1` = controllers A–F). Each slice is its own plan row, with the same prefix and output folder.
4. **Find dependencies** between components from `00-overview/system-context.md` (REST clients, events consumed, shared tables).
5. **Assign waves:**
   - **Wave 0:** database / domain (`/re-domain`), shared libraries
   - **Wave 1…n:** components grouped by **business domain cluster** (e.g. client, cash, stock, payments, reporting). Within a cluster, components with the fewest dependencies come first.
   - **Last waves:** UIs (`/re-ui`), integrations, then processes (`/re-process`)
   - Aim for waves of 5–15 components, so each one can be reviewed and verified as a batch.
   - **Priority override:** if the user names priority processes (e.g. "trade placement"), move the components those processes touch into the earliest waves.
6. **Pick the procedure for each row** by component type: `re-service`, `re-api`, `re-batch`, `re-ui`, `re-integration`, `re-domain`.
7. **Write `<OUT>/_run/plan.md`** from the template, with every row Queued (or keep existing statuses on `refresh`).
   - Create `<OUT>/_run/claims/` (empty, with a `.gitkeep`).
   - Create `<OUT>/_run/run-log.md` if it is missing.
8. **Final message:**
   - waves, with their components and size classes
   - total entry points
   - the time estimate formula from the plan header, once timings exist in the run log
   - next step: `/re-next`
