# P-003 — Register a new client

**Status:** Draft · **Last traced:** 2026-10-04 · **Components involved:** Front-end, Web server (or Public API), Core library, Shared database

## Goal

A visitor becomes a client with an account, an empty wallet and a welcome message, and is signed in.

## Entry points

- Portal: `/register` → `POST /api/auth/register` (`packages/server/src/modules/auth/authRoutes.ts:26`)
- API: `POST /api/v1/users` (`packages/api/src/modules/users/usersRoutes.ts:12`)

## Main flow

| Step | Actor / component | What happens | Rules | Source |
|---|---|---|---|---|
| 1 | Front-end | The visitor enters name, email, phone and password. The screen validates them. | BR-FO-002 | `packages/web/src/pages/Register.tsx:28-33` |
| 2 | Web server | Validates again. The email is lower-cased. | BR-LIB-008…011 | `authRoutes.ts:29` |
| 3 | Web server | Checks that the email isn't already registered | BR-WEB-007, BR-DB-001 | `authRoutes.ts:31-36` |
| 4 | Web server | Creates the client (KYC Unverified) and their wallet (balance 0) together. The password is stored hashed. | BR-WEB-008, BR-DB-006, 007 | `authRoutes.ts:38-48` |
| 5 | Web server | Sends the welcome message | BR-WEB-009 | `authRoutes.ts:50-55` |
| 6 | Web server | Signs the client in: a 7-day session (portal) or access token (API) | BR-WEB-010, BR-WEB-002, BR-API-001 | `authRoutes.ts:57-58` |
| 7 | Front-end | Goes to the dashboard | BR-FO-003 | `Register.tsx:37` |

## Alternative and failure paths

| At step | Condition | What happens | State left behind | Rules |
|---|---|---|---|---|
| 1–2 | Invalid field | Field messages | None | BR-FO-002, BR-LIB-008…011 |
| 3 | Email exists | "An account with this email already exists" | None | BR-WEB-007 |
| 3–4 | Two registrations with the same email at the same instant | The second is stopped by the DB uniqueness rule, showing "Internal server error" | None | BR-DB-001 |
| 5 | Welcome message fails | Client sees an error, **but the account exists**. Re-registering says "email already exists". | Account without a welcome message | D-WEB-002 (same pattern) |

## Gaps

No email verification, no KYC step, no terms acceptance (Q-DOM-001, Q-FO-002).

## Product comments
