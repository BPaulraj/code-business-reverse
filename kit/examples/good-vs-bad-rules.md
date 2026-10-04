# Calibration: good vs bad rules

The examples are **fictitious** and only illustrate the quality bar. Paths and values are invented.

---

## ❌ Bad: describes code, not business

> **BR-CLI-004** — `ClientLockService.acquire()` calls `lockRepo.save()` with `ttl=30` and throws `ClientLockedException` if `findByClientId` returns a row.

Problems:
- The statement is written in code terms.
- The mechanism and the rule are mixed together.
- Product can't say yes or no to it.

## ✅ Good

### BR-CLI-004 — Only one trade at a time per client

- **Statement:** While a trade is being placed for a client, any other trade request for the same client is rejected.
- **Rationale (inferred):** Prevents duplicate trades, e.g. from a double-click on "Place order".
- **Trigger:** Trade placement request received for a client.
- **Conditions / exceptions:** Applies to all trade types found. No exemption in code.
- **Outcome on violation:** Request rejected with message "A trade is already in progress for this client".
- **Used in:** P-001, capability entry point #1
- **Source:**
  - `Code/Microservice/client service/src/main/java/.../ClientLockService.java:58-97` — lock check and rejection
  - `Code/Microservice/client service/src/main/resources/messages.properties:14` — message text
  - `Code/Microservice/client service/src/test/java/.../ClientLockServiceTest.java:40` — test `rejectsSecondTradeWhileLocked`
- **Confidence:** High
- **Technical note:** Implemented as a row in `CLIENT_LOCK`. The front-end also disables the button after the first click (`front-end/src/trade/PlaceOrder.tsx:31`), so the rule exists in two places.
- **Related:** BR-CLI-005, Q-CLI-002
- **Status:** Draft
- **Product comments:**

### BR-CLI-005 — Client lock expires after a timeout

- **Statement:** If a trade does not finish, the client's trade lock is released automatically after a configured time (30 seconds in the repo's default configuration).
- **Rationale (inferred):** Stops a client being blocked forever when a trade fails half-way.
- **Trigger:** Lock age exceeds the configured timeout.
- **Conditions / exceptions:** Timeout comes from config `client.lock.ttl-seconds`.
- **Outcome on violation:** n/a
- **Used in:** P-001
- **Source:** `.../ClientLockService.java:101-118`, `.../application.yml:22`
- **Confidence:** Medium. The production value of the timeout isn't in the repo.
- **Technical note:** Expiry is checked lazily on the next lock attempt, not by a background job.
- **Related:** Q-CLI-002 ("Is 30s the production value, and is auto-release intended?")
- **Status:** Draft
- **Product comments:**

---

## ❌ Bad: two decisions in one rule

> Cash transfer must be between ledgers of the same client and the amount must not exceed the available balance.

## ✅ Good: split into two rules

- **BR-CSH-010** — A cash transfer is allowed only between ledgers that belong to the same client.
- **BR-CSH-011** — A cash transfer is rejected if the amount exceeds the source ledger's available balance.

---

## ❌ Bad: guess presented as fact

> **BR-STK-003** — Stock is credited to the vault at settlement date. *(Confidence: High)*

The code only shows a field called `settleDt` being set. No logic uses it.

## ✅ Good: guess presented as a guess

- **BR-STK-003** — Stock credit appears to be recorded with a settlement date, but no code found applies the credit on that date.
  - **Confidence:** Low
  - **Related:** Q-STK-001 ("Is stock credited immediately on trade, or on settlement date? The code credits immediately (`path:line`) and only stores the settlement date.")

---

## ❌ Bad batch rule: SQL copied, not translated

> **BR-BAT-012-01** — Job selects from `CLNT_ACCT a JOIN CASH_BAL b` where `a.STS_CD IN ('A','S') AND b.AVL_BAL < 0 AND a.LST_TXN_DT < :bizDt - 30`.

## ✅ Good batch rules: one business condition each

- **BR-BAT-012-01** — The nightly overdraft-fee job considers only clients whose account is Active or Suspended. Closed and Pending accounts are never charged.
- **BR-BAT-012-02** — A client is charged an overdraft fee only if their available cash balance is below zero at end of the business day.
- **BR-BAT-012-03** — Clients with any transaction in the last 30 calendar days are excluded from the overdraft fee.
  - **Confidence:** High for the logic.
  - **Technical note:** "30 days" is hard-coded and calendar-based, not business days. The inner join means clients with no cash-balance row are silently skipped (see D-BAT-012-01).
  - **Related:** Q-BAT-012-01 ("Calendar or business days intended?")
- **D-BAT-012-01** — The job does not prevent double charging on a re-run for the same business date. No "already charged" check was found (`OverdraftFeeWriter.java:40-71`).

---

## ❌ Bad web-service rule: describes plumbing

> **BR-API-007** — `TradeController.post()` calls `clientClient.lock()`, then `cashClient.move()`, then `stockClient.debit()`.

## ✅ Good web-service rules

- **BR-API-007** — When a trade is placed, the cash movement is made before the stock movement. If the cash movement fails, no stock is moved and the client lock is released.
- **BR-API-008** — If the stock movement fails after cash has moved, the cash movement is **not** reversed automatically (see D-API-003).
  - **Confidence:** High
- **BR-API-009** — A front-office user can only place trades for clients linked to their own login.
  - **Source:** `ClientScopeFilter.java:22-40`
  - **Technical note:** Enforced only in the web-services layer; the downstream services don't check it.

---

## ✅ Special case: rule plus defect

- **BR-CSH-020** — Transfers for client account 100045 skip the available-balance check.
  - **Confidence:** High
  - **Related:** D-CSH-004
- **D-CSH-004** — A hard-coded client ID bypasses the balance check (`CashTransferService.java:212`). Was this intended? Is the client still active?
