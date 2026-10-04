> 🔄 **Generated** by the reverse-engineering kit from project `stockbroker` (code commit `ae607a6`, 2026-10-04, business view). **Do not edit this page**: changes are overwritten on the next publish. Give feedback through the review packs.

**There are no roles.** Every signed-in client has exactly the same permissions, limited to their own data (BR-WEB-004). No administrator, operations or support role exists anywhere in the code.

| Action | Visitor (signed out) | Signed-in client | Source |
|---|---|---|---|
| Register, log in | ✅ | — (redirected to dashboard) | `packages/web/src/auth/ProtectedRoute.tsx:18-30` |
| Dashboard, Trade, Payments, Profile, Inbox | ❌ (redirected to login) | ✅ own data only | `ProtectedRoute.tsx:4-16`, BR-WEB-001, 004 |
| View or download another client's invoice or message | ❌ | ❌ ("not found") | BR-WEB-005 |
| Change own email or KYC status | ❌ | ❌ | BR-WEB-013 |
| Maintain companies, prices, client accounts | ❌ | ❌ (no function exists) | Q-DOM-004 |
