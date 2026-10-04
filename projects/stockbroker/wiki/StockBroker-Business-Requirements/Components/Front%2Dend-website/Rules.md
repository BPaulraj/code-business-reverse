> 🔄 **Generated** by the reverse-engineering kit from project `stockbroker` (code commit `ae607a6`, 2026-10-04, business view). **Do not edit this page**: changes are overwritten on the next publish. Give feedback through the review packs.

[[_TOC_]]

**Component:** `packages/web` · **Prefix:** `FO` · **Capability:** [capability.md](/Business-Requirements/StockBroker-Business-Requirements/Components/Front%2Dend-website) · **Journeys:** 05-user-journeys/front-office

## Summary

| ID | Title | Confidence | Status |
|---|---|---|---|
| BR-FO-001 | Signed-out visitors can reach only login and registration | High | Draft |
| BR-FO-002 | Registration form checks before submitting | High | Draft |
| BR-FO-003 | After login or registration the client lands on the dashboard | High | Draft |
| BR-FO-004 | Orders start from the company list with Buy or Sell | High | In review |
| BR-FO-005 | Order review checks quantity, balance and shares held | High | In review |
| BR-FO-006 | Two-step order: review, then confirm with price warning | High | In review |
| BR-FO-007 | Confirm button disabled while the trade executes | High | In review |
| BR-FO-008 | Company prices refresh every 15 seconds | High | Draft |
| BR-FO-009 | Trade success message shows executed price and total | High | Draft |
| BR-FO-010 | Funding form checks before submitting | High | Draft |
| BR-FO-011 | Add-funds button disabled while processing | High | Draft |
| BR-FO-012 | Transaction history display | High | Draft |
| BR-FO-013 | Profile screen: read-only and editable details | High | Draft |
| BR-FO-014 | Opening a message marks it read | High | Draft |
| BR-FO-015 | Unread badge refreshes every 30 seconds | High | Draft |
| BR-FO-016 | Invoice available from three places | High | Draft |
| BR-FO-017 | Demo-mode notice on key screens | High | Draft |

---

### BR-FO-001 — Signed-out visitors can reach only login and registration

- **Statement:**
  - A visitor who isn't signed in is sent to the login page from any other page.
  - A signed-in client who opens login or registration is sent to the dashboard.
  - Unknown addresses go to the dashboard (or to login if signed out).
- **Confidence:** High
- **Status:** Draft
- **Product comments:**

### BR-FO-002 — Registration form checks before submitting

- **Statement:** Before submitting, the registration screen checks:
  - name is not empty
  - email looks like an email
  - phone has at least 7 characters
  - password has at least 8 characters, including a letter and a number
  Server messages (e.g. email already registered) are shown against the field.
- **Confidence:** High
- **Status:** Draft
- **Product comments:**

### BR-FO-003 — After login or registration the client lands on the dashboard

- **Statement:** A successful login or registration takes the client to the dashboard. A failed login shows the server message.
- **Confidence:** High
- **Status:** Draft
- **Product comments:**

### BR-FO-004 — Orders start from the company list with Buy or Sell

- **Statement:** Every company row offers Buy and Sell. Sell is offered even if the client holds none of that company; the order is then stopped at review (BR-FO-005).
- **Confidence:** High
- **Status:** In review
- **Product comments:**

### BR-FO-005 — Order review checks quantity, balance and shares held

- **Statement:** When the client clicks "Review order", the screen refuses:
  - a quantity that is not a whole number above zero: "Enter a valid whole number of shares"
  - a buy whose estimated total (quoted price × quantity) exceeds the wallet balance: "Insufficient wallet balance for this order"
  - a sell of more shares than held: "Insufficient holdings for this order"
- **Confidence:** High
- **Status:** In review
- **Product comments:**

### BR-FO-006 — Two-step order: review, then confirm with price warning

- **Statement:** An order is placed in two steps:
  1. **Review:** shows the quantity, the quoted price per share and the estimated total.
  2. **Confirm:** the client must click "Confirm buy" or "Confirm sell".
  The screen warns that "the executed price is finalized at confirmation and may differ slightly from the quote". The client can go back or cancel.
- **Confidence:** High
- **Related:** BR-WEB-025, Q-WEB-001
- **Status:** In review
- **Product comments:**

### BR-FO-007 — Confirm button disabled while the trade executes

- **Statement:** After the client clicks Confirm, the button is disabled and shows "Executing trade…" until the result arrives. This prevents a double-click from placing two trades from this screen.
- **Confidence:** High
- **Status:** In review
- **Product comments:**

### BR-FO-008 — Company prices refresh every 15 seconds

- **Statement:** The company list re-fetches prices every 15 seconds while the Trade screen is open.
- **Confidence:** High
- **Status:** Draft
- **Product comments:**

### BR-FO-009 — Trade success message shows executed price and total

- **Statement:** After a successful trade, the screen shows "Bought/Sold N share(s) of TICKER at $price — total $total", using the **executed** price.
- **Confidence:** High
- **Status:** Draft
- **Product comments:**

### BR-FO-010 — Funding form checks before submitting

- **Statement:** Before submitting, the Payments screen checks:
  - the amount is a number above 0
  - **bank transfer:** account number of 6–18 digits, and an IFSC-style branch code
  - **debit card:** the card number passes the checksum, expiry is a valid MM/YY not in the past, CVV is 3–4 digits
- **Confidence:** High
- **Status:** Draft
- **Product comments:**

### BR-FO-011 — Add-funds button disabled while processing

- **Statement:** While funding is processing, the button is disabled and shows "Processing bank transfer…" or "Authorizing card…". The success message shows the amount added and the new balance.
- **Confidence:** High
- **Status:** Draft
- **Product comments:**

### BR-FO-012 — Transaction history display

- **Statement:** The transaction history shows the date, description, method, status (Success green, Pending amber, otherwise red) and amount. Credits are shown as "+", debits as "−".
- **Confidence:** High
- **Status:** Draft
- **Product comments:**

### BR-FO-013 — Profile screen: read-only and editable details

- **Statement:**
  - **Read-only:** email, member-since date, and KYC status, labelled "(mock — no real verification in this demo)".
  - **Editable:** name (required), phone (at least 7 characters) and address (optional).
- **Confidence:** High
- **Related:** Q-DOM-001
- **Status:** Draft
- **Product comments:**

### BR-FO-014 — Opening a message marks it read

- **Statement:** The inbox opens with the newest message selected. Viewing a message marks it read automatically. The client can toggle "Mark as read/unread". Invoice messages show a link to the invoice.
- **Confidence:** High
- **Status:** Draft
- **Product comments:**

### BR-FO-015 — Unread badge refreshes every 30 seconds

- **Statement:** The Inbox menu item shows a red badge with the unread count, refreshed every 30 seconds. It is hidden when the count is zero.
- **Confidence:** High
- **Status:** Draft
- **Product comments:**

### BR-FO-016 — Invoice available from three places

- **Statement:** A trade's invoice PDF can be opened in a new tab from the trade history, the dashboard's recent trades, and the invoice inbox message.
- **Confidence:** High
- **Status:** Draft
- **Product comments:**

### BR-FO-017 — Demo-mode notice on key screens

- **Statement:** A "Demo Mode — no real money" badge appears in the header of every signed-in page and on the login, registration and payments screens.
- **Confidence:** High
- **Status:** Draft
- **Product comments:**
