# UJ-FO-005 — Add funds to wallet

**Status:** Draft · **Application:** Front-office · **Last extracted:** 2026-10-04

## Actor and goal

- **Role(s):** Any signed-in client
- **Goal:** Put cash into the wallet so they can buy shares
- **Entry:** Menu "Payments" → `/payments` (`packages/web/src/components/Layout.tsx:10`)

## Steps

| # | Screen | User action | System response | Validations / rules | Backend call | Source |
|---|---|---|---|---|---|---|
| 1 | Payments | Opens Payments | Shows the balance, the funding form (Bank transfer tab selected) and the transaction history | BR-FO-012 | `GET /api/wallet`, `GET /api/wallet/transactions` | `packages/web/src/pages/Payments.tsx:45-54` |
| 2 | Payments | Chooses Bank transfer or Debit card | The form switches and errors are cleared | — | — | `Payments.tsx:118-137` |
| 3 | Payments | Enters details and clicks "Add funds" | Validates. The button shows "Processing bank transfer…" / "Authorizing card…" | BR-FO-010, 011 | `POST /api/wallet/add-funds` ([catalogue #11](../../03-capabilities/web-server/api-catalogue.md)) | `Payments.tsx:56-96` |
| 4 | Payments | — | "{amount} added successfully. New balance: {balance}." The form is cleared, the history refreshes, and the inbox gets a message. | BR-WEB-020…022 | — | `Payments.tsx:85-92` |

## Validations shown to the user

| Field / action | Rule | Message shown | Also enforced server-side? | Source |
|---|---|---|---|---|
| Amount | > 0 | "Enter a valid amount" | Yes, and max 1,000,000 (D-FO-002) | `Payments.tsx:25,36` |
| Account number | 6–18 digits | "Enter a valid account number (6-18 digits)" | Yes | `Payments.tsx:26-28` |
| Branch code | IFSC format | "Enter a valid IFSC-style branch code" | Yes | `Payments.tsx:29` |
| Card number | Luhn checksum | "Enter a valid card number" | Yes | `Payments.tsx:37` |
| Expiry | MM/YY, not past | "Enter a valid, non-expired MM/YY date" | Yes | `Payments.tsx:38-40` |
| CVV | 3–4 digits | "Enter a valid CVV" | Yes | `Payments.tsx:41` |

## Related

P-002, D-WEB-003, D-WEB-004

## Product comments
