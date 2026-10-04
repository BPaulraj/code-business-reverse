# ENT-Invoice — Trade invoice

**Status:** Draft · **Owner component:** Web server / Public API; PDF from the Core library · **Stored in:** `Invoice`

## Definition

The document issued for every executed trade. Only the reference is stored. The PDF is generated on demand from the trade, company and client data.

## Key attributes

| Attribute | Meaning | Format | Column | Source |
|---|---|---|---|---|
| Invoice number | Reference shown to the client | `INV-` + first 8 characters of the trade ID, upper case | `invoiceNumber` | `packages/db/src/services/invoiceService.ts:3-4` |
| Trade | The trade it documents (one invoice per trade) | — | `tradeId` | `packages/db/prisma/schema.prisma:90` |
| Created at | Issue time (same transaction as the trade) | automatic | `createdAt` | `schema.prisma:92` |

## PDF content

See BR-LIB-005 to BR-LIB-007: client details, a trade line, total, an illustrative fee, and a demo disclaimer.

## Lifecycle

Created together with the trade. Never changed or cancelled.

## Product comments
