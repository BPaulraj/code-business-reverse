> 🔄 **Generated** by the reverse-engineering kit from project `stockbroker` (code commit `ae607a6`, 2026-10-04, business view). **Do not edit this page**: changes are overwritten on the next publish. Give feedback through the review packs.

[[_TOC_]]

### BR-WEB-023 — Trade history newest first, with invoice

- **Statement:** A client's trade history lists all their trades, newest first, each with its invoice link.
- **Confidence:** High
- **Status:** Draft
- **Product comments:**

### BR-WEB-024 — Trade must be for an existing company

- **Statement:** A trade for an unknown company is refused with "Company not found".
- **Confidence:** High
- **Status:** In review
- **Product comments:**

### BR-WEB-025 — Execution price set by the server at execution time

- **Statement:** A trade executes at a price the system determines at the moment of execution (a fresh simulated price). The price the client saw when building the order is not used and not checked.
- **Rationale (inferred):** Never trust a client-supplied price. The public API code states this explicitly (`packages/api/src/modules/trades/tradesRoutes.ts:35-36`).
- **Conditions / exceptions:** There is no maximum difference (slippage limit) between the quoted and executed price. With ±2% simulation, the gap can reach about 4%.
- **Confidence:** High
- **Related:** Q-WEB-001
- **Status:** In review
- **Product comments:**

### BR-WEB-026 — Trade total = price × quantity, rounded to the cent

- **Statement:** The trade total is execution price × quantity, rounded to the nearest cent.
- **Confidence:** High
- **Status:** In review
- **Product comments:**

### BR-WEB-027 — Buy rejected if wallet balance is insufficient

- **Statement:** A buy is refused if the wallet balance is less than the trade total. A balance exactly equal to the total is enough.
- **Outcome on violation:** "Insufficient wallet balance for this order"; nothing changes.
- **Confidence:** High
- **Status:** In review
- **Product comments:**

### BR-WEB-028 — Buy debits wallet and adds to holding at weighted average cost

- **Statement:** When a buy executes, the wallet is reduced by the trade total and the holding is updated:
  - **New holding:** quantity = shares bought, average cost = execution price.
  - **Existing holding:** quantity increases. New average cost = (old average cost × old quantity + trade total) ÷ new quantity.
- **Confidence:** High
- **Status:** In review
- **Product comments:**

### BR-WEB-029 — Sell rejected if client doesn't hold enough shares

- **Statement:** A sell is refused if the client holds none, or fewer shares than they want to sell. Short selling is not possible.
- **Outcome on violation:** "Insufficient holdings for this order"; nothing changes.
- **Confidence:** High
- **Status:** In review
- **Product comments:**

### BR-WEB-030 — Sell reduces holding; removed at zero; average cost unchanged

- **Statement:** When a sell executes, the holding quantity is reduced. If no shares remain, the holding is removed. The average cost of the remaining shares does not change.
- **Confidence:** High
- **Status:** In review
- **Product comments:**

### BR-WEB-031 — Sell credits the wallet with the trade total

- **Statement:** When a sell executes, the full trade total is added to the wallet immediately. There is no settlement delay.
- **Confidence:** High
- **Status:** In review
- **Product comments:**

### BR-WEB-032 — Every trade records a wallet transaction

- **Statement:** Every trade adds a wallet transaction with status Success and method Trade:
  - **Buy:** a Debit, described "Buy {qty} {ticker} @ ${price}"
  - **Sell:** a Credit, described "Sell {qty} {ticker} @ ${price}"
- **Confidence:** High
- **Status:** In review
- **Product comments:**

### BR-WEB-033 — Every trade is recorded as Completed with an invoice

- **Statement:** Every executed trade is recorded with status Completed, its execution price and total, and gets an invoice with a unique invoice number at the same moment.
- **Confidence:** High
- **Status:** In review
- **Product comments:**

### BR-WEB-034 — Trade updates are all-or-nothing

- **Statement:** For a trade, the balance check, the wallet change, the holding change, the wallet transaction, the trade record and the invoice either all happen or none happen.
- **Confidence:** High
- **Status:** In review
- **Product comments:**

### BR-WEB-035 — Two notifications after every trade

- **Statement:** After each trade the client receives two inbox messages:
  - **System, "Trade executed":** "Bought/Sold N share(s) of TICKER at $price for a total of $total."
  - **Invoice, "Invoice INV-… for your purchase/sale of TICKER":** linked to the invoice PDF.
- **Confidence:** High
- **Status:** In review
- **Product comments:**

### BR-WEB-036 — No fees or commission charged on trades

- **Statement:** Trades are charged no brokerage, commission or tax. The client pays or receives exactly price × quantity.
- **Confidence:** Medium. This is inferred from the absence of any fee logic.
- **Related:** Q-LIB-002
- **Status:** In review
- **Product comments:**
