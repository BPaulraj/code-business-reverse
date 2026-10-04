> 🔄 **Generated** by the reverse-engineering kit from project `stockbroker` (code commit `ae607a6`, 2026-10-04, business view). **Do not edit this page**: changes are overwritten on the next publish. Give feedback through the review packs.

[[_TOC_]]

**Status:** Draft · **Owner component:** Web server / Public API · **Stored in:** `Trade`

## Definition

An executed instruction by a client to buy or sell a whole number of shares of one company. Execution is immediate, at a server-determined price. Only successful trades are stored.

## Key attributes

| Attribute | Meaning | Format | Column | Source |
|---|---|---|---|---|
| Type | Buy or Sell | `BUY` / `SELL` | `type` | `packages/shared/src/index.ts:16` |
| Quantity | Shares traded | whole number > 0 | `quantity` | `index.ts:259-262` |
| Price per share | Execution price | decimal (2 dp) | `pricePerShare` | `packages/server/src/modules/trades/tradesRoutes.ts:36` |
| Total | Price × quantity, rounded to the cent | decimal | `total` | `tradesRoutes.ts:37` |
| Status | Outcome | Completed / Failed | `status` | `index.ts:17` |
| Created at | Execution time | automatic | `createdAt` | `packages/db/prisma/schema.prisma:81` |

## Lifecycle

| From state | To state | Trigger | Rules | Source |
|---|---|---|---|---|
| — | Completed | Trade executed successfully | BR-WEB-033 | `tradesRoutes.ts:107-117` |
| — | Failed | **Never set.** A rejected or failed trade leaves no record. | — | Q-WEB-002 |

## Relationships

| Related entity | Relationship | Cardinality |
|---|---|---|
| [Client](/Business-Requirements/StockBroker-Business-Requirements/Domain-Model/ENT%2DClient-%E2%80%94-Client-account) | placed by | 1 |
| [Company](/Business-Requirements/StockBroker-Business-Requirements/Domain-Model/ENT%2DCompany-%E2%80%94-Listed-company) | of | 1 |
| [Invoice](/Business-Requirements/StockBroker-Business-Requirements/Domain-Model/ENT%2DInvoice-%E2%80%94-Trade-invoice) | documented by | 0..1 (always 1 in practice) |

## Product comments
