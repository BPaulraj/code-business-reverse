> 🔄 **Generated** by the reverse-engineering kit from project `stockbroker` (code commit `ae607a6`, 2026-10-04, business view). **Do not edit this page**: changes are overwritten on the next publish. Give feedback through the review packs.

[[_TOC_]]

**Component:** `packages/db/src/services`, `packages/db/src/mappers`, `packages/shared/src` · **Prefix:** `LIB` · **Tech:** TypeScript, Zod, pdfkit · **Last extracted:** 2026-10-04 · **Status:** Extracted

## Purpose

Business logic shared by the web server and the public API, plus the input-validation rules that the front end also reuses. It decides the market price, values portfolios, numbers invoices, renders invoice PDFs, and defines what valid client input looks like.

## Responsibilities

- Simulate the current market price of a share.
- Value a client's holdings: current value and unrealised gain/loss.
- Generate invoice numbers and invoice PDFs.
- Define the validation rules for registration, login, profile, funding and trade requests.
- Mask bank and card numbers to their last 4 digits.

## Not owned here

Trade execution, wallet updates and messaging are duplicated in the web server and the public API, not centralised here (D-API-001).

## Entry points

| # | Type | Name | Business meaning | Called by | Rules | Source |
|---|---|---|---|---|---|---|
| 1 | Function | `simulatePrice` | Current market price | WEB, API (companies, trades, holdings) | BR-LIB-001 | `packages/db/src/services/priceService.ts:5-9` |
| 2 | Function | `getHoldingsDto` | Value a client's holdings | WEB (dashboard, holdings), API (portfolio) | BR-LIB-002, 003 | `packages/db/src/services/holdingsService.ts:5-29` |
| 3 | Function | `generateInvoiceNumber` | Invoice reference | WEB, API (trades) | BR-LIB-004 | `packages/db/src/services/invoiceService.ts:3-5` |
| 4 | Function | `generateInvoicePdf` | Invoice document | WEB, API (invoices) | BR-LIB-005…007 | `packages/db/src/services/invoicePdfService.ts:5-78` |
| 5 | Function | `createInboxMessage` | Store a notification | WEB, API | — (mechanism only) | `packages/db/src/services/inboxService.ts:4-20` |
| 6 | Schemas | `registerSchema`, `loginSchema`, `updateProfileSchema`, `addFundsSchema`, `tradeSchema`, `updateMessageSchema` | Input validation | WEB, API; helpers reused by FO | BR-LIB-008…019 | `packages/shared/src/index.ts:192-267` |
| 7 | Function | `maskLast4`, `luhnCheck`, `isExpiryValid` | Card and account helpers | WEB, API, FO | BR-LIB-016, 017, 020 | `packages/shared/src/index.ts:149-185` |

## Configuration with business meaning

| Key | Business meaning | Value in repo | Production value known? |
|---|---|---|---|
| `MAX_FLUCTUATION` | Maximum simulated price movement around the base price | 0.02 (±2%) | Hard-coded (`priceService.ts:3`) |
| Fee rate (hard-coded) | Illustrative brokerage fee on the invoice | 0.1%, min $0.50 | Hard-coded (`invoicePdfService.ts:51`) |
| Funding limit (hard-coded) | Maximum per funding transaction | 1,000,000 | Hard-coded (`packages/shared/src/index.ts:230`) |

## Business rules

See [rules.md](/Business-Requirements/StockBroker-Business-Requirements/Components/Core-library/Rules). High 19 / Medium 1 / Low 0.


## Pages

[[_TOSP_]]
