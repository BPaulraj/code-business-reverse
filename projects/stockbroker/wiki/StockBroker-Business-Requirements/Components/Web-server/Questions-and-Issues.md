> 🔄 **Generated** by the reverse-engineering kit from project `stockbroker` (code commit `ae607a6`, 2026-10-04, business view). **Do not edit this page**: changes are overwritten on the next publish. Give feedback through the review packs.

| ID | Question for product | What the code does today | Related | Raised | Answer | Status |
|---|---|---|---|---|---|---|
| Q-WEB-001 | Should a trade be rejected, or re-confirmed, if the execution price moves too far from the quote? What tolerance? | The trade executes at a fresh price with no limit. The gap can reach about 4%. The screen only warns that the price "may differ slightly". | BR-WEB-025, BR-FO-006 | 2026-10-04 | | Open |
| Q-WEB-002 | Should rejected or failed trades be recorded (status Failed exists)? | Rejected trades leave no record. Status Failed is never used. | ENT-Trade, D-DOM-001 | 2026-10-04 | | Open |
| Q-WEB-003 | Should company search ignore upper/lower case? | It depends on the database. SQLite matching is case-insensitive for English letters, but a production database may not be. | BR-WEB-015 | 2026-10-04 | | Open |
| Q-WEB-004 | Is a fixed 7-day session acceptable, or is an inactivity timeout needed? | 7 days from login, regardless of activity | BR-WEB-002 | 2026-10-04 | | Open |
| Q-WEB-005 | Should funding or trading require KYC to be Verified? | No KYC check anywhere | Q-DOM-001 | 2026-10-04 | | Open |
| Q-WEB-006 | Should realised profit/loss on sales be calculated and reported? | Only unrealised gain/loss on current holdings is shown | BR-WEB-030, BR-LIB-003 | 2026-10-04 | | Open |
| Q-WEB-007 | Is an audit trail required for account changes and logins? | Nothing is logged except unexpected errors | api-catalogue cross-cutting | 2026-10-04 | | Open |

| ID | Observation | Evidence | Possible impact | Related | Raised | Decision | Status |
|---|---|---|---|---|---|---|---|
| D-WEB-001 | Logout only deletes the browser cookie. The session token stays valid until it expires 7 days after login. | `packages/server/src/modules/auth/authRoutes.ts:82-85` | A copied or stolen token keeps working after logout | BR-WEB-012 | 2026-10-04 | | Open |
| D-WEB-002 | Trade and funding notifications are written **after** the main transaction commits, and outside it | `packages/server/src/modules/trades/tradesRoutes.ts:129-146`, `packages/server/src/modules/wallet/walletRoutes.ts:83-90` | If writing the message fails (e.g. DB busy, D-DB-002), the trade or funding is already done, but the client sees "Internal server error". They may retry and **trade twice**. | BR-WEB-034, D-WEB-004 | 2026-10-04 | | Open |
| D-WEB-003 | The pending funding transaction is created separately from the final credit. Nothing ever reconciles or fails a stuck Pending transaction. | `walletRoutes.ts:58-81` | If the server stops during the 0.8–1.5 s delay, a Pending transaction remains forever and the wallet isn't credited | BR-WEB-020, Q-DOM-003 | 2026-10-04 | | Open |
| D-WEB-004 | No duplicate-submission protection on the server for trades or funding (no idempotency key, no per-client lock) | `tradesRoutes.ts:25-28`, `walletRoutes.ts:41-45` | Double submission (network retry, API client, D-WEB-002 retry) creates duplicate trades or deposits. Only the screen's disabled button protects against double-clicks (BR-FO-007). | BR-FO-007, BR-FO-011 | 2026-10-04 | | Open |
| D-WEB-005 | `GET /api/invoices` has no caller in the portal | `packages/server/src/modules/invoices/invoicesRoutes.ts:12-22`. Grep of `packages/web` for `/invoices"` found only the PDF link. | Possible dead code, or a missing "My invoices" screen | BR-WEB-037 | 2026-10-04 | | Open |
| D-WEB-006 | The buy balance check uses the execution price, while the screen pre-checks with the quote | `tradesRoutes.ts:48` vs `packages/web/src/pages/Trade.tsx:54` | A client with just enough balance for the quote may be rejected at confirmation. Low impact, but confusing. | BR-WEB-027, BR-FO-005 | 2026-10-04 | | Open |
| D-WEB-007 | No limit on failed login attempts | `authRoutes.ts:62-80` | Password guessing is possible | BR-WEB-011 | 2026-10-04 | | Open |
