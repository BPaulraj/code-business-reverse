# Suspected defects — Core library

| ID | Observation | Evidence | Possible impact | Related | Raised | Decision | Status |
|---|---|---|---|---|---|---|---|
| D-LIB-001 | Invoice numbers use only 8 hex characters of the trade ID. A collision is rare, but it would break the unique constraint inside the trade transaction. | `packages/db/src/services/invoiceService.ts:3-4`, `packages/server/src/modules/trades/tradesRoutes.ts:119-124` | The whole trade is rolled back and the client sees "Internal server error". This becomes more likely as volume grows. | BR-LIB-004, BR-DB-005 | 2026-10-04 | | Open |
