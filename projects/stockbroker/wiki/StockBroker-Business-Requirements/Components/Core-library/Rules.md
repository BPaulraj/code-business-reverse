> 🔄 **Generated** by the reverse-engineering kit from project `stockbroker` (code commit `ae607a6`, 2026-10-04, business view). **Do not edit this page**: changes are overwritten on the next publish. Give feedback through the review packs.

[[_TOC_]]

**Component:** `packages/db/src/services`, `packages/shared/src` · **Prefix:** `LIB` · **Capability:** [capability.md](/Business-Requirements/StockBroker-Business-Requirements/Components/Core-library)

## Summary

| ID | Title | Confidence | Status |
|---|---|---|---|
| BR-LIB-001 | Market price is simulated within ±2% of base price | High | In review |
| BR-LIB-002 | Empty holdings are not shown | High | Draft |
| BR-LIB-003 | Holding valuation and unrealised gain/loss | High | Draft |
| BR-LIB-004 | Invoice number format | High | In review |
| BR-LIB-005 | Invoice content | High | Draft |
| BR-LIB-006 | Brokerage fee shown on invoice but not charged | High | In review |
| BR-LIB-007 | Invoice carries a demo disclaimer | High | Draft |
| BR-LIB-008 | Password strength | High | Draft |
| BR-LIB-009 | Name required, max 100 characters | High | Draft |
| BR-LIB-010 | Email must be valid and is case-insensitive | High | Draft |
| BR-LIB-011 | Phone number format | High | Draft |
| BR-LIB-012 | Address optional, max 200 characters | High | Draft |
| BR-LIB-013 | Funding amount limits | High | Draft |
| BR-LIB-014 | Bank account number format | High | Draft |
| BR-LIB-015 | IFSC-style branch code format | High | Draft |
| BR-LIB-016 | Debit card number must pass checksum | High | Draft |
| BR-LIB-017 | Debit card must not be expired | High | Draft |
| BR-LIB-018 | CVV format | High | Draft |
| BR-LIB-019 | Trade request: whole positive quantity, Buy or Sell | High | In review |
| BR-LIB-020 | Card and account numbers shown as last 4 digits | Medium | Draft |

---

### BR-LIB-001 — Market price is simulated within ±2% of base price

- **Statement:** A company's current share price is its base price adjusted by a random amount of up to ±2%, rounded to the cent. A new price is drawn every time a price is needed: each listing refresh, each portfolio valuation, and each trade execution.
- **Rationale (inferred):** Imitates live market movement without a market-data feed.
- **Trigger:** Any price lookup.
- **Conditions / exceptions:** No market hours, no trend. The price always stays within ±2% of base, so it never drifts.
- **Confidence:** High
- **Related:** BR-WEB-025, Q-WEB-001
- **Status:** In review
- **Product comments:**

### BR-LIB-002 — Empty holdings are not shown

- **Statement:** Only holdings with at least one share are included in the client's portfolio.
- **Confidence:** High
- **Status:** Draft
- **Product comments:**

### BR-LIB-003 — Holding valuation and unrealised gain/loss

- **Statement:** For each holding:
  - current value = current price × quantity
  - cost = average cost × quantity
  - gain/loss = current value − cost
  - gain/loss % = gain/loss ÷ cost × 100, or 0% when cost is zero
- **Confidence:** High
- **Status:** Draft
- **Product comments:**

### BR-LIB-004 — Invoice number format

- **Statement:** An invoice number is "INV-" followed by the first 8 characters of the trade's reference, in upper case (e.g. INV-3F2A9C1B).
- **Rationale (inferred):** A human-readable reference with no separate counter.
- **Confidence:** High
- **Related:** D-LIB-001
- **Status:** In review
- **Product comments:**

### BR-LIB-005 — Invoice content

- **Statement:** The invoice PDF shows:
  - the invoice number and date
  - "Bill To": client name, email, phone, and address if present
  - one line: trade type, ticker and company name, quantity, price per share, amount
  - the total amount in USD with 2 decimals
- **Confidence:** High
- **Related:** Q-LIB-003
- **Status:** Draft
- **Product comments:**

### BR-LIB-006 — Brokerage fee shown on invoice but not charged

