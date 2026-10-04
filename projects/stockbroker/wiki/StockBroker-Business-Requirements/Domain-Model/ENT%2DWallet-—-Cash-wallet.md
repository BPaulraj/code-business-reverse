> 🔄 **Generated** by the reverse-engineering kit from project `stockbroker` (code commit `ae607a6`, 2026-10-04, business view). **Do not edit this page**: changes are overwritten on the next publish. Give feedback through the review packs.

[[_TOC_]]

**Status:** Draft · **Owner component:** Web server / Public API · **Stored in:** `Wallet`

## Definition

The client's single cash account in USD. Funding credits it. Purchases debit it and sales credit it. It cannot go below zero through trading, because purchases are checked against the balance (BR-WEB-027).

## Identifiers

| Identifier | Business meaning | Source |
|---|---|---|
| Wallet ID | System-generated UUID | `packages/db/prisma/schema.prisma:27` |
| Client ID | Owner. At most one wallet per client. | `schema.prisma:28` |

## Key attributes

| Attribute | Meaning | Allowed values / format | Column | Source |
|---|---|---|---|---|
| Balance | Available cash, USD | Decimal (stored as floating point), starts at 0 | `balance` | `schema.prisma:29` |

## Lifecycle

| Event | Effect on balance | Rules | Source |
|---|---|---|---|
| Opened at registration | 0 | BR-WEB-008, BR-DB-007 | `packages/server/src/modules/auth/authRoutes.ts:46` |
| Funding succeeds | + amount | BR-WEB-020 | `packages/server/src/modules/wallet/walletRoutes.ts:73-76` |
| Buy executed | − trade total | BR-WEB-028 | `packages/server/src/modules/trades/tradesRoutes.ts:54` |
| Sell executed | + trade total | BR-WEB-031 | `tradesRoutes.ts:93` |

There is no withdrawal function. Grep for `decrement` found only the buy path (Q-DOM-002).

## Relationships

| Related entity | Relationship | Cardinality |
|---|---|---|
| [Client](/Business-Requirements/StockBroker-Business-Requirements/Domain-Model/ENT%2DClient-%E2%80%94-Client-account) | belongs to | 1 |
| [Wallet transaction](/Business-Requirements/StockBroker-Business-Requirements/Domain-Model/ENT%2DWalletTransaction-%E2%80%94-Wallet-transaction) | has history of | 0..n |

## Constraints

- BR-DB-002: one wallet per client
- BR-DB-007: opening balance 0
- D-DB-001: money is stored as floating point

## Product comments
