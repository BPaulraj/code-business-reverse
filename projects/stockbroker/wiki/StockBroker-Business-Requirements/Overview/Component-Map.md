> 🔄 **Generated** by the reverse-engineering kit from project `stockbroker` (code commit `ae607a6`, 2026-10-04, business view). **Do not edit this page**: changes are overwritten on the next publish. Give feedback through the review packs.

`/re-discover` fills this in. Correct it by hand if anything is wrong; every other command reads it.
**Folder** = the folder name under `requirements/03-capabilities/`.
**Prefix** = 2–4 letters used in rule, question and defect IDs. Never change a prefix once IDs exist.

| Component | Type | Repo path | Folder | Prefix | Tech stack | Invoked via | Notes |
|---|---|---|---|---|---|---|---|
| Front-end website (client portal) | UI (front-office) | `packages/web` | `front-end` | FO | React 18, Vite, React Query, Tailwind | Browser | Calls the web server only, through the `/api` proxy (`vite.config.ts:17-24`) |
| Web server (portal back end) | API layer (front-end ↔ DB) | `packages/server` | `web-server` | WEB | Node, Express 4, Zod, JWT in cookie | REST `/api/*`, port 4000 | Writes straight to the DB through Prisma. There is no separate back-office. |
| Public REST API | API layer (external clients ↔ DB) | `packages/api` | `public-api` | API | Node, Express 4, Zod, JWT bearer, Swagger | REST `/api/v1/*`, port 4100 | Added in commit `ae607a6`. Shares the DB with the web server. Much of its logic is duplicated from the web server. |
| Core library (shared domain services and validation) | Library | `packages/db/src/services`, `packages/db/src/mappers`, `packages/shared/src` | `core-library` | LIB | TypeScript, Zod, pdfkit | Imported by `server` and `api` (and `shared` by `web`) | Has its own folder because two components call it |
| Shared database | Database | `packages/db/prisma` (schema, migration, seed) | `database` | DB | SQLite via Prisma 5 (WAL mode) | — | One migration, `20260815131827_init` |
| Back-office website | — | — | — | — | — | — | **Not present** in this repo |
| Microservices | — | — | — | — | — | — | **Not present** |
| Batch jobs | — | — | — | — | — | — | **Not present**: no scheduler, cron or job code found |
| Connectivity components | — | — | — | — | — | — | **Not present**: payments and prices are simulated in-process |

## External systems (third parties)

| Counterparty | Integration ID | Connected through component | Protocol / format | Notes |
|---|---|---|---|---|
| _None_ | — | — | — | Market prices are simulated (`packages/db/src/services/priceService.ts:1-9`). Bank and card payments are simulated with a fixed delay (`packages/server/src/modules/wallet/walletRoutes.ts:69-70`). |
