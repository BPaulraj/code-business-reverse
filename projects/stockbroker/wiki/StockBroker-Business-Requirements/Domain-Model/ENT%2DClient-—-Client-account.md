> 🔄 **Generated** by the reverse-engineering kit from project `stockbroker` (code commit `ae607a6`, 2026-10-04, business view). **Do not edit this page**: changes are overwritten on the next publish. Give feedback through the review packs.

[[_TOC_]]

**Status:** Draft · **Owner component:** Web server / Public API (registration, profile) · **Stored in:** `User`

## Definition

A person who has registered on the platform with an email and password. A client owns exactly one wallet, and can hold shares, place trades and receive inbox messages.

## Identifiers

| Identifier | Business meaning | Source |
|---|---|---|
| Client ID | System-generated unique ID (UUID) | `packages/db/prisma/schema.prisma:11` |
| Email | Login identifier. Unique across all clients and stored in lower case. | `schema.prisma:13`, `packages/shared/src/index.ts:200` |

## Key attributes

| Attribute | Meaning | Allowed values / format | Column | Source |
|---|---|---|---|---|
| Name | Full name | 1–100 characters | `name` | `packages/shared/src/index.ts:199` |
| Email | Login and contact email | Valid email, lower-cased, unique | `email` | `index.ts:200`, `schema.prisma:13` |
| Phone | Contact phone | 7–20 characters: digits, `+ - ( )` and space | `phone` | `index.ts:201-206` |
| Address | Postal address (optional) | ≤ 200 characters | `address` | `index.ts:224` |
| KYC status | Verification state | Unverified (default) / Pending / Verified | `kycStatus` | `schema.prisma:17`, `index.ts:19` |
| Member since | Registration date-time | Set automatically | `memberSince` | `schema.prisma:18` |
| Password | Stored only as a one-way hash | ≥ 8 characters, at least one letter and one digit | `passwordHash` | `index.ts:192-196`, `packages/server/src/modules/auth/authRoutes.ts:38` |

## Lifecycle

There is no account status (active / closed / locked). The only state-like attribute is KYC status.

| From state | To state | Trigger / who | Rules | Source |
|---|---|---|---|---|
| — | Registered, KYC Unverified | Self-registration | BR-WEB-007…010, BR-DB-001, BR-DB-006 | `authRoutes.ts:26-60` |
| KYC Unverified | KYC Pending / Verified | **No code found** that changes KYC status | — | Grep `kycStatus` writes: none (Q-DOM-001) |

::: mermaid
stateDiagram-v2
    [*] --> Registered_KYC_Unverified : self-registration
    Registered_KYC_Unverified --> Registered_KYC_Unverified : profile edit (name, phone, address)
:::
## Relationships

| Related entity | Relationship | Cardinality |
|---|---|---|
| [Wallet](/Business-Requirements/StockBroker-Business-Requirements/Domain-Model/ENT%2DWallet-%E2%80%94-Cash-wallet) | owns | exactly 1 (created at registration) |
| [Holding](/Business-Requirements/StockBroker-Business-Requirements/Domain-Model/ENT%2DHolding-%E2%80%94-Share-holding-%28position%29) | owns | 0..n (one per company) |
| [Trade](/Business-Requirements/StockBroker-Business-Requirements/Domain-Model/ENT%2DTrade-%E2%80%94-Trade) | places | 0..n |
| [Inbox message](/Business-Requirements/StockBroker-Business-Requirements/Domain-Model/ENT%2DInboxMessage-%E2%80%94-Inbox-message) | receives | 0..n |

## Constraints and DB-resident rules

- BR-DB-001: email unique
- BR-DB-006: KYC defaults to Unverified
- BR-DB-010: a client can't be deleted while related records exist

## Product comments