- **Statement:** The invoice shows an "illustrative brokerage fee" of 0.1% of the trade total, minimum $0.50, labelled "informational only — not charged". No fee is deducted from the wallet.
- **Confidence:** High
- **Related:** Q-LIB-002
- **Status:** In review
- **Product comments:**

### BR-LIB-007 — Invoice carries a demo disclaimer

- **Statement:** Every invoice is marked "Simulated trade invoice — demo mode — no real money involved". The footer says it has no legal or financial validity.
- **Confidence:** High
- **Status:** Draft
- **Product comments:**

### BR-LIB-008 — Password strength

- **Statement:** A password must be at least 8 characters and contain at least one letter and at least one digit.
- **Outcome on violation:** "Password must be at least 8 characters" / "Password must contain a letter" / "Password must contain a number".
- **Used in:** Registration (BR-WEB-007), BR-FO-002
- **Confidence:** High
- **Status:** Draft
- **Product comments:**

### BR-LIB-009 — Name required, max 100 characters

- **Statement:** The client's name is required (surrounding spaces ignored) and may be at most 100 characters.
- **Confidence:** High
- **Status:** Draft
- **Product comments:**

### BR-LIB-010 — Email must be valid and is case-insensitive

- **Statement:** The email must be a valid address. It is trimmed and converted to lower case before use, so "John@X.com" and "john@x.com" are the same account.
- **Confidence:** High
- **Status:** Draft
- **Product comments:**

### BR-LIB-011 — Phone number format

- **Statement:** A phone number must be 7–20 characters and may contain only digits, spaces, "+", "-", "(" and ")".
- **Confidence:** High
- **Related:** D-FO-001 (the screen checks only the minimum length)
- **Status:** Draft
- **Product comments:**

### BR-LIB-012 — Address optional, max 200 characters

- **Statement:** The address is optional and limited to 200 characters. It can only be set through the profile, not at registration.
- **Confidence:** High
- **Status:** Draft
- **Product comments:**

### BR-LIB-013 — Funding amount limits

- **Statement:** A single funding amount must be greater than 0 and no more than 1,000,000.
- **Outcome on violation:** "Amount must be greater than 0" / "Amount is too large for a demo transaction".
- **Confidence:** High
- **Related:** Q-LIB-001
- **Status:** Draft
- **Product comments:**

### BR-LIB-014 — Bank account number format

- **Statement:** For bank transfers, the account number must be 6–18 digits.
- **Confidence:** High
- **Status:** Draft
- **Product comments:**

### BR-LIB-015 — IFSC-style branch code format

- **Statement:** For bank transfers, the branch code must be 4 letters, then a zero, then 6 letters or digits (e.g. DEMO0123456). Lower case is accepted and converted to upper case.
- **Confidence:** High
- **Status:** Draft
- **Product comments:**

### BR-LIB-016 — Debit card number must pass checksum

- **Statement:** A debit card number must be 13–19 digits (spaces allowed) and pass the standard card checksum (Luhn).
- **Outcome on violation:** "Enter a valid card number" / "Card number failed validation".
- **Confidence:** High
- **Status:** Draft
- **Product comments:**

### BR-LIB-017 — Debit card must not be expired

- **Statement:** The card expiry must be in MM/YY format and not earlier than the current month. A card expiring this month is accepted.
- **Outcome on violation:** "Enter expiry as MM/YY" / "Card has expired".
- **Confidence:** High
- **Status:** Draft
- **Product comments:**

### BR-LIB-018 — CVV format

- **Statement:** The card CVV must be 3 or 4 digits.
- **Confidence:** High
- **Status:** Draft
- **Product comments:**

### BR-LIB-019 — Trade request: whole positive quantity, Buy or Sell

- **Statement:** A trade must name a company, be either Buy or Sell, and have a whole-number quantity of at least 1. There is no maximum quantity.
- **Outcome on violation:** "Company is required" / "Quantity must be a whole number" / "Quantity must be greater than 0".
- **Confidence:** High
- **Status:** In review
- **Product comments:**

### BR-LIB-020 — Card and account numbers shown as last 4 digits

- **Statement:** Wherever a bank account or card number is displayed or recorded, only its last 4 digits are used (left-padded with zeros if shorter).
- **Confidence:** Medium. The padding case can't occur, because account numbers have at least 6 digits.
- **Status:** Draft
- **Product comments:**
