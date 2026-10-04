> 🔄 **Generated** by the reverse-engineering kit from project `stockbroker` (code commit `ae607a6`, 2026-10-04, business view). **Do not edit this page**: changes are overwritten on the next publish. Give feedback through the review packs.

**Component:** `packages/server` · **Prefix:** `WEB` · **Capability:** [capability.md](/Business-Requirements/StockBroker-Business-Requirements/Components/Web-server) · **Endpoints:** [api-catalogue.md](/Business-Requirements/StockBroker-Business-Requirements/Components/Web-server/API-Catalogue)

> Most of these rules are **also implemented, by copy, in the Public API**. See the duplicate map in [public-api/rules.md](/Business-Requirements/StockBroker-Business-Requirements/Components/Public-REST-API/Rules).

## Summary

| ID | Title | Confidence | Status |
|---|---|---|---|
| BR-WEB-001 | Sign-in required for all client operations | High | Draft |
| BR-WEB-002 | Session lasts 7 days | High | Draft |
| BR-WEB-003 | Missing or expired session is rejected | High | Draft |
| BR-WEB-004 | Clients see and change only their own data | High | Draft |
| BR-WEB-005 | Another client's invoice or message is reported as not found | High | Draft |
| BR-WEB-006 | Invalid input is rejected with a message per field | High | Draft |
| BR-WEB-007 | Email must not already be registered | High | Draft |
| BR-WEB-008 | Wallet opened automatically at registration | High | Draft |
| BR-WEB-009 | Welcome message at registration | High | Draft |
| BR-WEB-010 | Client is signed in immediately after registering | High | Draft |
| BR-WEB-011 | Login failure gives one generic message | High | Draft |
| BR-WEB-012 | Logout ends the session on that browser | High | Draft |
| BR-WEB-013 | Clients may change only name, phone and address | High | Draft |
| BR-WEB-014 | Address can be cleared | Medium | Draft |
| BR-WEB-015 | Company search by ticker, name or sector, sorted by ticker | High | Draft |
| BR-WEB-016 | Company list shows a current simulated price | High | Draft |
| BR-WEB-017 | Dashboard contents | High | Draft |
| BR-WEB-018 | Dashboard total gain/loss % | High | Draft |
| BR-WEB-019 | Transaction history newest first | High | Draft |
| BR-WEB-020 | Funding: Pending, then credited and Success | High | Draft |
| BR-WEB-021 | Only the last 4 digits of bank or card details are kept | High | Draft |
| BR-WEB-022 | Funding confirmation message | High | Draft |
| BR-WEB-023 | Trade history newest first, with invoice | High | Draft |
| BR-WEB-024 | Trade must be for an existing company | High | In review |
| BR-WEB-025 | Execution price set by the server at execution time | High | In review |
| BR-WEB-026 | Trade total = price × quantity, rounded to the cent | High | In review |
| BR-WEB-027 | Buy rejected if wallet balance is insufficient | High | In review |
| BR-WEB-028 | Buy debits wallet and adds to holding at weighted average cost | High | In review |
| BR-WEB-029 | Sell rejected if client doesn't hold enough shares | High | In review |
| BR-WEB-030 | Sell reduces holding; removed at zero; average cost unchanged | High | In review |
| BR-WEB-031 | Sell credits the wallet with the trade total | High | In review |
| BR-WEB-032 | Every trade records a wallet transaction | High | In review |
| BR-WEB-033 | Every trade is recorded as Completed with an invoice | High | In review |
| BR-WEB-034 | Trade updates are all-or-nothing | High | In review |
| BR-WEB-035 | Two notifications after every trade | High | In review |
| BR-WEB-036 | No fees or commission charged on trades | Medium | In review |
| BR-WEB-037 | Invoice list, newest first | Medium | Draft |
| BR-WEB-038 | Invoice PDF downloadable only by the trade owner | High | Draft |
| BR-WEB-039 | Inbox newest first | High | Draft |
| BR-WEB-040 | Unread count | High | Draft |
| BR-WEB-041 | Client can mark a message read or unread | High | Draft |
| BR-WEB-042 | Passwords are stored only as a one-way hash and never returned | High | Draft |

---



[[_TOSP_]]
