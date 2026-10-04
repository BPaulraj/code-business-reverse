> 🔄 **Generated** by the reverse-engineering kit from project `stockbroker` (code commit `ae607a6`, 2026-10-04, business view). **Do not edit this page**: changes are overwritten on the next publish. Give feedback through the review packs.

[[_TOC_]]

**Component:** `packages/api` · **Prefix:** `API` · **Last extracted:** 2026-10-04 · **Status:** Extracted
**Published contract:** `packages/api/openapi.yaml`, served at `/api/v1/docs` (`packages/api/src/docs.ts:15-16`). Its paths match the code (15 operations).

All endpoints go straight to the database. "Same as" means the logic is a copy of the web server endpoint.

## Endpoints by business area

### Account and session

| # | Method + path | Business operation | Consumers | Downstream | Logic type | Auth | Rules | Source |
|---|---|---|---|---|---|---|---|---|
| 1 | `POST /api/v1/users` | Register; returns an access token | External clients (unknown) | DB: User, Wallet, InboxMessage | Business logic | Public | Same as WEB #1 + BR-API-001 | `packages/api/src/modules/users/usersRoutes.ts:12-46` |
| 2 | `GET /api/v1/users/me` | Own profile | External | DB | Data query | Token | BR-WEB-004 | `usersRoutes.ts:48-56` |
| 3 | `PUT /api/v1/users/me` | Update profile | External | DB | Data query | Token | Same as WEB #5 | `usersRoutes.ts:58-66` |
| 4 | `POST /api/v1/sessions` | Login; returns an access token | External | DB | Business logic | Public | Same as WEB #2 + BR-API-001 | `packages/api/src/modules/sessions/sessionsRoutes.ts:11-29` |

### Portfolio and market

| # | Method + path | Business operation | Consumers | Downstream | Logic type | Auth | Rules | Source |
|---|---|---|---|---|---|---|---|---|
| 5 | `GET /api/v1/companies?search=` | List and search companies | External | DB; LIB price | Data query | Token | Same as WEB #8 | `packages/api/src/modules/companies/companiesRoutes.ts:11-35` |
| 6 | `GET /api/v1/portfolio` | Cash, stock value, total value, holdings | External | DB; LIB valuation | Business logic | Token | BR-API-003 | `packages/api/src/modules/portfolio/portfolioRoutes.ts:10-29` |
| 7 | `GET /api/v1/portfolio/holdings` | Holdings only | External | LIB | Data query | Token | Same as WEB #7 | `portfolioRoutes.ts:31-37` |

### Wallet and funding

| # | Method + path | Business operation | Consumers | Downstream | Logic type | Auth | Rules | Source |
|---|---|---|---|---|---|---|---|---|
| 8 | `GET /api/v1/wallet/balance` | Wallet balance | External | DB | Data query | Token | Same as WEB #9 | `packages/api/src/modules/wallet/walletRoutes.ts:12-20` |
| 9 | `POST /api/v1/payments` | Add funds (simulated) | External | DB | Business logic | Token | Same as WEB #11 + BR-API-007 | `packages/api/src/modules/payments/paymentsRoutes.ts:13-68` |

### Trading and invoices

| # | Method + path | Business operation | Consumers | Downstream | Logic type | Auth | Rules | Source |
|---|---|---|---|---|---|---|---|---|
| 10 | `GET /api/v1/trades` | Trade history | External | DB | Data query | Token | Same as WEB #12 | `packages/api/src/modules/trades/tradesRoutes.ts:12-22` |
| 11 | `POST /api/v1/trades` | Execute buy or sell | External | DB; LIB | Business logic | Token | Same as WEB #13 + BR-API-006 | `tradesRoutes.ts:24-151` |
| 12 | `GET /api/v1/invoices/by-trade/{tradeId}` | Invoice details and PDF link for a trade | External | DB | Business logic | Token + owner | BR-API-004 | `packages/api/src/modules/invoices/invoicesRoutes.ts:11-28` |
| 13 | `GET /api/v1/invoices/{invoiceId}/pdf` | Download invoice PDF | External | DB; LIB PDF | Business logic | Token + owner | Same as WEB #15 | `invoicesRoutes.ts:30-49` |

### Inbox

| # | Method + path | Business operation | Consumers | Downstream | Logic type | Auth | Rules | Source |
|---|---|---|---|---|---|---|---|---|
| 14 | `GET /api/v1/inbox` | List messages | External | DB | Data query | Token | Same as WEB #16 | `packages/api/src/modules/inbox/inboxRoutes.ts:11-20` |
| 15 | `GET /api/v1/inbox/{id}` | Read one message (doesn't mark it read) | External | DB | Data query | Token + owner | BR-API-005 | `inboxRoutes.ts:22-31` |
| 16 | `GET /api/v1/openapi.json`, `/api/v1/docs` | API documentation | Developers | — | Pass-through | Public | — | `packages/api/src/docs.ts:15-16` |
| 17 | `GET /api/health` | Health check | Operations | — | Pass-through | Public | — | `packages/api/src/index.ts:25` |

## Cross-cutting behaviour

| Concern | Behaviour | Business-relevant? | Rules | Source |
|---|---|---|---|---|
| Authentication | Bearer access token, valid 7 days, obtained at registration or login | Yes | BR-API-001 | `packages/api/src/middleware/requireAuth.ts:10-24`, `packages/api/src/lib/token.ts:4-8` |
| Allowed callers | Any origin (open CORS). Intended for Swagger, Postman and curl clients. | Yes | BR-API-002 | `packages/api/src/index.ts:19-22` |
| Authorisation | Same as the web server: own data only, no roles | Yes | BR-WEB-004, 005 | |
| Validation, errors | Same as the web server | Yes | BR-WEB-006 | `packages/api/src/middleware/errorHandler.ts:5-21` |
| Logout / revocation | **None** | Yes | D-API-002 | — |

## Feature gaps vs web server

| Web server capability | In public API? |
|---|---|
| Logout | No |
| Dashboard summary | No; replaced by `/portfolio` (no recent trades, no gain/loss totals) |
| Wallet transaction history | **No** |
| Invoice list | No; lookup by trade instead |
| Unread count, mark read/unread | **No** |

## Unused or unmatched endpoints

The consumers are external and unknown. No usage evidence is available in the repo (Q-API-001).
