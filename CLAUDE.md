# Business requirements reverse-engineering kit

This repo extracts business requirements from **other** applications' source code. The applications live elsewhere and are only read. Everything this kit generates stays in this repo.

## Layout

| Path | Contents |
|---|---|
| `kit/RULES.md` | Extraction rules: project resolution, evidence, confidence, IDs, checkpoints |
| `kit/procedures/re-*.md` | **Single source of truth** for every command |
| `.claude/commands/`, `.claude/agents/` | Claude Code wrappers that point to `kit/procedures/` |
| `.github/prompts/`, `.github/agents/`, `.github/copilot-instructions.md` | GitHub Copilot wrappers that point to `kit/procedures/` |
| `kit/templates/`, `kit/examples/` | Output templates and calibration examples |
| `kit/skeleton/requirements/` | Empty output structure, copied for each new project |
| `projects/<name>/project.md` | Target repo path and commit analysed |
| `projects/<name>/requirements/` | **Generated output** for that application, including `_run/` (plan, claims, log) |
| `projects/.active` | Name of the project the commands work on |

**When changing kit behaviour, edit `kit/` only.** Never put logic in the wrappers.

## Rules

@kit/RULES.md
