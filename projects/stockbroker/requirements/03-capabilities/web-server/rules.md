# Web server — Business Rules

**Component:** `packages/server` · **Prefix:** `WEB` · **Capability:** [capability.md](capability.md) · **Endpoints:** [api-catalogue.md](api-catalogue.md)

> Most of these rules are **also implemented, by copy, in the Public API**. See the duplicate map in [public-api/rules.md](../public-api/rules.md).

## Summary

| ID | Title | Confidence | Status |
|---|---|---|---|
| BR-WEB-001 | Sign-in required for all client operations | High | Draft |
| BR-WEB-002 | Session lasts 7 days | High | Draft |
| BR-WEB-003 | Missing or expired session is rejected | High | Draft |
| BR-WEB-004 | Clients see and change only their own data | High | Draft |
| BR-WEB-005 | Another client's invoice or message is reported as not found | High | Draft |
| BR-WEB-006 | Invalid input is rejected with a message per field | High | Draft |
| BR-WEB-007 | Email must not already be registered | High | Draft |
| BR-WEB-008 | Wallet opened automatically at registration | High | Draft |
| BR-WEB-009 | Welcome message at registration | High | Draft |
| BR-WEB-010 | Client is signed in immediately after registering | High | Draft |
| BR-WEB-011 | Login failure gives one generic message | High | Draft |
| BR-WEB-012 | Logout ends the session on that browser | High | Draft |
| BR-WEB-013 | Clients may change only name, phone and address | High | Draft |
| BR-WEB-014 | Address can be cleared | Medium | Draft |
| BR-WEB-015 | Company search by ticker, name or sector, sorted by ticker | High | Draft |
| BR-WEB-016 | Company list shows a current simulated price | High | Draft |
| BR-WEB-017 | Dashboard contents | High | Draft |
| BR-WEB-018 | Dashboard total gain/loss % | High | Draft |
| BR-WEB-019 | Transaction history newest first | High | Draft |
| BR-WEB-020 | Funding: Pending, then credited and Success | High | Draft |
| BR-WEB-021 | Only the last 4 digits of bank or card details are kept | High | Draft |
| BR-WEB-022 | Funding confirmation message | High | Draft |
| BR-WEB-023 | Trade history newest first, with invoice | High | Draft |
| BR-WEB-024 | Trade must be for an existing company | High | In review |
| BR-WEB-025 | Execution price set by the server at execution time | High | In review |
| BR-WEB-026 | Trade total = price × quantity, rounded to the cent | High | In review |
| BR-WEB-027 | Buy rejected if wallet balance is insufficient | High | In review |
| BR-WEB-028 | Buy debits wallet and adds to holding at weighted average cost | High | In review |
| BR-WEB-029 | Sell rejected if client doesn't hold enough shares | High | In review |
| BR-WEB-030 | Sell reduces holding; removed at zero; average cost unchanged | High | In review |
| BR-WEB-031 | Sell credits the wallet with the trade total | High | In review |
| BR-WEB-032 | Every trade records a wallet transaction | High | In review |
| BR-WEB-033 | Every trade is recorded as Completed with an invoice | High | In review |
| BR-WEB-034 | Trade updates are all-or-nothing | High | In review |
| BR-WEB-035 | Two notifications after every trade | High | In review |
| BR-WEB-036 | No fees or commission charged on trades | Medium | In review |
| BR-WEB-037 | Invoice list, newest first | Medium | Draft |
| BR-WEB-038 | Invoice PDF downloadable only by the trade owner | High | Draft |
| BR-WEB-039 | Inbox newest first | High | Draft |
| BR-WEB-040 | Unread count | High | Draft |
| BR-WEB-041 | Client can mark a message read or unread | High | Draft |
| BR-WEB-042 | Passwords are stored only as a one-way hash and never returned | High | Draft |

---

## Cross-cutting

### BR-WEB-001 — Sign-in required for all client operations

- **Statement:** Every operation except registering, logging in and logging out requires the client to be signed in.
- **Outcome on violation:** "Not authenticated".
- **Source:** `packages/server/src/middleware/requireAuth.ts:10-14`. Applied at `companiesRoutes.ts:10`, `dashboardRoutes.ts:10`, `holdingsRoutes.ts:8`, `inboxRoutes.ts:11`, `invoicesRoutes.ts:10`, `tradesRoutes.ts:11`, `walletRoutes.ts:12`, `authRoutes.ts:89,101`
- **Confidence:** High
- **Technical note:** Duplicated in the front end as page redirects (BR-FO-001).
- **Status:** Draft
- **Product comments:**

