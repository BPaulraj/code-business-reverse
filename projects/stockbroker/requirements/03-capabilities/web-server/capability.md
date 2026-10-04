# Web server — Capability

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

- The price, valuation, invoice numbering, PDF and validation rules are in the [Core library](../core-library/capability.md).
- The same operations exist, copied, in the [Public API](../public-api/capability.md).

## Entry points

See [api-catalogue.md](api-catalogue.md): 19 endpoints.

## Data owned / touched

| Entity | Access | Notes |
|---|---|---|
| [Client](../../01-domain/entities/client.md) | Write | register, profile |
| [Wallet](../../01-domain/entities/wallet.md) | Write | register, funding, trades |
| [Wallet transaction](../../01-domain/entities/wallet-transaction.md) | Write | funding, trades |
| [Holding](../../01-domain/entities/holding.md) | Write | trades |
| [Trade](../../01-domain/entities/trade.md) | Write | trades |
| [Invoice](../../01-domain/entities/invoice.md) | Write | trades |
| [Inbox message](../../01-domain/entities/inbox-message.md) | Write | register, funding, trades, read status |
| [Company](../../01-domain/entities/company.md) | Read | listing, trades |

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

See [rules.md](rules.md): 42 rules. High 39 / Medium 3 / Low 0.

## Open questions and suspected defects

See [_questions.md](_questions.md) and [_defects.md](_defects.md).
