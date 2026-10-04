# Copilot instructions — business requirements reverse-engineering kit

This repository extracts business requirements from **another** application's source code. That application is opened as a second folder in the VS Code workspace and is **read-only**. Everything generated stays in this repository, under `projects/<name>/requirements/`.

## Before any `/re-*` task

1. Read [kit/RULES.md](../kit/RULES.md) in full. It is mandatory, and §0 tells you how to find the active project (`projects/.active`), the output folder `<OUT>`, and the application repo `<TARGET>`.
2. Read the procedure file in `kit/procedures/` named by the prompt, and follow it step by step.
3. Read [kit/examples/good-vs-bad-rules.md](../kit/examples/good-vs-bad-rules.md) before writing any rules.

## Non-negotiables (summary; RULES.md is authoritative)

- **Never create, edit or delete files in `<TARGET>`.** Never run git commands that change it.
- **Cite every rule** with a full `path:line` relative to `<TARGET>`, and give a confidence level (High / Medium / Low).
- **Write in business language.** Code names belong only in Source and Technical note.
- **Checkpoint after every entry point:** write the rules first, then tick `_progress.md`. On resume, continue from the first unticked entry point. Never redo ticked work.
- **New items are Draft.** Never change Status or Product comments, except through `/re-apply-review`.
- **Fresh chat per component.** When a procedure says to start a fresh session, start a new chat.