### BR-WEB-002 — Session lasts 7 days

- **Statement:** After logging in or registering, a client stays signed in for 7 days. There is no inactivity timeout.
- **Source:** `packages/server/src/modules/auth/authRoutes.ts:14-24`
- **Confidence:** High
- **Technical note:** Signed token in an http-only, same-site cookie, marked secure in production.
- **Related:** Q-WEB-004, D-WEB-001
- **Status:** Draft
- **Product comments:**

### BR-WEB-003 — Missing or expired session is rejected

- **Statement:** A request with an invalid or expired session is refused with "Invalid or expired session".
- **Source:** `packages/server/src/middleware/requireAuth.ts:16-22`
- **Confidence:** High
- **Technical note:** Verifier 2026-10-04 removed "the portal then shows the login page". The portal redirects to login only when its "who am I" check fails (`packages/web/src/auth/AuthContext.tsx:21-33`, re-checked at most once a minute, and on page load). Until then, other screens just show errors.
- **Status:** Draft
- **Product comments:**

### BR-WEB-004 — Clients see and change only their own data

- **Statement:** A client can only see and act on their own wallet, transactions, holdings, trades, invoices and messages.
- **Source:** client filter in every query: `walletRoutes.ts:15,34`, `tradesRoutes.ts:17,40`, `dashboardRoutes.ts:18-21`, `invoicesRoutes.ts:16`, `inboxRoutes.ts:17,28`, `packages/db/src/services/holdingsService.ts:7`
- **Confidence:** High
- **Technical note:** There are no roles. There is no administrator or back-office access anywhere.
- **Status:** Draft
- **Product comments:**

### BR-WEB-005 — Another client's invoice or message is reported as not found

- **Statement:** If a client asks for an invoice or message that belongs to someone else, the system answers "not found". It does not reveal that the item exists.
- **Source:** `packages/server/src/modules/invoices/invoicesRoutes.ts:32-34`, `packages/server/src/modules/inbox/inboxRoutes.ts:39-42`
- **Confidence:** High
- **Status:** Draft
- **Product comments:**

### BR-WEB-006 — Invalid input is rejected with a message per field

- **Statement:** When submitted data breaks a validation rule, the request is refused with "Validation failed" and one message per invalid field (the first problem only).
- **Source:** `packages/server/src/middleware/errorHandler.ts:6-13`
- **Confidence:** High
- **Status:** Draft
- **Product comments:**

## Registration, login, profile

### BR-WEB-007 — Email must not already be registered

- **Statement:** Registration is refused if an account already exists with the same email (case-insensitive).
- **Outcome on violation:** "An account with this email already exists", shown against the email field.
- **Source:** `packages/server/src/modules/auth/authRoutes.ts:31-36`. Also enforced by the DB (BR-DB-001).
- **Confidence:** High
- **Technical note:** Telling the user that an email is registered allows account enumeration. Accepted for a demo?
- **Status:** Draft
- **Product comments:**

### BR-WEB-008 — Wallet opened automatically at registration

- **Statement:** Every new client gets a wallet with a zero balance at the moment of registration.
- **Source:** `authRoutes.ts:40-48`
- **Confidence:** High
- **Status:** Draft
- **Product comments:**

### BR-WEB-009 — Welcome message at registration

- **Statement:** A new client receives a "Welcome to StockBroker Demo" inbox message. It explains that the wallet is ready, that they should add funds to trade, and that no real money is involved.
- **Source:** `authRoutes.ts:50-55`
- **Confidence:** High
- **Status:** Draft
- **Product comments:**

### BR-WEB-010 — Client is signed in immediately after registering

- **Statement:** A successful registration signs the client in straight away. There is no email verification step.
- **Source:** `authRoutes.ts:57-58`
- **Confidence:** High
- **Status:** Draft
- **Product comments:**

### BR-WEB-011 — Login failure gives one generic message

