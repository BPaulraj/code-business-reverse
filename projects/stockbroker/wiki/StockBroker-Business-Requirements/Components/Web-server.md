> 🔄 **Generated** by the reverse-engineering kit from project `stockbroker` (code commit `ae607a6`, 2026-10-04, business view). **Do not edit this page**: changes are overwritten on the next publish. Give feedback through the review packs.

[[_TOC_]]

**Component:** `packages/server` · **Prefix:** `WEB` · **Tech:** Node, Express 4, Zod, JWT (cookie) · **Last extracted:** 2026-10-04 · **Status:** Extracted

## Purpose

The back end of the client portal. It authenticates clients, and it applies and persists every business operation the portal offers: registration, profile, funding, trading, invoices and inbox. It writes straight to the shared database.

## Responsibilities

- **Account and session:** registration (with automatic wallet and welcome message), login, logout, profile update.
- **Portfolio and market:** dashboard summary, holdings valuation, company list and search with live (simulated) prices.
- **Wallet and funding:** balance, transaction history, simulated bank transfer and card deposits.
- **Trading:** buy and sell execution with balance and holding checks, the cash leg, invoice creation and notifications.
- **Invoices:** invoice PDF download (owner only).
- **Inbox:** list, unread count, mark read or unread.

## Not owned here

- The price, valuation, invoice numbering, PDF and validation rules are in the [Core library](/Business-Requirements/StockBroker-Business-Requirements/Components/Core-library).
- The same operations exist, copied, in the [Public API](/Business-Requirements/StockBroker-Business-Requirements/Components/Public-REST-API).

## Entry points

See [api-catalogue.md](/Business-Requirements/StockBroker-Business-Requirements/Components/Web-server/API-Catalogue): 19 endpoints.

## Data owned / touched

| Entity | Access | Notes |
|---|---|---|
| [Client](/Business-Requirements/StockBroker-Business-Requirements/Domain-Model/ENT%2DClient-%E2%80%94-Client-account) | Write | register, profile |
| [Wallet](/Business-Requirements/StockBroker-Business-Requirements/Domain-Model/ENT%2DWallet-%E2%80%94-Cash-wallet) | Write | register, funding, trades |
| [Wallet transaction](/Business-Requirements/StockBroker-Business-Requirements/Domain-Model/ENT%2DWalletTransaction-%E2%80%94-Wallet-transaction) | Write | funding, trades |
| [Holding](/Business-Requirements/StockBroker-Business-Requirements/Domain-Model/ENT%2DHolding-%E2%80%94-Share-holding-%28position%29) | Write | trades |
| [Trade](/Business-Requirements/StockBroker-Business-Requirements/Domain-Model/ENT%2DTrade-%E2%80%94-Trade) | Write | trades |
| [Invoice](/Business-Requirements/StockBroker-Business-Requirements/Domain-Model/ENT%2DInvoice-%E2%80%94-Trade-invoice) | Write | trades |
| [Inbox message](/Business-Requirements/StockBroker-Business-Requirements/Domain-Model/ENT%2DInboxMessage-%E2%80%94-Inbox-message) | Write | register, funding, trades, read status |
| [Company](/Business-Requirements/StockBroker-Business-Requirements/Domain-Model/ENT%2DCompany-%E2%80%94-Listed-company) | Read | listing, trades |

## Dependencies

| Depends on | Why | How | Source |
|---|---|---|---|
| Core library | Price, valuation, invoice, validation, messaging | In-process import | `packages/server/src/modules/trades/tradesRoutes.ts:6-7` |
| Shared database | All persistence | Prisma | `packages/server/src/prisma.ts:1` |

## Configuration with business meaning

| Key | Business meaning | Value in repo | Production value known? |
|---|---|---|---|
| Session length (hard-coded) | How long a client stays signed in | 7 days | `authRoutes.ts:14,17` |
| Processing delay (hard-coded) | Simulated payment processing time | Bank transfer 1.5 s, card 0.8 s | `walletRoutes.ts:52,55` |
| `WEB_ORIGIN` | Address of the portal allowed to call | `http://localhost:5173` | No |
| `JWT_SECRET` | Session signing key | placeholder in `.env.example` | No (secret) |

## Business rules

See [rules.md](/Business-Requirements/StockBroker-Business-Requirements/Components/Web-server/Rules): 42 rules. High 39 / Medium 3 / Low 0.

## Open questions and suspected defects

See [_questions.md](/Business-Requirements/StockBroker-Business-Requirements/Components/Web-server/Questions-and-Issues) and [_defects.md](/Business-Requirements/StockBroker-Business-Requirements/Components/Web-server/Questions-and-Issues).


## Pages

[[_TOSP_]]
