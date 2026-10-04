# Open questions — Domain

| ID | Question for product | What the code does today | Related | Raised | Answer | Status |
|---|---|---|---|---|---|---|
| Q-DOM-001 | How should a client's KYC status move from Unverified to Pending/Verified? Should anything (funding, trading) require KYC to be Verified? | KYC defaults to Unverified and no code ever changes it. Nothing checks it before funding or trading. The profile screen labels it "mock". | ENT-Client, BR-DB-006, BR-FO-013 | 2026-10-04 | | Open |
| Q-DOM-002 | Can clients withdraw cash from their wallet to a bank account? | There is no withdrawal function. Cash only leaves the wallet to pay for purchases. | ENT-Wallet | 2026-10-04 | | Open |
| Q-DOM-003 | When should a funding transaction be marked Failed, and what should the client see? | The Failed status exists but is never set. Funding always succeeds after the delay. | ENT-WalletTransaction, D-WEB-003 | 2026-10-04 | | Open |
| Q-DOM-004 | Who maintains the list of tradable companies, and can a company be suspended or delisted? | 41 companies are loaded by a seed script. There is no maintenance screen and no status. | ENT-Company | 2026-10-04 | | Open |
| Q-DOM-005 | Can a client close their account? | There is no account status or closure. The database prevents deleting a client who has records. | ENT-Client, BR-DB-010 | 2026-10-04 | | Open |
