# Open questions — Web server

| ID | Question for product | What the code does today | Related | Raised | Answer | Status |
|---|---|---|---|---|---|---|
| Q-WEB-001 | Should a trade be rejected, or re-confirmed, if the execution price moves too far from the quote? What tolerance? | The trade executes at a fresh price with no limit. The gap can reach about 4%. The screen only warns that the price "may differ slightly". | BR-WEB-025, BR-FO-006 | 2026-10-04 | | Open |
| Q-WEB-002 | Should rejected or failed trades be recorded (status Failed exists)? | Rejected trades leave no record. Status Failed is never used. | ENT-Trade, D-DOM-001 | 2026-10-04 | | Open |
| Q-WEB-003 | Should company search ignore upper/lower case? | It depends on the database. SQLite matching is case-insensitive for English letters, but a production database may not be. | BR-WEB-015 | 2026-10-04 | | Open |
| Q-WEB-004 | Is a fixed 7-day session acceptable, or is an inactivity timeout needed? | 7 days from login, regardless of activity | BR-WEB-002 | 2026-10-04 | | Open |
| Q-WEB-005 | Should funding or trading require KYC to be Verified? | No KYC check anywhere | Q-DOM-001 | 2026-10-04 | | Open |
| Q-WEB-006 | Should realised profit/loss on sales be calculated and reported? | Only unrealised gain/loss on current holdings is shown | BR-WEB-030, BR-LIB-003 | 2026-10-04 | | Open |
| Q-WEB-007 | Is an audit trail required for account changes and logins? | Nothing is logged except unexpected errors | api-catalogue cross-cutting | 2026-10-04 | | Open |
