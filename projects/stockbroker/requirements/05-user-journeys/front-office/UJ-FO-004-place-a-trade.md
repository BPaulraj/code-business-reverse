# UJ-FO-004 — Buy or sell shares

**Status:** Draft · **Application:** Front-office · **Last extracted:** 2026-10-04

## Actor and goal

- **Role(s):** Any signed-in client. There are no roles (BR-WEB-004).
- **Goal:** Buy or sell a whole number of shares of a listed company.
- **Entry:** Menu "Trade" → `/trade` (`packages/web/src/components/Layout.tsx:9`, `packages/web/src/App.tsx:25`)

## Steps

| # | Screen | User action | System response | Validations / rules | Backend call | Source |
|---|---|---|---|---|---|---|
| 1 | Trade | Opens the Trade screen | Shows the company list with current prices, refreshed every 15 s, plus the client's trade history | BR-WEB-015, 016, BR-FO-008 | `GET /api/companies`, `GET /api/trades` ([catalogue #8, #12](../../03-capabilities/web-server/api-catalogue.md)) | `packages/web/src/pages/Trade.tsx:13-19` |
| 2 | Trade | Types in search | The list filters by ticker, name or sector | BR-WEB-015 | `GET /api/companies?search=` | `Trade.tsx:106-112` |
| 3 | Trade | Clicks Buy or Sell on a company | The order panel opens with the company, the current price, the wallet balance, and (for Sell) shares held | BR-FO-004 | `GET /api/wallet`, `GET /api/holdings` | `Trade.tsx:37-44`, `:208-243` |
| 4 | Order panel | Enters a quantity and clicks "Review order" | Shows the estimated total, or an error | BR-FO-005 | — | `Trade.tsx:46-63` |
| 5 | Confirm panel | Reads the quote and warning, clicks "Confirm buy/sell" | The button shows "Executing trade…" and is disabled | BR-FO-006, 007 | `POST /api/trades` (catalogue #13) | `Trade.tsx:65-86`, `:251-284` |
| 6 | Trade | — | Success message with the executed price and total. Balance, holdings, history and dashboard refresh. The two inbox messages arrive. | BR-FO-009, BR-WEB-025…035 | — | `Trade.tsx:74-81`, `packages/web/src/api/trades.ts:16-21` |
| 6a | Trade | — | On error: back to the order form with the server message, e.g. insufficient balance at the execution price | BR-WEB-027, 029 | — | `Trade.tsx:82-85` |

## Validations shown to the user

| Field / action | Rule | Message shown | Also enforced server-side? | Source |
|---|---|---|---|---|
| Quantity | Whole number > 0 | "Enter a valid whole number of shares" | Yes (BR-LIB-019) | `Trade.tsx:50-53` |
| Buy | Estimated total ≤ wallet balance | "Insufficient wallet balance for this order" | Yes, but at the execution price (D-WEB-006) | `Trade.tsx:54-57` |
| Sell | Quantity ≤ shares held | "Insufficient holdings for this order" | Yes (BR-WEB-029) | `Trade.tsx:58-61` |

## Permissions

| Action | Allowed roles | Source |
|---|---|---|
| View companies, trade | Any signed-in client | BR-FO-001, BR-WEB-001 |

## Related

P-001, Q-WEB-001, D-FO-003, D-WEB-004

## Product comments
