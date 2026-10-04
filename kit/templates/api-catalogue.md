# <Web services component> — API Catalogue

**Component:** `<repo path>` · **Prefix:** `<PREFIX>` · **Last extracted:** <YYYY-MM-DD> · **Status:** Draft

**Logic type** says where the business logic lives, which tells reviewers where to look for the rules:

| Logic type | Meaning |
|---|---|
| **Pass-through** | Forwards to back-office / a service with no business logic |
| **Orchestration** | Calls several downstream services in sequence; the order and the error handling are business-relevant |
| **Business logic** | Rules are implemented in the web service itself |
| **Data query** | Reads or writes the DB directly (SQL / ORM / stored procedure). Selection criteria and updates are rules. |

## Endpoints by business area

### <Business area, e.g. Trading>

| # | Method + path | Business operation | Consumers (screen / app / system) | Downstream (service / back-office / DB tables / stored proc) | Logic type | Auth / roles | Rules | Source |
|---|---|---|---|---|---|---|---|---|
| 1 | `POST /api/trades` | Place a trade | Front-end: Place order screen | Client svc (lock) → Cash svc → Stock svc | Orchestration | Client user | BR-API-001…004 | `path:line` |

## Cross-cutting behaviour (applies to all or many endpoints)

| Concern | Behaviour | Business-relevant? | Rules | Source |
|---|---|---|---|---|
| Authentication / session | | | | |
| Authorisation model | | | | |
| Common validation | | | | |
| Error responses / messages | | | | |
| Audit logging | | | | |
| Rate limits / idempotency keys | | | | |

## Unused or unmatched endpoints

| Method + path | Observation | Defect |
|---|---|---|
| | No consumer found in front-end / back-office / other services | D-API-… |
