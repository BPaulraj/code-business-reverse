> 🔄 **Generated** by the reverse-engineering kit from project `stockbroker` (code commit `ae607a6`, 2026-10-04, business view). **Do not edit this page**: changes are overwritten on the next publish. Give feedback through the review packs.

| ID | Observation | Evidence | Possible impact | Related | Raised | Decision | Status |
|---|---|---|---|---|---|---|---|
| D-DB-001 | Money amounts (balance, amount, price, total, average cost) are stored as floating-point numbers, not decimals | `packages/db/prisma/schema.prisma:29,40,53,64,78-79` | Cent-level rounding drift in balances and average costs over many transactions | BR-WEB-026 | 2026-10-04 | | Open |
| D-DB-002 | Two independent processes (web server and public API) write the same SQLite file | `packages/db/src/prisma.ts:5-11` (the comment says contention is reduced "but not eliminated") | Under load, writes can time out after 5 s, so trades or funding fail with "Internal server error" | D-API-001 | 2026-10-04 | | Open |
