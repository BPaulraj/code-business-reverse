# BJ-NNN — <Job name in business words>

**Status:** Draft · **Component:** <batch component> · **Prefix:** `<PREFIX>` · **Last extracted:** <YYYY-MM-DD>

<!--
A batch job file is self-contained. Its rules, questions and defects live HERE, numbered per job:
  rules     BR-<PREFIX>-<JJJ>-NN   e.g. BR-BAT-012-03
  questions Q-<PREFIX>-<JJJ>-NN
  defects   D-<PREFIX>-<JJJ>-NN
/re-coverage consolidates them. Rules shared by many jobs (common library) use job number 000 and live in the component's rules.md.
-->

## Business purpose

<What business outcome this job produces each night, and who relies on it (ops, finance, clients, a third party).>

## Schedule and triggering

| Aspect | Detail | Source |
|---|---|---|
| Schedule | e.g. nightly 01:30, business days only | |
| Scheduler | In repo (cron / Quartz / Spring Batch / …) or external (Control-M, Autosys, Windows Task Scheduler …) | |
| Entry point | e.g. `POST /batch/interest-accrual`, a main class, a script | |
| Runs after (depends on) | BJ-… | |
| Followed by | BJ-… | |
| Business date used | System date / business-date table / parameter | |
| Parameters | | |

## Input selection: which records are picked

| Source (entity / table / file) | Selection criteria, in business terms | Rules | Source (query / code) |
|---|---|---|---|
| ENT-Client | Active clients whose cash balance is negative at end of day | BR-XXX-JJJ-01 | `path:line` |

## Processing

| Step | What happens per record / per group (business terms) | Rules | Source |
|---|---|---|---|

## Outputs

| Output | Kind (table insert / update / delete, file, event, email, report) | Business meaning | Target (entity / table / FL-NNN / INT-NNN) | Source |
|---|---|---|---|---|

## Record-level exceptions

| Situation | Behaviour (skip & log / reject whole file / abort job / route to ops queue) | Where it is reported | Source |
|---|---|---|---|

## Re-run, restart and idempotency

- **Re-run for the same business date:** <What happens to records already processed? Can it create duplicates?>
- **Restart after failure:** <Starts over, or resumes from a checkpoint?>
- **Manual trigger:** <From the back-office, by ops, by parameter?>

## Controls and reconciliation

<Record counts, control totals, header/trailer checks, completion flags, alerts, who gets notified on failure.>

## Rules

### BR-XXX-JJJ-01 — <Short title>

- **Statement:**
- **Rationale (inferred):**
- **Trigger:** Nightly run of BJ-NNN
- **Conditions / exceptions:**
- **Outcome on violation:**
- **Source:**
- **Confidence:** High | Medium | Low
- **Technical note:**
- **Related:**
- **Status:** Draft
- **Product comments:**

## Questions

| ID | Question for product | What the code does today | Related | Raised | Answer | Status |
|---|---|---|---|---|---|---|

## Suspected defects

| ID | Observation | Evidence | Possible impact | Related | Raised | Decision | Status |
|---|---|---|---|---|---|---|---|

## Product comments
