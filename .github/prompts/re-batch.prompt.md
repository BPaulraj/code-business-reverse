---
description: Phase 2c – inventory nightly batch jobs (schedule, dependencies) and extract each job's input selection, rules, outputs, file layouts and re-run behaviour. Resumable; supports job ranges.
argument-hint: "<batch component folder> [inventory | BJ-001..BJ-020 | BJ-007]"
agent: agent
---

Read and follow [the re-batch procedure](../../kit/procedures/re-batch.md) exactly. It is the single source of truth for this command.
First read [the rules](../../kit/RULES.md) and resolve `<OUT>` and `<TARGET>` (§0).

ARGUMENTS: whatever the user typed after the prompt name in their message. If nothing was typed and the procedure needs arguments, ask for them.