- **Statement:** If the email is unknown or the password is wrong, login fails with the same message: "Invalid email or password". There is no limit on attempts.
- **Source:** `authRoutes.ts:67-75`
- **Confidence:** High
- **Related:** D-WEB-007
- **Status:** Draft
- **Product comments:**

### BR-WEB-012 — Logout ends the session on that browser

- **Statement:** Logging out removes the session from the client's browser.
- **Source:** `authRoutes.ts:82-85`
- **Confidence:** High
- **Technical note:** The token isn't revoked on the server (D-WEB-001).
- **Status:** Draft
- **Product comments:**

### BR-WEB-013 — Clients may change only name, phone and address

- **Statement:** A client can update their name, phone number and address. Email, KYC status and member-since date can't be changed by the client.
- **Source:** `authRoutes.ts:99-112`, `packages/shared/src/index.ts:215-225`
- **Confidence:** High
- **Technical note:** There is no password change, and no email change.
- **Status:** Draft
- **Product comments:**

### BR-WEB-014 — Address can be cleared

- **Statement:** A client can remove their address by saving it empty.
- **Source:** `packages/shared/src/index.ts:224` (no minimum length), `packages/web/src/pages/Profile.tsx:45`
- **Confidence:** Medium. It is saved as an empty text, not "no address", which may matter for invoices (`packages/db/src/services/invoicePdfService.ts:29`).
- **Status:** Draft
- **Product comments:**

## Market and portfolio

### BR-WEB-015 — Company search by ticker, name or sector, sorted by ticker

- **Statement:** Clients can search companies by any part of the ticker, name or sector. Results are listed alphabetically by ticker. An empty search lists all companies.
- **Source:** `packages/server/src/modules/companies/companiesRoutes.ts:15-24`
- **Confidence:** High
- **Related:** Q-WEB-003 (case sensitivity)
- **Status:** Draft
- **Product comments:**

### BR-WEB-016 — Company list shows a current simulated price

- **Statement:** Every company in the list shows a freshly simulated current price (BR-LIB-001).
- **Source:** `companiesRoutes.ts:26-32`
- **Confidence:** High
- **Status:** Draft
- **Product comments:**

### BR-WEB-017 — Dashboard contents

- **Statement:** The dashboard shows:
  - the wallet balance
  - the portfolio value (sum of the current value of all holdings)
  - total unrealised gain/loss and its %
  - each holding with its valuation
  - the 5 most recent trades
- **Source:** `packages/server/src/modules/dashboard/dashboardRoutes.ts:17-42`
- **Confidence:** High
- **Status:** Draft
- **Product comments:**

### BR-WEB-018 — Dashboard total gain/loss %

- **Statement:** Total gain/loss % = total gain/loss ÷ total cost of all holdings × 100. It is 0% when the client holds nothing.
- **Source:** `dashboardRoutes.ts:31-33`
- **Confidence:** High
- **Status:** Draft
- **Product comments:**

## Wallet and funding

### BR-WEB-019 — Transaction history newest first

- **Statement:** The wallet transaction history lists all funding and trade transactions, newest first, with no paging or date filter.
- **Source:** `packages/server/src/modules/wallet/walletRoutes.ts:29-39`
- **Confidence:** High
- **Status:** Draft
- **Product comments:**

### BR-WEB-020 — Funding: Pending, then credited and Success

- **Statement:** When a client adds funds:
  1. A credit transaction is recorded as Pending.
  2. After a simulated processing time (bank transfer 1.5 s, debit card 0.8 s), the wallet is credited with the full amount and the transaction is marked Success. These two changes happen together.
  Funding never fails once the input is valid.
- **Trigger:** Add funds request.
- **Source:** `walletRoutes.ts:47-81`
- **Confidence:** High
- **Related:** D-WEB-003, Q-DOM-003
- **Status:** Draft
- **Product comments:**

### BR-WEB-021 — Only the last 4 digits of bank or card details are kept

- **Statement:** The transaction description records only the method and the last 4 digits, e.g. "Bank transfer from account ending 6789" or "Debit card ending 4242". The full account number, branch code, card number, expiry and CVV are not stored.
- **Source:** `walletRoutes.ts:50-67` (only `description`, `method` and `amount` are saved)
- **Confidence:** High
- **Status:** Draft
- **Product comments:**

### BR-WEB-022 — Funding confirmation message

