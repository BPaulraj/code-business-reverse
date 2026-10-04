> 🔄 **Generated** by the reverse-engineering kit from project `stockbroker` (code commit `ae607a6`, 2026-10-04, business view). **Do not edit this page**: changes are overwritten on the next publish. Give feedback through the review packs.

[[_TOC_]]

### BR-WEB-015 — Company search by ticker, name or sector, sorted by ticker

- **Statement:** Clients can search companies by any part of the ticker, name or sector. Results are listed alphabetically by ticker. An empty search lists all companies.
- **Confidence:** High
- **Related:** Q-WEB-003 (case sensitivity)
- **Status:** Draft
- **Product comments:**

### BR-WEB-016 — Company list shows a current simulated price

- **Statement:** Every company in the list shows a freshly simulated current price (BR-LIB-001).
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
- **Confidence:** High
- **Status:** Draft
- **Product comments:**

### BR-WEB-018 — Dashboard total gain/loss %

- **Statement:** Total gain/loss % = total gain/loss ÷ total cost of all holdings × 100. It is 0% when the client holds nothing.
- **Confidence:** High
- **Status:** Draft
- **Product comments:**
