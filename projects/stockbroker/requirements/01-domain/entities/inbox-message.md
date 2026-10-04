# ENT-InboxMessage — Inbox message

**Status:** Draft · **Owner component:** Web server / Public API · **Stored in:** `InboxMessage`

## Definition

An in-app notification to a client. **System** messages cover welcome, funding and trade confirmations. **Invoice** messages link to a trade invoice.

## Key attributes

| Attribute | Meaning | Values | Column | Source |
|---|---|---|---|---|
| Type | Kind of message | System / Invoice | `type` | `packages/shared/src/index.ts:18` |
| Subject, body | Text | free text | `subject`, `body` | `packages/db/prisma/schema.prisma:101-102` |
| Linked invoice | Invoice to download (Invoice messages only) | optional | `linkedInvoiceId` | `schema.prisma:103` |
| Read | Whether the client has read it | default unread | `isRead` | `schema.prisma:104` |

## Messages the system sends

| Trigger | Type | Subject | Source |
|---|---|---|---|
| Registration | System | "Welcome to StockBroker Demo" | `packages/server/src/modules/auth/authRoutes.ts:50-55` |
| Funding succeeded | System | "Funds added successfully" | `packages/server/src/modules/wallet/walletRoutes.ts:83-90` |
| Trade executed | System | "Trade executed" | `packages/server/src/modules/trades/tradesRoutes.ts:129-136` |
| Trade executed | Invoice | "Invoice INV-… for your purchase/sale of TICKER" | `tradesRoutes.ts:138-146` |

## Lifecycle

| From | To | Trigger | Source |
|---|---|---|---|
| — | Unread | Message created | `schema.prisma:104` |
| Unread | Read | Client opens it in the portal (automatic), or clicks "Mark as read" | `packages/web/src/pages/Inbox.tsx:27-32`, `packages/server/src/modules/inbox/inboxRoutes.ts:34-50` |
| Read | Unread | Client clicks "Mark as unread" | `Inbox.tsx:88-93` |

Messages cannot be deleted.

## Product comments
