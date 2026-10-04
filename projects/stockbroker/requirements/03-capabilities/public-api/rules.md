# Public REST API — Business Rules

**Component:** `packages/api` · **Prefix:** `API` · **Capability:** [capability.md](capability.md)

## Duplicated rules (same behaviour as the web server)

These rules are implemented a second time in this component, by copying the code. They are reviewed once, under their WEB ID. The sources below are the *second* place where each one must be changed.

| Rule | Also implemented here | Difference |
|---|---|---|
| BR-WEB-001 Sign-in required | `packages/api/src/middleware/requireAuth.ts:10-24` + `router.use(requireAuth)` in each module | Bearer token instead of cookie |
| BR-WEB-002 7-day session | `packages/api/src/lib/token.ts:4-8` | — |
| BR-WEB-003 Expired session rejected | `requireAuth.ts:14-23` | Message: "Invalid or expired token" |
| BR-WEB-004 Own data only | all `where: { userId }` filters | — |
| BR-WEB-005 Others' items not found | `invoicesRoutes.ts:19-21,38-40`, `inboxRoutes.ts:26-28` | — |
| BR-WEB-006 Validation messages | `packages/api/src/middleware/errorHandler.ts:6-13` | — |
| BR-WEB-007…010 Registration | `packages/api/src/modules/users/usersRoutes.ts:15-44` | Returns a token instead of setting a cookie |
| BR-WEB-011 Generic login failure | `packages/api/src/modules/sessions/sessionsRoutes.ts:16-24` | — |
| BR-WEB-013, 014 Profile changes | `usersRoutes.ts:58-65` | — |
| BR-WEB-015, 016 Company search and price | `packages/api/src/modules/companies/companiesRoutes.ts:14-30` | — |
| BR-WEB-020…022 Funding | `packages/api/src/modules/payments/paymentsRoutes.ts:16-64` | Response differs (BR-API-007) |
| BR-WEB-023…035 Trading | `packages/api/src/modules/trades/tradesRoutes.ts:12-150` | Invoice message text differs (BR-API-006) |
| BR-WEB-038 Invoice PDF owner only | `packages/api/src/modules/invoices/invoicesRoutes.ts:30-49` | — |
| BR-WEB-039 Inbox newest first | `packages/api/src/modules/inbox/inboxRoutes.ts:11-20` | — |

**Not implemented here:**
- BR-WEB-012 (logout)
- BR-WEB-017, 018 (dashboard)
- BR-WEB-019 (transaction history)
- BR-WEB-037 (invoice list)
- BR-WEB-040, 041 (unread count, mark read)

## API-specific rules

| ID | Title | Confidence | Status |
|---|---|---|---|
| BR-API-001 | API clients authenticate with a bearer access token | High | Draft |
| BR-API-002 | Any client application may call the API | Medium | Draft |
| BR-API-003 | Portfolio summary shows total account value | High | Draft |
| BR-API-004 | Invoice lookup by trade reference | High | Draft |
| BR-API-005 | Reading a message through the API doesn't mark it read | High | Draft |
| BR-API-006 | API invoice message points to the API lookup | High | Draft |
| BR-API-007 | Funding through the API returns only the new balance | High | Draft |

---

### BR-API-001 — API clients authenticate with a bearer access token

- **Statement:** Registering or logging in through the API returns an access token valid for 7 days. Every other call must present it as "Bearer &lt;token&gt;".
- **Outcome on violation:** "Missing or malformed Authorization header — expected 'Bearer &lt;token&gt;'" or "Invalid or expired token".
- **Source:** `packages/api/src/middleware/requireAuth.ts:10-24`, `packages/api/src/lib/token.ts:4-8`, `usersRoutes.ts:43-44`, `sessionsRoutes.ts:26-27`
- **Confidence:** High
- **Technical note:** Tokens are signed with `JWT_SECRET`. If the web server and the API share the secret, a token from one works on the other. Not verifiable from the repo.
- **Status:** Draft
- **Product comments:**

### BR-API-002 — Any client application may call the API

- **Statement:** The API accepts calls from any website or application origin.
- **Rationale (inferred):** The code comment calls it "a general-purpose public API surface (Swagger/Postman/curl clients)".
- **Source:** `packages/api/src/index.ts:19-22`
- **Confidence:** Medium. The business intent (which partners, which apps) is unknown.
- **Related:** Q-API-001
- **Status:** Draft
- **Product comments:**

### BR-API-003 — Portfolio summary shows total account value

- **Statement:** The portfolio summary returns:
  - cash balance
  - stock value (sum of the current value of holdings)
  - total account value = cash + stock value
  - the holdings with their valuations
- **Source:** `packages/api/src/modules/portfolio/portfolioRoutes.ts:10-29`
- **Confidence:** High
- **Technical note:** The web portal never shows "total account value". Its dashboard shows wallet and portfolio values separately (BR-WEB-017).
- **Status:** Draft
- **Product comments:**

### BR-API-004 — Invoice lookup by trade reference

- **Statement:** A client can fetch the invoice of one of their trades by the trade reference. The response includes a link to download the PDF. If the trade isn't theirs or has no invoice, the answer is "No invoice found for this trade reference".
- **Source:** `packages/api/src/modules/invoices/invoicesRoutes.ts:11-28`
- **Confidence:** High
- **Status:** Draft
- **Product comments:**

### BR-API-005 — Reading a message through the API doesn't mark it read

- **Statement:** Opening a single inbox message through the API leaves it unread. The API has no way to mark messages read.
- **Source:** `packages/api/src/modules/inbox/inboxRoutes.ts:22-31`
- **Confidence:** High
- **Related:** D-API-003
- **Status:** Draft
- **Product comments:**

### BR-API-006 — API invoice message points to the API lookup

- **Statement:** For trades placed through the API, the invoice inbox message tells the client to fetch the invoice via the API trade lookup, instead of "Trade history".
- **Source:** `packages/api/src/modules/trades/tradesRoutes.ts:139-147` vs `packages/server/src/modules/trades/tradesRoutes.ts:138-146`
- **Confidence:** High
- **Technical note:** A client who trades via the API and then reads the portal inbox sees a technical instruction ("GET /invoices/by-trade/…").
- **Status:** Draft
- **Product comments:**

### BR-API-007 — Funding through the API returns only the new balance

- **Statement:** After adding funds through the API, the response contains only the new wallet balance, not the transaction.
- **Source:** `packages/api/src/modules/payments/paymentsRoutes.ts:66`
- **Confidence:** High
- **Status:** Draft
- **Product comments:**
