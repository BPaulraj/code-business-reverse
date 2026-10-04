# Core library — Business Rules

**Component:** `packages/db/src/services`, `packages/shared/src` · **Prefix:** `LIB` · **Capability:** [capability.md](capability.md)

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
- **Source:** `packages/db/src/services/priceService.ts:1-9`
- **Confidence:** High
- **Technical note:** The same company can show different prices on two screens at the same moment. The UI text says prices "fluctuate slightly on refresh" (`packages/web/src/pages/Trade.tsx:94-95`).
- **Related:** BR-WEB-025, Q-WEB-001
- **Status:** In review
- **Product comments:**

### BR-LIB-002 — Empty holdings are not shown

- **Statement:** Only holdings with at least one share are included in the client's portfolio.
- **Source:** `packages/db/src/services/holdingsService.ts:6-9`
- **Confidence:** High
- **Technical note:** Fully sold holdings are deleted anyway (BR-WEB-030), so this is a safety filter.
- **Status:** Draft
- **Product comments:**

### BR-LIB-003 — Holding valuation and unrealised gain/loss

- **Statement:** For each holding:
  - current value = current price × quantity
  - cost = average cost × quantity
  - gain/loss = current value − cost
  - gain/loss % = gain/loss ÷ cost × 100, or 0% when cost is zero
- **Source:** `packages/db/src/services/holdingsService.ts:11-27`
- **Confidence:** High
- **Technical note:** It uses a freshly simulated price (BR-LIB-001), so gain/loss changes on every refresh. Realised gain/loss on sales is not calculated anywhere (Q-WEB-006).
- **Status:** Draft
- **Product comments:**

### BR-LIB-004 — Invoice number format

- **Statement:** An invoice number is "INV-" followed by the first 8 characters of the trade's reference, in upper case (e.g. INV-3F2A9C1B).
- **Rationale (inferred):** A human-readable reference with no separate counter.
- **Source:** `packages/db/src/services/invoiceService.ts:1-5`
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
- **Source:** `packages/db/src/services/invoicePdfService.ts:13-63`
- **Confidence:** High
- **Technical note:** The PDF is generated on demand from current client data. A client who changes their address afterwards will see the new address on old invoices.
- **Related:** Q-LIB-003
- **Status:** Draft
- **Product comments:**

### BR-LIB-006 — Brokerage fee shown on invoice but not charged

- **Statement:** The invoice shows an "illustrative brokerage fee" of 0.1% of the trade total, minimum $0.50, labelled "informational only — not charged". No fee is deducted from the wallet.
- **Source:** `packages/db/src/services/invoicePdfService.ts:49-59`. Trade total excludes fees: `packages/server/src/modules/trades/tradesRoutes.ts:37`.
- **Confidence:** High
- **Related:** Q-LIB-002
- **Status:** In review
- **Product comments:**

### BR-LIB-007 — Invoice carries a demo disclaimer

- **Statement:** Every invoice is marked "Simulated trade invoice — demo mode — no real money involved". The footer says it has no legal or financial validity.
- **Source:** `packages/db/src/services/invoicePdfService.ts:14-17`, `:65-74`
- **Confidence:** High
- **Status:** Draft
- **Product comments:**

### BR-LIB-008 — Password strength

- **Statement:** A password must be at least 8 characters and contain at least one letter and at least one digit.
- **Outcome on violation:** "Password must be at least 8 characters" / "Password must contain a letter" / "Password must contain a number".
- **Used in:** Registration (BR-WEB-007), BR-FO-002
- **Source:** `packages/shared/src/index.ts:192-196`
- **Confidence:** High
- **Technical note:** There is no maximum length and no password change or reset function.
- **Status:** Draft
- **Product comments:**

### BR-LIB-009 — Name required, max 100 characters

- **Statement:** The client's name is required (surrounding spaces ignored) and may be at most 100 characters.
- **Source:** `packages/shared/src/index.ts:199`, `:216`
- **Confidence:** High
- **Status:** Draft
- **Product comments:**

### BR-LIB-010 — Email must be valid and is case-insensitive

- **Statement:** The email must be a valid address. It is trimmed and converted to lower case before use, so "John@X.com" and "john@x.com" are the same account.
- **Source:** `packages/shared/src/index.ts:200`, `:211`
- **Confidence:** High
- **Status:** Draft
- **Product comments:**

