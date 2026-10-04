# Shared database — Business Rules

**Component:** `packages/db/prisma` · **Prefix:** `DB` · **Capability:** [capability.md](capability.md)

## Summary

| ID | Title | Confidence | Status |
|---|---|---|---|
| BR-DB-001 | One account per email address | High | Draft |
| BR-DB-002 | One wallet per client | High | Draft |
| BR-DB-003 | One holding per client per company | High | Draft |
| BR-DB-004 | One invoice per trade | High | Draft |
| BR-DB-005 | Invoice numbers are unique | High | Draft |
| BR-DB-006 | New clients start as KYC Unverified | High | Draft |
| BR-DB-007 | New wallets start with zero balance | High | Draft |
| BR-DB-008 | Tickers are unique | High | Draft |
| BR-DB-009 | New messages are unread | High | Draft |
| BR-DB-010 | Records with history can't be deleted | Medium | Draft |

---

### BR-DB-001 — One account per email address

- **Statement:** No two client accounts can have the same email address.
- **Trigger:** Registration.
- **Conditions / exceptions:** Emails are lower-cased before saving (BR-LIB-010), so the check is effectively case-insensitive.
- **Outcome on violation:** The registration is rejected (the application checks first; see BR-WEB-007).
- **Source:** `packages/db/prisma/schema.prisma:13`, `packages/db/prisma/migrations/20260815131827_init/migration.sql:92`
- **Confidence:** High
- **Status:** Draft
- **Product comments:**

### BR-DB-002 — One wallet per client

- **Statement:** Each client has at most one wallet.
- **Source:** `schema.prisma:28`, `migration.sql:95`
- **Confidence:** High
- **Technical note:** The wallet is created together with the client (BR-WEB-008).
- **Status:** Draft
- **Product comments:**

### BR-DB-003 — One holding per client per company

- **Statement:** A client's shares in a given company are always held as a single position. Repeated purchases add to it.
- **Source:** `schema.prisma:69`, `migration.sql:101`
- **Confidence:** High
- **Status:** Draft
- **Product comments:**

### BR-DB-004 — One invoice per trade

- **Statement:** A trade can have at most one invoice.
- **Source:** `schema.prisma:90`, `migration.sql:104`
- **Confidence:** High
- **Status:** Draft
- **Product comments:**

### BR-DB-005 — Invoice numbers are unique

- **Statement:** No two invoices share an invoice number.
- **Source:** `schema.prisma:91`, `migration.sql:107`
- **Confidence:** High
- **Related:** D-LIB-001 (if two numbers ever collided, the trade itself would fail)
- **Status:** Draft
- **Product comments:**

### BR-DB-006 — New clients start as KYC Unverified

- **Statement:** Every new client account starts with KYC status Unverified.
- **Source:** `schema.prisma:17`, `migration.sql:9`
- **Confidence:** High
- **Related:** Q-DOM-001 (nothing ever changes it)
- **Status:** Draft
- **Product comments:**

### BR-DB-007 — New wallets start with zero balance

- **Statement:** A new wallet holds no cash until the client adds funds. There is no sign-up bonus.
- **Source:** `schema.prisma:29`, `packages/server/src/modules/auth/authRoutes.ts:46`
- **Confidence:** High
- **Status:** Draft
- **Product comments:**

### BR-DB-008 — Tickers are unique

- **Statement:** Each company has a unique ticker symbol.
- **Source:** `schema.prisma:50`, `migration.sql:98`
- **Confidence:** High
- **Status:** Draft
- **Product comments:**

### BR-DB-009 — New messages are unread

- **Statement:** Every new inbox message starts as unread.
- **Source:** `schema.prisma:104`, `migration.sql:86`
- **Confidence:** High
- **Status:** Draft
- **Product comments:**

### BR-DB-010 — Records with history can't be deleted

- **Statement:** A client, wallet, company or trade cannot be deleted while related records (transactions, holdings, trades, invoices, messages) exist.
- **Source:** `migration.sql:18,31,50-51,65-66,75,88` (`ON DELETE RESTRICT`)
- **Confidence:** Medium. No application code deletes these records anyway, so the constraint is never exercised.
- **Technical note:** The only delete in the application is removing an empty holding (BR-WEB-030).
- **Related:** Q-DOM-005
- **Status:** Draft
- **Product comments:**
