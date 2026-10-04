# Work plan — <project>

**Created by** `/re-plan` on <YYYY-MM-DD> · **Target commit** <hash> · **Auto-commit after each row:** no
**Statuses:** Queued → Extracting → Extracted → Verifying → Verified (or Failed / Blocked with a reason)
**Claims** live in `_run/claims/<row-id>.claim`. A claim older than 4 hours is stale.
**Time estimate** (fill in after about 5 rows are done, from `run-log.md`): remaining ≈ Σ(remaining rows × average minutes for their size class) ÷ parallel sessions.

## Summary

| Wave | Theme | Rows | Queued | In progress | Extracted | Verified | Failed/Blocked |
|---|---|---|---|---|---|---|---|

## Rows

| Row ID | Wave | Component / slice | Folder | Prefix | Procedure | Size | Entry points | Depends on | Status | Started | Finished | EP done | Rules | Commit | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| W0-01 | 0 | Shared database | database | DB | re-domain | M | — | — | Queued | | | | | | |
| W1-01 | 1 | Client service | client-service | CLI | re-service | M | 24 | DB | Queued | | | | | | |
| W1-02 | 1 | Payments service (slice 1: controllers A–F) | payments-service | PAY | re-service | L | 60 | CLI | Queued | | | | | | Split from XL |
