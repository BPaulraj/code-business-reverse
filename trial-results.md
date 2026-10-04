# Kit trial — StockBroker demo (2026-10-04)

**Target:** `D:\AutomationProjects\Applications\StockBroker` at commit `ae607a6`, read only. The repo was left untouched.
**Output:** `projects/stockbroker/requirements/` in this kit repo.
**Size:** a TypeScript monorepo of about 3,800 lines:
- React portal
- Express portal back end
- separate public REST API
- shared domain library
- SQLite via Prisma

**Method:** extraction from code only. The repo's `Docs/` and README were not read until afterwards, when the Product Spec was used as a stand-in for the product team.

## Phases run

| Phase | Kit command | Result |
|---|---|---|
| 0 | `/re-discover` | 5 components mapped. No microservices, batch, back-office or third parties. |
| 1 | `/re-domain` | 8 entities with lifecycles, 10 DB rules |
| 2 | `/re-api` ×2 | Portal back end: 19 endpoints, 42 rules. Public API: 17 endpoints, 7 own rules plus a 29-rule duplicate map. |
| 2 | (core library) | 20 shared rules |
| 4 | `/re-ui` | 17 screen rules, 7 journeys, roles matrix |
| 5 | `/re-process` | P-001 trade, P-002 funding, P-003 registration, with failure paths and sequence diagrams |
| 2a | `/re-verify` | 227 citations checked mechanically (0 broken). 1 rule corrected. |
| 6 | `/re-review-pack` | P-001 pack: 21 rules, 7 questions, 5 defects |
| — | `/re-coverage` | 96 rules, 21 questions, 19 suspected defects |

## Accuracy vs the Product Spec

- **19 of 20** spec business rules were recovered fully from code. One (password hashing as a rule) was found only partially.
- **None** contradicted.
- **4 of 7** sampled open questions are answered by the spec.
- **Spec gaps found:** 12 findings the spec doesn't mention, including:
  - a whole public API channel with copy-pasted rules
  - post-commit notifications that can cause duplicate trades on retry
  - no server-side duplicate protection
  - stuck Pending payments
  - invoice-number collision risk

Full comparison: `projects/stockbroker/requirements/_review/2026-10-04-accuracy-vs-product-spec.md`

## Kit changes made after the trial

1. Full repo-relative paths are required in every citation. Mechanical citation checks were added to `/re-verify` and `/re-coverage`.
2. New "where rules hide" items: side effects after commit, duplicate-submission exposure, data protection.
3. New RULES §6a: shared libraries get their own folder and prefix; copy-pasted logic is documented once, with a duplicate map.
4. `/re-ui` checks that money-moving actions have a confirmation step.
5. Business purpose and NFRs are explicitly out of extraction scope.
6. README: how to use old documents as a benchmark.
7. **Artefacts moved out of the application repo:** the kit now runs from its own repo. `/re-init` registers the target; output goes to `projects/<name>/`, and the target is read-only.

## Caveats

- **Same-session verification:** it ran in the same session as the extraction, and the kit says to verify in a fresh one. Re-run `/re-verify` after `/clear` for a true independent check.
- **Small demo:** the codebase was small and modern. On a decade-old system, expect lower confidence, more questions, and more need for the resumable, one-component-per-session workflow.
