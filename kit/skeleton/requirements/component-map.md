# Component Map

`/re-discover` fills this in. Correct it by hand if anything is wrong; every other command reads it.
**Folder** = the folder name under `<OUT>/03-capabilities/`.
**Prefix** = 2–4 letters used in rule, question and defect IDs. Never change a prefix once IDs exist.

| Component | Type | Repo path | Folder | Prefix | Tech stack | Invoked via | Notes |
|---|---|---|---|---|---|---|---|
| Front-end website | UI (front-office) | `Code/Websites/front-end` | `front-end` | FO | TBD | Browser | |
| Back-office website | UI (back-office) | `Code/Websites/back-end` | `back-office` | BO | TBD | Browser | |
| Web services (REST API) | API layer (front-end ↔ back-office / DB) | TBD | `web-services` | API | TBD | REST | Extract with `/re-api` |
| Batch jobs (nightly) | Batch | TBD | `batch-jobs` | BAT | TBD | Scheduler: TBD (in repo or external) | Extract with `/re-batch`; add a row per separate batch application |
| Client service | Microservice | `Code/Microservice/client service` | `client-service` | CLI | TBD | TBD | |
| Cash service | Microservice | `Code/Microservice/cash service` | `cash-service` | CSH | TBD | TBD | |
| Stock service | Microservice | `Code/Microservice/stock service` | `stock-service` | STK | TBD | TBD | |
| _Connectivity component(s)_ | Integration | TBD | TBD | TBD | TBD | TBD | One row per adapter |
| Shared database | Database | TBD (migrations / DDL / procs) | `database` | DB | TBD | — | |
| _Shared libraries_ | Library | TBD | TBD | TBD | TBD | — | One caller: its rules belong to that caller. Two or more callers: the library gets its own folder and prefix (RULES §6a). |

## External systems (third parties)

| Counterparty | Integration ID | Connected through component | Protocol / format | Notes |
|---|---|---|---|---|
| TBD | INT-001 | TBD | TBD | |
