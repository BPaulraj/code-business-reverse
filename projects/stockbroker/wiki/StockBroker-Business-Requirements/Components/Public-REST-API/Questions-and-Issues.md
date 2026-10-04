> 🔄 **Generated** by the reverse-engineering kit from project `stockbroker` (code commit `ae607a6`, 2026-10-04, business view). **Do not edit this page**: changes are overwritten on the next publish. Give feedback through the review packs.

| ID | Question for product | What the code does today | Related | Raised | Answer | Status |
|---|---|---|---|---|---|---|
| Q-API-001 | Who are the intended users of the public API (partners, a mobile app, internal tools)? Should it match the portal's features (transaction history, mark read, logout)? | Open to any caller. Missing transaction history, read status and logout. | BR-API-002, api-catalogue feature gaps | 2026-10-04 | | Open |
| Q-API-002 | Should a token issued by the portal work on the API and vice versa? | Both sign tokens with a `JWT_SECRET`. Whether the values match depends on deployment. | BR-API-001 | 2026-10-04 | | Open |

| ID | Observation | Evidence | Possible impact | Related | Raised | Decision | Status |
|---|---|---|---|---|---|---|---|
| D-API-001 | Trading, funding and registration rules are **copy-pasted** between the web server and the public API, not shared | `packages/api/src/modules/trades/tradesRoutes.ts:24-151` ≈ `packages/server/src/modules/trades/tradesRoutes.ts:25-150`; also payments vs wallet add-funds, users vs auth register | Every rule change must be made twice. The two channels can silently diverge (they already differ in message text, BR-API-006). | Duplicate map in rules.md | 2026-10-04 | | Open |
| D-API-002 | No logout or token revocation in the API | `packages/api/src/index.ts:29-37` (no such route) | A leaked token is usable for 7 days | BR-API-001, D-WEB-001 | 2026-10-04 | | Open |
| D-API-003 | Messages read via the API stay unread in the portal | `packages/api/src/modules/inbox/inboxRoutes.ts:22-31` | Inconsistent unread badge for clients who use both channels | BR-API-005 | 2026-10-04 | | Open |
| D-API-004 | The published API spec says the funding minimum is 0.01. The code accepts any positive amount (e.g. 0.001). | `packages/api/openapi.yaml:500,518` vs `packages/shared/src/index.ts:229` | Sub-cent deposits are possible through the API, and the contract misleads integrators | BR-LIB-013 | 2026-10-04 | | Open |
| D-API-005 | Same server-side duplicate-submission risk as the web server, but with **no** screen to disable a button | `tradesRoutes.ts:24-28`, `paymentsRoutes.ts:13-18` | API client retries create duplicate trades or deposits | D-WEB-004 | 2026-10-04 | | Open |
