# Open questions — Public API

| ID | Question for product | What the code does today | Related | Raised | Answer | Status |
|---|---|---|---|---|---|---|
| Q-API-001 | Who are the intended users of the public API (partners, a mobile app, internal tools)? Should it match the portal's features (transaction history, mark read, logout)? | Open to any caller. Missing transaction history, read status and logout. | BR-API-002, api-catalogue feature gaps | 2026-10-04 | | Open |
| Q-API-002 | Should a token issued by the portal work on the API and vice versa? | Both sign tokens with a `JWT_SECRET`. Whether the values match depends on deployment. | BR-API-001 | 2026-10-04 | | Open |
