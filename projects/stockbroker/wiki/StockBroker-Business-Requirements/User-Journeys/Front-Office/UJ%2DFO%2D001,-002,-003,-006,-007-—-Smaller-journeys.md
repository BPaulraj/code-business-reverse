> 🔄 **Generated** by the reverse-engineering kit from project `stockbroker` (code commit `ae607a6`, 2026-10-04, business view). **Do not edit this page**: changes are overwritten on the next publish. Give feedback through the review packs.

[[_TOC_]]

**Status:** Draft · **Application:** Front-office · **Last extracted:** 2026-10-04

These journeys are short, so they are combined in one file. Each section follows the user-journey template.

---

## UJ-FO-001 — Register

- **Actor / goal:** A visitor creates an account.
- **Entry:** `/register` (`packages/web/src/App.tsx:20`), linked from login.

| # | User action | System response | Rules | Backend call | Source |
|---|---|---|---|---|---|
| 1 | Enters name, email, phone and password, clicks "Create account" | The screen checks the fields | BR-FO-002 | — | `packages/web/src/pages/Register.tsx:28-33` |
| 2 | — | The account and wallet are created, a welcome message is sent, the client is signed in and sent to the dashboard | BR-WEB-007…010, BR-FO-003 | `POST /api/auth/register` | `Register.tsx:34-37` |
| 2a | — | Email already registered: the message appears under the email field | BR-WEB-007 | | `Register.tsx:39-41` |

Address can't be given at registration (BR-LIB-012).

---

## UJ-FO-002 — Log in / log out

- **Entry:** `/login` (`packages/web/src/App.tsx:19`). "Log out" is in the header of every page (`packages/web/src/components/Layout.tsx:35-37`).

| # | User action | System response | Rules | Backend call | Source |
|---|---|---|---|---|---|
| 1 | Enters email and password, clicks "Log in" | Success → dashboard. Failure → "Invalid email or password". | BR-WEB-011, BR-FO-003 | `POST /api/auth/login` | `packages/web/src/pages/Login.tsx:14-26` |
| 2 | Clicks "Log out" | Session removed, back to login | BR-WEB-012 | `POST /api/auth/logout` | `Layout.tsx:20-23` |

There is no "forgot password", password change or "remember me" option.

---

## UJ-FO-003 — View dashboard

- **Entry:** `/dashboard`, the default page (`packages/web/src/App.tsx:16,24`).

| Element | Content | Rules | Source |
|---|---|---|---|
| Greeting | "Welcome, {name}" | — | `packages/web/src/pages/Dashboard.tsx:24` |
| Tiles | Wallet balance; Portfolio value; Total gain/loss (amount and %), green if ≥ 0, red if negative | BR-WEB-017, 018 | `Dashboard.tsx:34-59` |
| Holdings table | Ticker, quantity, average cost, price, value, gain/loss (%). Empty: "You don't own any shares yet. Place your first trade." | BR-LIB-003 | `Dashboard.tsx:61-102` |
| Recent trades | Last 5: type, ticker, quantity, total, date, invoice link | BR-WEB-017, BR-FO-016 | `Dashboard.tsx:104-133` |
| Quick links | Trade, Payments, Profile, Inbox | — | `Dashboard.tsx:9-14` |

Backend: `GET /api/dashboard/summary`.

---

## UJ-FO-006 — Manage profile

- **Entry:** `/profile`.

| # | User action | System response | Rules | Backend call | Source |
|---|---|---|---|---|---|
| 1 | Opens Profile | Shows email, member since and KYC status (mock) | BR-FO-013 | — | `packages/web/src/pages/Profile.tsx:63-88` |
| 2 | Edits name, phone or address and clicks "Save changes" | "Profile updated successfully." | BR-FO-013, BR-WEB-013, 014 | `PUT /api/auth/profile` | `Profile.tsx:33-51` |

---

## UJ-FO-007 — Read inbox and download invoices

- **Entry:** `/inbox`, with an unread badge in the menu (BR-FO-015).

| # | User action | System response | Rules | Backend call | Source |
|---|---|---|---|---|---|
| 1 | Opens Inbox | The list is newest first. The newest message opens and is marked read. | BR-WEB-039, BR-FO-014 | `GET /api/inbox`, `PATCH /api/inbox/:id` | `packages/web/src/pages/Inbox.tsx:15-32` |
| 2 | Selects a message | Shows its type, subject, date and body. Invoice messages also show an "Invoice" link. | BR-FO-014, 016 | | `Inbox.tsx:76-101` |
| 3 | Clicks "Mark as read/unread" | Read status toggles, and the badge updates | BR-WEB-041 | `PATCH /api/inbox/:id` | `Inbox.tsx:88-93` |
| 4 | Clicks "Invoice" | The invoice PDF opens in a new tab | BR-WEB-038, BR-LIB-005…007 | `GET /api/invoices/:id/pdf` | `packages/web/src/components/InvoiceLink.tsx:1-13` |

## Product comments