- **Statement:** After successful funding, the client receives an inbox message "Funds added successfully" with the amount, the method and the new balance.
- **Source:** `walletRoutes.ts:83-90`
- **Confidence:** High
- **Technical note:** Written after the funding is committed (see D-WEB-002).
- **Status:** Draft
- **Product comments:**

## Trading

### BR-WEB-023 — Trade history newest first, with invoice

- **Statement:** A client's trade history lists all their trades, newest first, each with its invoice link.
- **Source:** `packages/server/src/modules/trades/tradesRoutes.ts:13-23`
- **Confidence:** High
- **Status:** Draft
- **Product comments:**

### BR-WEB-024 — Trade must be for an existing company

- **Statement:** A trade for an unknown company is refused with "Company not found".
- **Source:** `tradesRoutes.ts:31-34`
- **Confidence:** High
- **Status:** In review
- **Product comments:**

### BR-WEB-025 — Execution price set by the server at execution time

- **Statement:** A trade executes at a price the system determines at the moment of execution (a fresh simulated price). The price the client saw when building the order is not used and not checked.
- **Rationale (inferred):** Never trust a client-supplied price. The public API code states this explicitly (`packages/api/src/modules/trades/tradesRoutes.ts:35-36`).
- **Conditions / exceptions:** There is no maximum difference (slippage limit) between the quoted and executed price. With ±2% simulation, the gap can reach about 4%.
- **Source:** `tradesRoutes.ts:36`, UI warning `packages/web/src/pages/Trade.tsx:273-276`
- **Confidence:** High
- **Related:** Q-WEB-001
- **Status:** In review
- **Product comments:**

### BR-WEB-026 — Trade total = price × quantity, rounded to the cent

- **Statement:** The trade total is execution price × quantity, rounded to the nearest cent.
- **Source:** `tradesRoutes.ts:37`
- **Confidence:** High
- **Status:** In review
- **Product comments:**

### BR-WEB-027 — Buy rejected if wallet balance is insufficient

- **Statement:** A buy is refused if the wallet balance is less than the trade total. A balance exactly equal to the total is enough.
- **Outcome on violation:** "Insufficient wallet balance for this order"; nothing changes.
- **Source:** `tradesRoutes.ts:47-52`
- **Confidence:** High
- **Technical note:** The check uses the execution price. The screen pre-checks with the quoted price (BR-FO-005), so a buy can pass the screen check and still fail here.
- **Status:** In review
- **Product comments:**

### BR-WEB-028 — Buy debits wallet and adds to holding at weighted average cost

- **Statement:** When a buy executes, the wallet is reduced by the trade total and the holding is updated:
  - **New holding:** quantity = shares bought, average cost = execution price.
  - **Existing holding:** quantity increases. New average cost = (old average cost × old quantity + trade total) ÷ new quantity.
- **Source:** `tradesRoutes.ts:54-67`
- **Confidence:** High
- **Status:** In review
- **Product comments:**

### BR-WEB-029 — Sell rejected if client doesn't hold enough shares

- **Statement:** A sell is refused if the client holds none, or fewer shares than they want to sell. Short selling is not possible.
- **Outcome on violation:** "Insufficient holdings for this order"; nothing changes.
- **Source:** `tradesRoutes.ts:80-84`
- **Confidence:** High
- **Status:** In review
- **Product comments:**

### BR-WEB-030 — Sell reduces holding; removed at zero; average cost unchanged

- **Statement:** When a sell executes, the holding quantity is reduced. If no shares remain, the holding is removed. The average cost of the remaining shares does not change.
- **Source:** `tradesRoutes.ts:86-91`
- **Confidence:** High
- **Technical note:** Realised profit or loss is not calculated or stored (Q-WEB-006).
- **Status:** In review
- **Product comments:**

### BR-WEB-031 — Sell credits the wallet with the trade total

- **Statement:** When a sell executes, the full trade total is added to the wallet immediately. There is no settlement delay.
- **Source:** `tradesRoutes.ts:93`
- **Confidence:** High
- **Status:** In review
- **Product comments:**

### BR-WEB-032 — Every trade records a wallet transaction

- **Statement:** Every trade adds a wallet transaction with status Success and method Trade:
  - **Buy:** a Debit, described "Buy {qty} {ticker} @ ${price}"
  - **Sell:** a Credit, described "Sell {qty} {ticker} @ ${price}"
