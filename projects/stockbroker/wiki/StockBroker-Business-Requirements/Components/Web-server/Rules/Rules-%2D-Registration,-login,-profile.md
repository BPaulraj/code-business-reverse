> 🔄 **Generated** by the reverse-engineering kit from project `stockbroker` (code commit `ae607a6`, 2026-10-04, business view). **Do not edit this page**: changes are overwritten on the next publish. Give feedback through the review packs.

[[_TOC_]]

### BR-WEB-007 — Email must not already be registered

- **Statement:** Registration is refused if an account already exists with the same email (case-insensitive).
- **Outcome on violation:** "An account with this email already exists", shown against the email field.
- **Confidence:** High
- **Status:** Draft
- **Product comments:**

### BR-WEB-008 — Wallet opened automatically at registration

- **Statement:** Every new client gets a wallet with a zero balance at the moment of registration.
- **Confidence:** High
- **Status:** Draft
- **Product comments:**

### BR-WEB-009 — Welcome message at registration

- **Statement:** A new client receives a "Welcome to StockBroker Demo" inbox message. It explains that the wallet is ready, that they should add funds to trade, and that no real money is involved.
- **Confidence:** High
- **Status:** Draft
- **Product comments:**

### BR-WEB-010 — Client is signed in immediately after registering

- **Statement:** A successful registration signs the client in straight away. There is no email verification step.
- **Confidence:** High
- **Status:** Draft
- **Product comments:**

### BR-WEB-011 — Login failure gives one generic message

- **Statement:** If the email is unknown or the password is wrong, login fails with the same message: "Invalid email or password". There is no limit on attempts.
- **Confidence:** High
- **Related:** D-WEB-007
- **Status:** Draft
- **Product comments:**

### BR-WEB-012 — Logout ends the session on that browser

- **Statement:** Logging out removes the session from the client's browser.
- **Confidence:** High
- **Status:** Draft
- **Product comments:**

### BR-WEB-013 — Clients may change only name, phone and address

- **Statement:** A client can update their name, phone number and address. Email, KYC status and member-since date can't be changed by the client.
- **Confidence:** High
- **Status:** Draft
- **Product comments:**

### BR-WEB-014 — Address can be cleared

- **Statement:** A client can remove their address by saving it empty.
- **Confidence:** Medium. It is saved as an empty text, not "no address", which may matter for invoices (`packages/db/src/services/invoicePdfService.ts:29`).
- **Status:** Draft
- **Product comments:**
