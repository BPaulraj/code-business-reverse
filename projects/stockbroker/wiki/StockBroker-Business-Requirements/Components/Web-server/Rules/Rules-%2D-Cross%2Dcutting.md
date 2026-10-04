> 🔄 **Generated** by the reverse-engineering kit from project `stockbroker` (code commit `ae607a6`, 2026-10-04, business view). **Do not edit this page**: changes are overwritten on the next publish. Give feedback through the review packs.

[[_TOC_]]

### BR-WEB-001 — Sign-in required for all client operations

- **Statement:** Every operation except registering, logging in and logging out requires the client to be signed in.
- **Outcome on violation:** "Not authenticated".
- **Confidence:** High
- **Status:** Draft
- **Product comments:**

### BR-WEB-002 — Session lasts 7 days

- **Statement:** After logging in or registering, a client stays signed in for 7 days. There is no inactivity timeout.
- **Confidence:** High
- **Related:** Q-WEB-004, D-WEB-001
- **Status:** Draft
- **Product comments:**

### BR-WEB-003 — Missing or expired session is rejected

- **Statement:** A request with an invalid or expired session is refused with "Invalid or expired session".
- **Confidence:** High
- **Status:** Draft
- **Product comments:**

### BR-WEB-004 — Clients see and change only their own data

- **Statement:** A client can only see and act on their own wallet, transactions, holdings, trades, invoices and messages.
- **Confidence:** High
- **Status:** Draft
- **Product comments:**

### BR-WEB-005 — Another client's invoice or message is reported as not found

- **Statement:** If a client asks for an invoice or message that belongs to someone else, the system answers "not found". It does not reveal that the item exists.
- **Confidence:** High
- **Status:** Draft
- **Product comments:**

### BR-WEB-006 — Invalid input is rejected with a message per field

- **Statement:** When submitted data breaks a validation rule, the request is refused with "Validation failed" and one message per invalid field (the first problem only).
- **Confidence:** High
- **Status:** Draft
- **Product comments:**
