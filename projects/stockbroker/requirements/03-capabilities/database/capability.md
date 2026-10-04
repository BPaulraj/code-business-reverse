# Shared database — Capability

**Component:** `packages/db/prisma` · **Prefix:** `DB` · **Tech:** SQLite (WAL mode) via Prisma 5 · **Last extracted:** 2026-10-04 · **Status:** Extracted

## Purpose

The single store for all business data. It is shared by the web server and the public API, which run as two independent processes.

## Responsibilities

- Persist clients, wallets, wallet transactions, companies, holdings, trades, invoices and inbox messages.
- Enforce uniqueness rules: email, ticker, one wallet per client, one holding per client and company, one invoice per trade.
- Supply the company reference data (seed).

## Not owned here

No business logic lives in the database: there are no triggers, stored procedures, views or CHECK constraints (`packages/db/prisma/migrations/20260815131827_init/migration.sql`). All rules are in application code.

## Entry points

| # | Type | Name | Business meaning | Source |
|---|---|---|---|---|
| 1 | Migration | `20260815131827_init` | Creates all 8 tables | `migration.sql:1-107` |
| 2 | Seed script | `prisma/seed.ts` | Loads or refreshes the 41 tradable companies | `packages/db/prisma/seed.ts:49-58` |

## Technical tables

None.

## Configuration with business meaning

| Key | Business meaning | Value in repo | Production value known? |
|---|---|---|---|
| `DATABASE_URL` | Database location | `file:./dev.db?connection_limit=1` | No. A comment mentions Azure SQL / Postgres for production (`packages/db/src/prisma.ts:10-11`). |
| `busy_timeout` | How long a write waits for the other process | 5000 ms | `packages/db/src/prisma.ts:20` |

## Business rules

See [rules.md](rules.md). High 9 / Medium 1 / Low 0.
