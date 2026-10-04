# ENT-Trade — Trade

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
| [Client](client.md) | placed by | 1 |
| [Company](company.md) | of | 1 |
| [Invoice](invoice.md) | documented by | 0..1 (always 1 in practice) |

## Product comments
