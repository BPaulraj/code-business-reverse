# Suspected defects — Domain

| ID | Observation | Evidence | Possible impact | Related | Raised | Decision | Status |
|---|---|---|---|---|---|---|---|
| D-DOM-001 | Status values are defined but never used: Trade "Failed", Transaction "Failed", KYC "Pending"/"Verified" | `packages/shared/src/index.ts:15,17,19`. No writes found anywhere in the repo. | Reports and screens imply states that can't happen. Failed trades and payments leave no audit trail. | Q-DOM-001, Q-DOM-003, Q-WEB-002 | 2026-10-04 | | Open |
