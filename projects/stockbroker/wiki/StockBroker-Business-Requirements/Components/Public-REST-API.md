> 🔄 **Generated** by the reverse-engineering kit from project `stockbroker` (code commit `ae607a6`, 2026-10-04, business view). **Do not edit this page**: changes are overwritten on the next publish. Give feedback through the review packs.

[[_TOC_]]

**Component:** `packages/api` · **Prefix:** `API` · **Tech:** Node, Express 4, Zod, JWT bearer, Swagger UI · **Last extracted:** 2026-10-04 · **Status:** Extracted

## Purpose

Offers the platform's core client operations to external client applications through a documented, token-based REST API, without using the web portal. These operations are registration, login, profile, companies, portfolio, funding, trading, invoices and inbox reading.

## Responsibilities

- Token-based registration and login (BR-API-001).
- The same business rules as the web server for funding, trading, profile and data access. **They are implemented by copy, not shared** (D-API-001).
- Portfolio summary with total account value (BR-API-003).
- Invoice lookup by trade reference (BR-API-004).
- Published OpenAPI contract and interactive docs.

## Not owned here

- The rules themselves are documented once, in [web-server/rules.md](/Business-Requirements/StockBroker-Business-Requirements/Components/Web-server/Rules) and [core-library/rules.md](/Business-Requirements/StockBroker-Business-Requirements/Components/Core-library/Rules).
- This component's [rules.md](/Business-Requirements/StockBroker-Business-Requirements/Components/Public-REST-API/Rules) maps the duplicates and adds only the API-specific rules.

## Entry points

See [api-catalogue.md](/Business-Requirements/StockBroker-Business-Requirements/Components/Public-REST-API/API-Catalogue): 15 business operations, plus docs and health.

## Dependencies

| Depends on | Why | How | Source |
|---|---|---|---|
| Core library | Price, valuation, invoice, validation, messaging | Import | `packages/api/src/modules/trades/tradesRoutes.ts:2-3` |
| Shared database | Persistence, shared with the web server | Prisma | `packages/api/src/modules/trades/tradesRoutes.ts:3` |

## Configuration with business meaning

| Key | Business meaning | Value in repo | Production value known? |
|---|---|---|---|
| Token lifetime (hard-coded) | How long an API token is valid | 7 days | `packages/api/src/lib/token.ts:4` |
| `PORT` | API address | 4100 | No |

## Business rules

See [rules.md](/Business-Requirements/StockBroker-Business-Requirements/Components/Public-REST-API/Rules): 7 API-specific rules (High 6 / Medium 1) and 29 rules duplicated from the web server.


## Pages

[[_TOSP_]]
