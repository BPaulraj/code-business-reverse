# Kit trial — extraction accuracy vs the Product Spec

**Purpose:** a calibration exercise for the reverse-engineering kit, not a product review pack.
**Method:**
- The requirements were extracted from code only. `Docs/` and `README.md` were not read.
- Afterwards, the result was compared with `Docs/StockBroker Product Spec.pdf` (v1.0), which plays the role of a "product team" that already knows the answers.

## 1. Recall: did the extraction find the spec's rules?

| Spec rule | Spec statement (short) | Extracted as | Match |
|---|---|---|---|
| AUTH-01 | Email unique, lower-cased | BR-DB-001, BR-WEB-007, BR-LIB-010 | ✅ Full |
| AUTH-02 | Password ≥ 8, letter and number, client and server | BR-LIB-008, BR-FO-002 | ✅ Full |
| AUTH-03 | Passwords hashed, never logged or returned | Noted in ENT-Client only; **added as BR-WEB-042 after comparison** | ⚠️ Partial (missed as a rule) |
| AUTH-04 | Session 7 days, token not script-readable | BR-WEB-002 (+ http-only cookie note) | ✅ Full |
| AUTH-05 | $0 wallet and welcome message on sign-up | BR-WEB-008, BR-WEB-009, BR-DB-007 | ✅ Full |
| PAY-01 | Amount > 0 and ≤ 1,000,000 | BR-LIB-013 | ✅ Full |
| PAY-02 | Bank account and branch code format | BR-LIB-014, BR-LIB-015 | ✅ Full (more precise: 6–18 digits, IFSC pattern) |
| PAY-03 | Card checksum, future expiry, valid CVV | BR-LIB-016, 017, 018 | ✅ Full (more precise: the current month counts as valid) |
| PAY-04 | Card and account numbers never stored, only masked | BR-WEB-021, BR-LIB-020 | ✅ Full |
| PAY-05 | Pending → Success after a delay | BR-WEB-020 | ✅ Full (more precise: 1.5 s / 0.8 s) |
| TRD-01 | Buy rejected unless balance ≥ total, checked at execution | BR-WEB-027 (+ screen pre-check BR-FO-005) | ✅ Full |
| TRD-02 | Sell rejected unless held ≥ quantity | BR-WEB-029 | ✅ Full |
| TRD-03 | Execution price is the server's price, not the quote | BR-WEB-025 | ✅ Full |
| TRD-04 | Weighted average cost on buy | BR-WEB-028 | ✅ Full |
| TRD-05 | Positive whole quantity | BR-LIB-019 | ✅ Full |
| TRD-06 | Trade fully succeeds or fully fails | BR-WEB-034 | ✅ Full (the extraction also found what is *outside* that unit: D-WEB-002) |
| INV-01 | Invoice for every completed trade | BR-WEB-033 | ✅ Full |
| INV-02 | Invoice numbers unique and immutable, derived from trade ID | BR-LIB-004, BR-DB-005 | ✅ Full, plus a challenge (D-LIB-001) |
| INBX-01 | New messages unread; opening marks read; toggle back | BR-DB-009, BR-FO-014, BR-WEB-041 | ✅ Full |
| INBX-02 | Unread badge refreshes within 30 s | BR-FO-015 | ✅ Full |

**Score: 19 of 20 fully found, 1 partially found. No rule was contradicted.** The features listed in the spec's module sections were also all found:
- dashboard tiles, empty states, quick links
- the ~40-company catalogue
- the review-then-confirm step
- instant fill
- invoice links from history and inbox
- the demo disclaimer
- email fixed, KYC cosmetic

## 2. Open questions the spec answers

| Question | Spec answer | Effect |
|---|---|---|
| Q-DOM-001 KYC | "Cosmetic status field only; no verification occurs." KYC/AML is out of scope; a KYC provider is on the roadmap (Phase 3). | Answered: intended |
| Q-WEB-005 KYC gating | Out of scope | Answered |
| Q-FO-002 Forgot or change password | Forgot-password is on the roadmap (Phase 2). MFA and reset emails are out of scope. | Answered: known gap |
| Q-PRC-001 Settlement and market hours | "Instant fill — no order book, no partial fills" | Answered: intended |
| Q-API-001 Public API consumers | Not in the Product Spec. The API was added after v1.0 (commit `ae607a6`) and has its own API Spec. | Still open |
| Q-WEB-001 Price tolerance | "The reviewed price is an estimate, not a lock." No tolerance is defined. | Partly answered. Product still needs to decide on a tolerance. |
| Q-LIB-002 Brokerage fee | Not mentioned | Still open |

## 3. What the code shows that the spec doesn't say

These are the kit's added value. The spec describes what the system was *meant* to do; the code shows what it *actually* does.

| Finding | Why it matters |
|---|---|
| A whole second channel, the **Public REST API**, with duplicated rules (D-API-001) and feature gaps | The spec covers only the portal. API callers have none of the screen protections. |
| Notifications are written **after** the atomic trade commits (D-WEB-002) | The spec says "no partially-applied trade". That holds for money, but a failure here produces an error after a successful trade, and a retry produces a duplicate trade. |
| No server-side duplicate-submission protection (D-WEB-004, D-API-005) | Only the browser button prevents double trades. This is the same class of problem as the "client lock" in your real system. |
| Stuck Pending funding is never reconciled (D-WEB-003) | Contradicts "funding request moves from pending to confirmed" in failure cases |
| Invoice number uniqueness relies on 8 hex characters (D-LIB-001) | The spec says "unique". The code assumes it; the DB enforces it by failing the trade. |
| Quote vs execution can differ by about 4%; the balance pre-check uses the quote (D-WEB-006) | Explains "insufficient balance" errors right after a passed review |
| Illustrative 0.1% fee on the invoice (BR-LIB-006) | Not in the spec at all |
| Invoices re-rendered with the *current* address (Q-LIB-003) | A record-keeping question the spec doesn't address |
| UI and server validation differences (D-FO-001, D-FO-002) | The spec says "client- and server-side validation on every field". True, but not identical. |
| Logout doesn't revoke the token (D-WEB-001); no login throttling (D-WEB-007) | Security gaps not covered by the spec's NFRs |
| Money stored as floating point (D-DB-001) | Data-integrity risk under "financial integrity" |
| `GET /api/invoices` has no caller (D-WEB-005) | Dead code, or a missing screen |

## 4. What the extraction could not produce (expected limits)

- **Why the product exists:** purpose, personas, value proposition, success metrics. The code can't say.
- **Non-functional targets:** performance, accessibility, browser support. These aren't in code.
- **One spec claim was not checked:** "every irreversible action requires explicit confirmation". Code shows that **funding has no confirm step**. Neither the extraction nor the spec flagged this. The kit's UI procedure should check money-moving actions for a confirmation step.

## 5. Lessons fed back into the kit

1. Make "data protection" (hashed, masked, never stored, never returned) an explicit rule category. This would have caught AUTH-03.
2. Look for side effects **after** the main transaction commits, and for retry or duplicate exposure.
3. Give shared libraries their own folder and prefix when several components call them.
4. When logic is copy-pasted across channels, document the rule once and map the duplicates.
5. Always cite full repo-relative paths. Short names were ambiguous here (two `tradesRoutes.ts`).
6. Run the mechanical citation check during verification and coverage.
7. In the UI procedure, check that money-moving actions have an explicit confirmation step.
8. Warn when `.claude/` is git-ignored, because the kit's commands won't be shared.
