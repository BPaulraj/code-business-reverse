# Front-end website — Capability

**Component:** `packages/web` · **Prefix:** `FO` · **Tech:** React 18, Vite, React Query, Tailwind · **Last extracted:** 2026-10-04 · **Status:** Extracted

## Purpose

The self-service client portal. Clients use it to register, sign in, fund their wallet, browse companies and trade, track their portfolio, read notifications and download invoices.

## Responsibilities

- Navigation and access control on screens (BR-FO-001)
- Registration and login (UJ-FO-001, 002)
- Dashboard (UJ-FO-003)
- Trading with a two-step order (UJ-FO-004)
- Wallet funding (UJ-FO-005)
- Profile (UJ-FO-006)
- Inbox and invoices (UJ-FO-007)

## Not owned here

All rules are enforced again on the server (web server). The screen checks are convenience copies.

## Entry points (screens)

| # | Type | Route | Business meaning | Backend calls | Rules | Source |
|---|---|---|---|---|---|---|
| 1 | Screen | `/login` | Sign in | `POST /api/auth/login` | BR-FO-003 | `packages/web/src/pages/Login.tsx` |
| 2 | Screen | `/register` | Create account | `POST /api/auth/register` | BR-FO-002, 003 | `packages/web/src/pages/Register.tsx` |
| 3 | Screen | `/dashboard` | Account snapshot | `GET /api/dashboard/summary` | BR-FO-016 | `packages/web/src/pages/Dashboard.tsx` |
| 4 | Screen | `/trade` | Browse and trade | companies, holdings, wallet, trades | BR-FO-004…009 | `packages/web/src/pages/Trade.tsx` |
| 5 | Screen | `/payments` | Add funds, history | wallet, transactions, add-funds | BR-FO-010…012 | `packages/web/src/pages/Payments.tsx` |
| 6 | Screen | `/profile` | View and edit profile | `PUT /api/auth/profile` | BR-FO-013 | `packages/web/src/pages/Profile.tsx` |
| 7 | Screen | `/inbox` | Messages and invoices | inbox list, mark read | BR-FO-014…016 | `packages/web/src/pages/Inbox.tsx` |

Routes: `packages/web/src/App.tsx:16-31`. Navigation: `packages/web/src/components/Layout.tsx:7-13`.

## Business rules

See [rules.md](rules.md): 17 rules, all High.
