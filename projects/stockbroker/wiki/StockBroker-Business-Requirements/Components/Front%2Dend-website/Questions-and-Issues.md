> 🔄 **Generated** by the reverse-engineering kit from project `stockbroker` (code commit `ae607a6`, 2026-10-04, business view). **Do not edit this page**: changes are overwritten on the next publish. Give feedback through the review packs.

| ID | Question for product | What the code does today | Related | Raised | Answer | Status |
|---|---|---|---|---|---|---|
| Q-FO-001 | Should Sell be hidden or disabled for companies the client doesn't hold? | Sell is always offered; an error appears at review | BR-FO-004 | 2026-10-04 | | Open |

| ID | Observation | Evidence | Possible impact | Related | Raised | Decision | Status |
|---|---|---|---|---|---|---|---|
| D-FO-001 | The phone check on screen (≥ 7 characters) is weaker than the server's (7–20 characters, limited symbols) | `packages/web/src/pages/Register.tsx:13`, `packages/web/src/pages/Profile.tsx:11` vs `packages/shared/src/index.ts:201-206` | Client sees the error only after submitting | BR-FO-002, BR-LIB-011 | 2026-10-04 | | Open |
| D-FO-002 | The 1,000,000 funding maximum isn't checked on screen | `packages/web/src/pages/Payments.tsx:25,36` vs `packages/shared/src/index.ts:230` | Error appears only after submitting | BR-FO-010, BR-LIB-013 | 2026-10-04 | | Open |
| D-FO-003 | The order panel keeps the quote from when Buy or Sell was clicked, while the list refreshes every 15 s | `packages/web/src/pages/Trade.tsx:21,37-38,35` | The estimate and balance check can be based on an old price | BR-FO-008, D-WEB-006 | 2026-10-04 | | Open |
