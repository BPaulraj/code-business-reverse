> 🔄 **Generated** by the reverse-engineering kit from project `stockbroker` (code commit `ae607a6`, 2026-10-04, business view). **Do not edit this page**: changes are overwritten on the next publish. Give feedback through the review packs.

[[_TOC_]]

**Status:** Draft · **Last traced:** 2026-10-04 · **Components involved:** Front-end, Web server (or Public API), Core library, Shared database

## Goal

A client buys or sells a whole number of shares of a listed company. Cash and holdings change immediately, and the trade is documented with an invoice and notifications.

## Actors and triggers

- **Initiated by:** A signed-in client.
- **Entry point(s):**
  - Portal: "Confirm buy/sell" on the Trade screen → `POST /api/trades` (`packages/web/src/pages/Trade.tsx:65-73`, `packages/server/src/modules/trades/tradesRoutes.ts:25`)
  - Public API: `POST /api/v1/trades` (`packages/api/src/modules/trades/tradesRoutes.ts:24`). Same logic, copied (D-API-001).

## Preconditions

- The client is signed in (BR-WEB-001).
- **Buy:** the wallet has enough cash at the execution price (BR-WEB-027).
- **Sell:** the client holds at least the quantity to sell (BR-WEB-029).
- **Not required:** KYC verification is not checked (Q-WEB-005), and there are no market hours.

## Main flow (happy path)

| Step | Actor / component | What happens (business terms) | Rules applied | Source |
|---|---|---|---|---|
| 1 | Front-end | The client picks a company and Buy or Sell. The screen shows the **quoted** price (simulated ±2%). | BR-FO-004, BR-LIB-001 | `Trade.tsx:37-44` |
| 2 | Front-end | The client enters a quantity and clicks Review. The screen pre-checks quantity, balance (at the quote) and shares held. | BR-FO-005 | `Trade.tsx:46-63` |
| 3 | Front-end | The client confirms. The button is disabled during execution. | BR-FO-006, BR-FO-007 | `Trade.tsx:251-284` |
| 4 | Web server | Checks the request: company, Buy/Sell, whole quantity ≥ 1 | BR-LIB-019, BR-WEB-006 | `tradesRoutes.ts:28` |
| 5 | Web server | Checks that the company exists | BR-WEB-024 | `tradesRoutes.ts:31-34` |
| 6 | Web server + Core library | Draws a **new** price, which becomes the execution price. Total = price × quantity, rounded to the cent. | BR-WEB-025, BR-WEB-026, BR-LIB-001 | `tradesRoutes.ts:36-37` |
| 7 | Web server (one DB transaction) | **Buy:** check balance → debit wallet → add to holding (weighted average cost) → record a Debit wallet transaction | BR-WEB-027, 028, 032 | `tradesRoutes.ts:47-78` |
| 7′ | Web server (same transaction) | **Sell:** check shares held → reduce holding (remove it at zero) → credit wallet → record a Credit wallet transaction | BR-WEB-029, 030, 031, 032 | `tradesRoutes.ts:79-105` |
| 8 | Web server (same transaction) | Record the trade as Completed. Create the invoice (INV-xxxxxxxx). | BR-WEB-033, BR-LIB-004, BR-DB-004/005 | `tradesRoutes.ts:107-124` |
| 9 | — | Steps 7–8 commit together | BR-WEB-034 | `tradesRoutes.ts:39-127` |
| 10 | Web server | Send the "Trade executed" message, then the invoice message with its link | BR-WEB-035 | `tradesRoutes.ts:129-146` |
| 11 | Front-end | Show the success message with the executed price and total. Refresh balance, holdings, history and dashboard. | BR-FO-009 | `Trade.tsx:74-81`, `packages/web/src/api/trades.ts:16-21` |

## Alternative and failure paths

