> 🔄 **Generated** by the reverse-engineering kit from project `stockbroker` (code commit `ae607a6`, 2026-10-04, business view). **Do not edit this page**: changes are overwritten on the next publish. Give feedback through the review packs.

### BR-WEB-042 — Passwords are stored only as a one-way hash and never returned

- **Statement:** A client's password is stored only as a one-way hash, never as readable text. The password and its hash are never included in any response.
- **Confidence:** High
- **Status:** Draft
- **Product comments:**
