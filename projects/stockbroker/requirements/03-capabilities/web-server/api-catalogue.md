# Web server — API Catalogue

**Component:** `packages/server` · **Prefix:** `WEB` · **Last extracted:** 2026-10-04 · **Status:** Extracted

**Logic type** says where the business logic lives:

| Logic type | Meaning |
|---|---|
| **Pass-through** | Forwards to back-office / a service with no business logic |
| **Orchestration** | Calls several downstream services in sequence |
| **Business logic** | Rules are implemented in the web service itself |
| **Data query** | Reads or writes the DB directly. Selection criteria and updates are rules. |

In this component, every endpoint goes straight to the database. There is no back-office or service layer behind it.

## Endpoints by business area

### Account and session

| # | Method + path | Business operation | Consumers | Downstream | Logic type | Auth | Rules | Source |
|---|---|---|---|---|---|---|---|---|
| 1 | `POST /api/auth/register` | Register a new client | FE Register screen (`packages/web/src/auth/AuthContext.tsx:41`) | DB: User, Wallet, InboxMessage | Business logic | Public | BR-WEB-007…010, BR-LIB-008…011 | `packages/server/src/modules/auth/authRoutes.ts:26-60` |
| 2 | `POST /api/auth/login` | Sign in | FE Login screen (`AuthContext.tsx:36`) | DB: User | Business logic | Public | BR-WEB-011, BR-WEB-002 | `authRoutes.ts:62-80` |
| 3 | `POST /api/auth/logout` | Sign out | FE header "Log out" (`AuthContext.tsx:46`) | — | Business logic | Public | BR-WEB-012 | `authRoutes.ts:82-85` |
| 4 | `GET /api/auth/me` | Who is signed in | FE on every page load (`AuthContext.tsx:25`) | DB: User | Data query | Session | BR-WEB-001 | `authRoutes.ts:87-97` |
| 5 | `PUT /api/auth/profile` | Update own profile | FE Profile screen (`packages/web/src/api/profile.ts:14`) | DB: User | Data query | Session | BR-WEB-013, BR-LIB-009, 011, 012 | `authRoutes.ts:99-112` |

### Portfolio and market

| # | Method + path | Business operation | Consumers | Downstream | Logic type | Auth | Rules | Source |
|---|---|---|---|---|---|---|---|---|
| 6 | `GET /api/dashboard/summary` | Account snapshot | FE Dashboard (`packages/web/src/api/dashboard.ts:8`) | DB: Wallet, Holding, Trade; LIB valuation | Business logic | Session | BR-WEB-017, 018, BR-LIB-003 | `packages/server/src/modules/dashboard/dashboardRoutes.ts:12-46` |
| 7 | `GET /api/holdings` | Client's holdings with valuation | FE Trade screen (`packages/web/src/api/holdings.ts:8`) | LIB `getHoldingsDto` | Data query | Session | BR-LIB-002, 003 | `packages/server/src/modules/holdings/holdingsRoutes.ts:10-16` |
| 8 | `GET /api/companies?search=` | List and search tradable companies with current price | FE Trade screen (`packages/web/src/api/companies.ts:8`) | DB: Company; LIB price | Data query | Session | BR-WEB-015, BR-LIB-001 | `packages/server/src/modules/companies/companiesRoutes.ts:12-36` |

### Wallet and funding

| # | Method + path | Business operation | Consumers | Downstream | Logic type | Auth | Rules | Source |
|---|---|---|---|---|---|---|---|---|
| 9 | `GET /api/wallet` | Wallet balance | FE Trade and Payments screens (`packages/web/src/api/wallet.ts:8`) | DB: Wallet | Data query | Session | BR-WEB-004 | `packages/server/src/modules/wallet/walletRoutes.ts:20-27` |
| 10 | `GET /api/wallet/transactions` | Wallet transaction history | FE Payments screen (`wallet.ts:15`) | DB: Transaction | Data query | Session | BR-WEB-019 | `walletRoutes.ts:29-39` |
| 11 | `POST /api/wallet/add-funds` | Add funds by bank transfer or debit card (simulated) | FE Payments screen (`wallet.ts:27`) | DB: Transaction, Wallet, InboxMessage | Business logic | Session | BR-WEB-020…022, BR-LIB-013…018 | `walletRoutes.ts:41-97` |

