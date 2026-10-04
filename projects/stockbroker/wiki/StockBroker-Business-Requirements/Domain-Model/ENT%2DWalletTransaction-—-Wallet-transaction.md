> 🔄 **Generated** by the reverse-engineering kit from project `stockbroker` (code commit `ae607a6`, 2026-10-04, business view). **Do not edit this page**: changes are overwritten on the next publish. Give feedback through the review packs.

[[_TOC_]]

**Status:** Draft · **Owner component:** Web server / Public API · **Stored in:** `Transaction`

## Definition

One movement of cash into or out of a wallet: a funding deposit, or the cash leg of a trade.

## Key attributes

| Attribute | Meaning | Allowed values | Column | Source |
|---|---|---|---|---|
| Type | Direction | Credit (money in) / Debit (money out) | `type` | `packages/shared/src/index.ts:13` |
| Method | Origin | Bank transfer / Debit card / Trade | `method` | `index.ts:14` |
| Amount | Value, USD, always positive | > 0 | `amount` | `packages/db/prisma/schema.prisma:40` |
| Status | Processing state | Pending / Success / Failed | `status` | `index.ts:15` |
| Description | Human-readable text, e.g. "Debit card ending 4242", "Buy 5 AAPL @ $228.10" | Free text | `description` | `packages/server/src/modules/wallet/walletRoutes.ts:51-55`, `packages/server/src/modules/trades/tradesRoutes.ts:76` |
| Created at | Timestamp | Automatic | `createdAt` | `schema.prisma:43` |

## Lifecycle

| From state | To state | Trigger | Rules | Source (where status is set) |
|---|---|---|---|---|
| — | Pending | Funding request accepted | BR-WEB-020 | `walletRoutes.ts:58-67`, `packages/api/src/modules/payments/paymentsRoutes.ts:31-40` |
| Pending | Success | Simulated processing delay ends; wallet credited at the same moment | BR-WEB-020 | `walletRoutes.ts:72-81`, `paymentsRoutes.ts:46-55` |
| — | Success | Trade executed (created directly as Success) | BR-WEB-032 | `tradesRoutes.ts:69-78`, `tradesRoutes.ts:95-104` |
| any | Failed | **Never set by any code** | — | Q-DOM-003, D-WEB-003 |

::: mermaid
stateDiagram-v2
    [*] --> Pending : funding requested
    Pending --> Success : processing delay ends
    [*] --> Success : trade cash leg
    note right of Pending : No path to Failed. A crash during the delay leaves the transaction Pending forever (D-WEB-003)
:::
## Product comments