| At step | Condition | What happens | State left behind / compensation | Rules | Source |
|---|---|---|---|---|---|
| 2 | Invalid quantity, or balance/holding short at the quote | Error on screen; nothing is sent | None | BR-FO-005 | `Trade.tsx:50-61` |
| 4 | Invalid request (API callers mostly) | "Validation failed" with field messages | None | BR-WEB-006 | `packages/server/src/middleware/errorHandler.ts:6-13` |
| 5 | Unknown company | "Company not found" | None | BR-WEB-024 | |
| 7 | Buy: balance < total at the **execution** price (can happen even after the screen check passed) | "Insufficient wallet balance for this order" | None (rolled back) | BR-WEB-027, D-WEB-006 | `tradesRoutes.ts:48-52` |
| 7′ | Sell: not enough shares (e.g. sold meanwhile in another tab or via the API) | "Insufficient holdings for this order" | None (rolled back) | BR-WEB-029 | `tradesRoutes.ts:80-84` |
| 8 | Invoice number collision (rare) | "Internal server error" | None (whole trade rolled back) | D-LIB-001 | |
| 7–8 | Database busy for over 5 s (web server and API writing together) | "Internal server error" | None (rolled back) | D-DB-002 | `packages/db/src/prisma.ts:20` |
| 10 | **Notification write fails after commit** | The client sees "Internal server error", **but the trade has been executed** | The trade, cash and holding are changed, but messages are missing. The client may retry and trade twice. | D-WEB-002, D-WEB-004 | `tradesRoutes.ts:129-146` |

## Concurrency and timing

- **Double-click:** prevented only in the browser (BR-FO-007). The server has no duplicate check, idempotency key or per-client lock (D-WEB-004). API clients have no protection at all (D-API-005).
- **Two trades at once for the same client** (two tabs, or portal plus API): each runs in its own database transaction, and SQLite serialises writes, so the balance and holding checks stay correct. On a production database this would need re-checking (D-DB-002).
- **Price timing:** the quote and the execution price are drawn independently. Within ±2% each, they can differ by up to about 4%, with no tolerance check (Q-WEB-001).
- **Settlement:** immediate. Cash and shares move at execution. There is no T+1/T+2 settlement and no market hours.

## Postconditions

- **Buy:**
  - wallet reduced by the total
  - holding created or increased, with average cost re-weighted
  - Debit transaction recorded (Success)
  - trade recorded (Completed), invoice created
  - two inbox messages sent
- **Sell:**
  - wallet increased by the total
  - holding reduced or removed, average cost unchanged
  - Credit transaction recorded (Success)
  - trade recorded (Completed), invoice created
  - two inbox messages sent

## Sequence diagram

::: mermaid
sequenceDiagram
    actor Client
    participant FE as Front-end (Trade screen)
    participant WS as Web server
    participant LIB as Core library
    participant DB as Shared database
    Client->>FE: Buy/Sell, quantity, Review
    FE->>FE: Pre-check quantity, balance (quote), shares held
    Client->>FE: Confirm (button disabled)
    FE->>WS: POST /api/trades {company, type, quantity}
    WS->>DB: Company exists?
    WS->>LIB: simulatePrice() → execution price
    rect rgb(235, 245, 255)
    note over WS,DB: Single DB transaction
    WS->>DB: Read wallet and holding
    alt Buy
        WS->>DB: Check balance ≥ total, debit wallet, add holding, Debit txn
    else Sell
        WS->>DB: Check held ≥ qty, reduce/remove holding, credit wallet, Credit txn
    end
    WS->>DB: Trade (Completed) + Invoice (INV-…)
    end
    WS->>DB: Inbox "Trade executed" (outside transaction)
    WS->>DB: Inbox invoice message (outside transaction)
    WS-->>FE: 201 Trade (executed price, total, invoice)
    FE-->>Client: Success message, refreshed balances
:::
## Overnight continuation

None. There are no batch jobs, and no settlement, statement or reporting run follows the trade.

## Gaps

- **No order types** (limit, stop, cancel), **no fees** (Q-LIB-002), **no realised P&L** (Q-WEB-006), **no failed-trade record** (Q-WEB-002).
- Public API consumers are unknown (Q-API-001).

## Product comments
