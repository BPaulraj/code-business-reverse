> 🔄 **Generated** by the reverse-engineering kit from project `stockbroker` (code commit `ae607a6`, 2026-10-04, business view). **Do not edit this page**: changes are overwritten on the next publish. Give feedback through the review packs.

| ID | Question for product | What the code does today | Related | Raised | Answer | Status |
|---|---|---|---|---|---|---|
| Q-LIB-001 | Are there daily/monthly funding limits, or a minimum deposit? | Only a per-transaction cap of 1,000,000 and > 0. Unlimited repeats are allowed. | BR-LIB-013 | 2026-10-04 | | Open |
| Q-LIB-002 | Should the 0.1% (min $0.50) brokerage fee actually be charged? | The fee is printed on the invoice as illustrative. Nothing is deducted. | BR-LIB-006 | 2026-10-04 | | Open |
| Q-LIB-003 | Should an invoice keep the client details as they were at trade time? | The PDF is regenerated each time from current profile data. | BR-LIB-005 | 2026-10-04 | | Open |

| ID | Observation | Evidence | Possible impact | Related | Raised | Decision | Status |
|---|---|---|---|---|---|---|---|
| D-LIB-001 | Invoice numbers use only 8 hex characters of the trade ID. A collision is rare, but it would break the unique constraint inside the trade transaction. | `packages/db/src/services/invoiceService.ts:3-4`, `packages/server/src/modules/trades/tradesRoutes.ts:119-124` | The whole trade is rolled back and the client sees "Internal server error". This becomes more likely as volume grows. | BR-LIB-004, BR-DB-005 | 2026-10-04 | | Open |