### BR-LIB-011 — Phone number format

- **Statement:** A phone number must be 7–20 characters and may contain only digits, spaces, "+", "-", "(" and ")".
- **Source:** `packages/shared/src/index.ts:201-206`, `:217-223`
- **Confidence:** High
- **Related:** D-FO-001 (the screen checks only the minimum length)
- **Status:** Draft
- **Product comments:**

### BR-LIB-012 — Address optional, max 200 characters

- **Statement:** The address is optional and limited to 200 characters. It can only be set through the profile, not at registration.
- **Source:** `packages/shared/src/index.ts:224`, `:198-208` (address is not in the registration schema)
- **Confidence:** High
- **Status:** Draft
- **Product comments:**

### BR-LIB-013 — Funding amount limits

- **Statement:** A single funding amount must be greater than 0 and no more than 1,000,000.
- **Outcome on violation:** "Amount must be greater than 0" / "Amount is too large for a demo transaction".
- **Source:** `packages/shared/src/index.ts:227-230`
- **Confidence:** High
- **Technical note:** There is no daily or cumulative limit, and no minimum such as $1. The front end doesn't check the maximum (D-FO-002). The OpenAPI spec says the minimum is 0.01 (D-API-004).
- **Related:** Q-LIB-001
- **Status:** Draft
- **Product comments:**

### BR-LIB-014 — Bank account number format

- **Statement:** For bank transfers, the account number must be 6–18 digits.
- **Source:** `packages/shared/src/index.ts:235-238`
- **Confidence:** High
- **Status:** Draft
- **Product comments:**

### BR-LIB-015 — IFSC-style branch code format

- **Statement:** For bank transfers, the branch code must be 4 letters, then a zero, then 6 letters or digits (e.g. DEMO0123456). Lower case is accepted and converted to upper case.
- **Source:** `packages/shared/src/index.ts:146`, `:239`
- **Confidence:** High
- **Status:** Draft
- **Product comments:**

### BR-LIB-016 — Debit card number must pass checksum

- **Statement:** A debit card number must be 13–19 digits (spaces allowed) and pass the standard card checksum (Luhn).
- **Outcome on violation:** "Enter a valid card number" / "Card number failed validation".
- **Source:** `packages/shared/src/index.ts:149-165`, `:245-249`
- **Confidence:** High
- **Technical note:** Card brand and debit vs credit are not checked.
- **Status:** Draft
- **Product comments:**

### BR-LIB-017 — Debit card must not be expired

- **Statement:** The card expiry must be in MM/YY format and not earlier than the current month. A card expiring this month is accepted.
- **Outcome on violation:** "Enter expiry as MM/YY" / "Card has expired".
- **Source:** `packages/shared/src/index.ts:147`, `:167-180`, `:250`
- **Confidence:** High
- **Status:** Draft
- **Product comments:**

### BR-LIB-018 — CVV format

- **Statement:** The card CVV must be 3 or 4 digits.
- **Source:** `packages/shared/src/index.ts:251`
- **Confidence:** High
- **Technical note:** The CVV is validated, then discarded. It is never stored (BR-WEB-021).
- **Status:** Draft
- **Product comments:**

### BR-LIB-019 — Trade request: whole positive quantity, Buy or Sell

- **Statement:** A trade must name a company, be either Buy or Sell, and have a whole-number quantity of at least 1. There is no maximum quantity.
- **Outcome on violation:** "Company is required" / "Quantity must be a whole number" / "Quantity must be greater than 0".
- **Source:** `packages/shared/src/index.ts:256-263`
- **Confidence:** High
- **Technical note:** No order types (limit, stop), no fractional shares, no maximum order size.
- **Status:** In review
- **Product comments:**

### BR-LIB-020 — Card and account numbers shown as last 4 digits

- **Statement:** Wherever a bank account or card number is displayed or recorded, only its last 4 digits are used (left-padded with zeros if shorter).
- **Source:** `packages/shared/src/index.ts:182-185`, used at `packages/server/src/modules/wallet/walletRoutes.ts:51,54`
- **Confidence:** Medium. The padding case can't occur, because account numbers have at least 6 digits.
- **Status:** Draft
- **Product comments:**
