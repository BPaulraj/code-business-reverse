> 🔄 **Generated** by the reverse-engineering kit from project `stockbroker` (code commit `ae607a6`, 2026-10-04, business view). **Do not edit this page**: changes are overwritten on the next publish. Give feedback through the review packs.

[[_TOC_]]

### BR-WEB-019 — Transaction history newest first

- **Statement:** The wallet transaction history lists all funding and trade transactions, newest first, with no paging or date filter.
- **Confidence:** High
- **Status:** Draft
- **Product comments:**

### BR-WEB-020 — Funding: Pending, then credited and Success

- **Statement:** When a client adds funds:
  1. A credit transaction is recorded as Pending.
  2. After a simulated processing time (bank transfer 1.5 s, debit card 0.8 s), the wallet is credited with the full amount and the transaction is marked Success. These two changes happen together.
  Funding never fails once the input is valid.
- **Trigger:** Add funds request.
- **Confidence:** High
- **Related:** D-WEB-003, Q-DOM-003
- **Status:** Draft
- **Product comments:**

### BR-WEB-021 — Only the last 4 digits of bank or card details are kept

- **Statement:** The transaction description records only the method and the last 4 digits, e.g. "Bank transfer from account ending 6789" or "Debit card ending 4242". The full account number, branch code, card number, expiry and CVV are not stored.
- **Confidence:** High
- **Status:** Draft
- **Product comments:**

### BR-WEB-022 — Funding confirmation message

- **Statement:** After successful funding, the client receives an inbox message "Funds added successfully" with the amount, the method and the new balance.
- **Confidence:** High
- **Status:** Draft
- **Product comments:**