### Trading and invoices

| # | Method + path | Business operation | Consumers | Downstream | Logic type | Auth | Rules | Source |
|---|---|---|---|---|---|---|---|---|
| 12 | `GET /api/trades` | Trade history | FE Trade screen (`packages/web/src/api/trades.ts:8`) | DB: Trade, Company, Invoice | Data query | Session | BR-WEB-023 | `packages/server/src/modules/trades/tradesRoutes.ts:13-23` |
| 13 | `POST /api/trades` | Execute a buy or sell | FE Trade screen confirm (`trades.ts:15`) | DB: Wallet, Holding, Transaction, Trade, Invoice, InboxMessage; LIB price and invoice number | Business logic | Session | BR-WEB-024…036, BR-LIB-019 | `tradesRoutes.ts:25-150` |
| 14 | `GET /api/invoices` | List client's invoices | **No consumer found** | DB: Invoice | Data query | Session | BR-WEB-037 | `packages/server/src/modules/invoices/invoicesRoutes.ts:12-22` |
| 15 | `GET /api/invoices/:id/pdf` | Download invoice PDF | FE Invoice links (`packages/web/src/components/InvoiceLink.tsx:5`) | DB; LIB PDF | Business logic | Session + owner | BR-WEB-038, BR-LIB-005…007 | `invoicesRoutes.ts:24-43` |

### Inbox

| # | Method + path | Business operation | Consumers | Downstream | Logic type | Auth | Rules | Source |
|---|---|---|---|---|---|---|---|---|
| 16 | `GET /api/inbox` | List messages | FE Inbox (`packages/web/src/api/inbox.ts:8`) | DB: InboxMessage | Data query | Session | BR-WEB-039 | `packages/server/src/modules/inbox/inboxRoutes.ts:13-22` |
| 17 | `GET /api/inbox/unread-count` | Unread badge | FE navigation (`inbox.ts:15`) | DB | Data query | Session | BR-WEB-040 | `inboxRoutes.ts:24-32` |
| 18 | `PATCH /api/inbox/:id` | Mark message read or unread | FE Inbox (`inbox.ts:24`) | DB | Data query | Session + owner | BR-WEB-041, BR-WEB-005 | `inboxRoutes.ts:34-51` |
| 19 | `GET /api/health` | Health check | Not used by FE (operational) | — | Pass-through | Public | — | `packages/server/src/index.ts:22` |

## Cross-cutting behaviour

| Concern | Behaviour | Business-relevant? | Rules | Source |
|---|---|---|---|---|
| Authentication / session | 7-day signed session stored in an http-only cookie | Yes | BR-WEB-001, 002 | `packages/server/src/middleware/requireAuth.ts:10-23`, `authRoutes.ts:14-24` |
| Authorisation model | No roles. Every signed-in client has the same rights, limited to their own data. | Yes | BR-WEB-004, 005 | `where: { userId }` in every query |
| Allowed callers | Only the configured web origin may call with credentials | Technical | — | `packages/server/src/index.ts:18`, `packages/server/src/env.ts:14` |
| Common validation | Invalid input → "Validation failed" with a message per field | Yes (messages) | BR-LIB-008…019 | `packages/server/src/middleware/errorHandler.ts:6-13` |
| Unexpected errors | "Internal server error" with no detail | Yes | D-WEB-002 | `errorHandler.ts:19-20` |
| Audit logging | **None** | Yes | Q-WEB-007 | — |
| Idempotency / duplicate protection | **None** on the server | Yes | D-WEB-004 | — |

## Unused or unmatched endpoints

| Method + path | Observation | Defect |
|---|---|---|
| `GET /api/invoices` | No caller in the front end. Invoices are reached only via trade history and inbox links. | D-WEB-005 |
| `GET /api/health` | Operational only | — |