- **Source:** `tradesRoutes.ts:69-78`, `tradesRoutes.ts:95-104`
- **Confidence:** High
- **Status:** In review
- **Product comments:**

### BR-WEB-033 — Every trade is recorded as Completed with an invoice

- **Statement:** Every executed trade is recorded with status Completed, its execution price and total, and gets an invoice with a unique invoice number at the same moment.
- **Source:** `tradesRoutes.ts:107-124`
- **Confidence:** High
- **Status:** In review
- **Product comments:**

### BR-WEB-034 — Trade updates are all-or-nothing

- **Statement:** For a trade, the balance check, the wallet change, the holding change, the wallet transaction, the trade record and the invoice either all happen or none happen.
- **Source:** `tradesRoutes.ts:39-127` (single database transaction)
- **Confidence:** High
- **Technical note:** The notifications (BR-WEB-035) are **outside** this unit (D-WEB-002).
- **Status:** In review
- **Product comments:**

### BR-WEB-035 — Two notifications after every trade

- **Statement:** After each trade the client receives two inbox messages:
  - **System, "Trade executed":** "Bought/Sold N share(s) of TICKER at $price for a total of $total."
  - **Invoice, "Invoice INV-… for your purchase/sale of TICKER":** linked to the invoice PDF.
- **Source:** `tradesRoutes.ts:129-146`
- **Confidence:** High
- **Status:** In review
- **Product comments:**

### BR-WEB-036 — No fees or commission charged on trades

- **Statement:** Trades are charged no brokerage, commission or tax. The client pays or receives exactly price × quantity.
- **Source:** `tradesRoutes.ts:37`, `:54`, `:93`. The fee appears on the invoice as illustrative only (BR-LIB-006).
- **Confidence:** Medium. This is inferred from the absence of any fee logic.
- **Related:** Q-LIB-002
- **Status:** In review
- **Product comments:**

## Invoices and inbox

### BR-WEB-037 — Invoice list, newest first

- **Statement:** A client can list all their invoices, newest first.
- **Source:** `packages/server/src/modules/invoices/invoicesRoutes.ts:12-22`
- **Confidence:** Medium. Reachability unconfirmed: no screen calls it (D-WEB-005).
- **Status:** Draft
- **Product comments:**

### BR-WEB-038 — Invoice PDF downloadable only by the trade owner

- **Statement:** An invoice PDF can be downloaded only by the client who placed the trade. It opens in the browser, named with the invoice number.
- **Source:** `invoicesRoutes.ts:24-43`
- **Confidence:** High
- **Status:** Draft
- **Product comments:**

### BR-WEB-039 — Inbox newest first

- **Statement:** The inbox lists all the client's messages, newest first. Messages can't be deleted.
- **Source:** `packages/server/src/modules/inbox/inboxRoutes.ts:13-22`
- **Confidence:** High
- **Status:** Draft
- **Product comments:**

### BR-WEB-040 — Unread count

- **Statement:** The unread count is the number of the client's messages not yet marked read.
- **Source:** `inboxRoutes.ts:24-32`
- **Confidence:** High
- **Status:** Draft
- **Product comments:**

### BR-WEB-041 — Client can mark a message read or unread

- **Statement:** A client can mark any of their own messages as read or unread.
- **Source:** `inboxRoutes.ts:34-51`
- **Confidence:** High
- **Status:** Draft
- **Product comments:**

## Data protection

### BR-WEB-042 — Passwords are stored only as a one-way hash and never returned

- **Statement:** A client's password is stored only as a one-way hash, never as readable text. The password and its hash are never included in any response.
- **Source:** `packages/server/src/modules/auth/authRoutes.ts:38-45` (hash on registration), `packages/server/src/modules/auth/authRoutes.ts:72` (compared on login), `packages/db/src/mappers/userMapper.ts:4-13` (client data returned without the password field)
- **Confidence:** High
- **Technical note:** Added 2026-10-04 after comparison with the Product Spec (AUTH-03). The extraction had noted this in the Client entity, but not as a reviewable rule. The public API does the same (`packages/api/src/modules/users/usersRoutes.ts:24`).
- **Status:** Draft
- **Product comments:**
