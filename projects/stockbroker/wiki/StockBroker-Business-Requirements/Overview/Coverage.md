> 🔄 **Generated** by the reverse-engineering kit from project `stockbroker` (code commit `ae607a6`, 2026-10-04, business view). **Do not edit this page**: changes are overwritten on the next publish. Give feedback through the review packs.

[[_TOC_]]

`/re-coverage` refreshes this file. Each command updates its own row when it finishes.

**Component status flow:** Not started → In progress → Extracted → Verified → In review → Confirmed

## Components

| Component | Folder | Entry points (found / done) | Rules | High / Med / Low | Open Q | Defects | Status | Last updated |
|---|---|---|---|---|---|---|---|---|
| Shared database | `database` | 2 / 2 | 10 | 9 / 1 / 0 | 0 | 2 | Extracted | 2026-10-04 |
| Core library | `core-library` | 7 / 7 | 20 | 19 / 1 / 0 | 3 | 1 | Extracted | 2026-10-04 |
| Web server | `web-server` | 19 / 19 | 42 | 39 / 3 / 0 | 7 | 7 | Verified (same session) | 2026-10-04 |
| Public API | `public-api` | 17 / 17 | 7 own + 29 duplicated | 6 / 1 / 0 | 2 | 5 | Extracted | 2026-10-04 |
| Front-end | `front-end` | 8 / 8 | 17 | 17 / 0 / 0 | 1 (+2 journeys) | 3 | Extracted | 2026-10-04 |
| Domain (entities) | `01-domain` | 8 entities | — | — | 5 | 1 | Extracted | 2026-10-04 |
| Back-office, microservices, batch, connectivity | — | — | — | — | — | — | Not present | 2026-10-04 |

## Web services

| Component / area | Endpoints (found / done) | Pass-through | Orchestration | Business logic | Data query | Unused | Rules | Status |
|---|---|---|---|---|---|---|---|---|
| Web server, all areas | 19 / 19 | 1 | 0 | 7 | 11 | 1 (`GET /api/invoices`) | 41 | Verified (same session) |
| Public API, all areas | 17 / 17 | 2 | 0 | 7 | 8 | unknown (external) | 7 + 29 dup | Extracted |

## Batch jobs

None in this repo.

## Processes

| ID | Process | Components | Steps | Gaps | Status | Last updated |
|---|---|---|---|---|---|---|
| P-001 | Place a trade | FE, WEB/API, LIB, DB | 11 + 8 failure paths | Order types, fees, realised P&L | Extracted | 2026-10-04 |
| P-002 | Add funds | FE, WEB/API, LIB, DB | 7 + 5 failure paths | Withdrawals, declined payments | Extracted | 2026-10-04 |
| P-003 | Register client | FE, WEB/API, LIB, DB | 7 + 4 failure paths | Email verification, KYC | Extracted | 2026-10-04 |

## Review progress (rules)

| Draft | In review | Confirmed | Changed | Rejected | Obsolete |
|---|---|---|---|---|---|
| 75 | 21 | 0 | 0 | 0 | 0 |

**Totals:** 96 unique business rules (10 DB + 20 LIB + 42 WEB + 7 API + 17 FO), 21 open questions, 19 suspected defects.
