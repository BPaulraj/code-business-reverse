> 🔄 **Generated** by the reverse-engineering kit from project `stockbroker` (code commit `ae607a6`, 2026-10-04, business view). **Do not edit this page**: changes are overwritten on the next publish. Give feedback through the review packs.

[[_TOC_]]

**Status:** Draft · **Owner component:** Database seed (reference data) · **Stored in:** `Company`

## Definition

A listed company whose shares clients can trade. Company data is reference data. It is loaded by the seed script, and there is no screen or API to add, change or delist companies.

## Key attributes

| Attribute | Meaning | Format | Column | Source |
|---|---|---|---|---|
| Ticker | Exchange symbol, unique | e.g. `AAPL`, `BRK.B` | `ticker` | `packages/db/prisma/schema.prisma:50` |
| Name | Company name | text | `name` | `schema.prisma:51` |
| Sector | Industry group | text | `sector` | `schema.prisma:52` |
| Base price | Reference share price, USD. The simulated price moves ±2% around it. | decimal | `basePrice` | `schema.prisma:53`, `packages/db/src/services/priceService.ts:3-8` |

## Reference data

There are 41 companies across 8 sectors: Technology, Consumer Discretionary, Financials, Healthcare, Energy, Consumer Staples, Communication Services and Industrials (`packages/db/prisma/seed.ts:5-47`).
Re-running the seed updates the name, sector and base price of existing tickers (`seed.ts:51-55`).

## Lifecycle

None. Companies are static, with no listed/delisted/suspended state (Q-DOM-004).

## Product comments
