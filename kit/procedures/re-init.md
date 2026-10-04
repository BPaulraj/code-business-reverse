# /re-init — Register (or switch to) an application to reverse-engineer. Creates projects/<name>/ in this kit repo; the application repo is never written to.

**ARGUMENTS:** `<project-name> [path-to-application-repo]` — the text supplied with the command.

**Arguments:** `ARGUMENTS`. The first word is the project name (kebab-case). The rest, if present, is the path to the application repo.

## If `projects/<name>/project.md` already exists (switching project)

1. Write `<name>` to `projects/.active`.
2. Read `project.md` and check that the target path is readable. If it isn't, tell the user to grant access (RULES §0 step 4).
3. Show the project summary and the coverage-tracker status. Stop.

## If it is a new project

1. **The repo path is required.** Check that it exists and is readable. If it isn't readable, tell the user to grant access (RULES §0 step 4), then stop.
2. **Record the analysed version** with read-only git commands in the target: current branch, `git rev-parse HEAD`, and whether the working tree is clean (`git status --porcelain`). If it isn't a git repo, record "not a git repo" and today's date.
3. **Create the project folder.** Copy the skeleton `kit/skeleton/requirements/` to `projects/<name>/requirements/`, including the empty folders.
4. **Write `projects/<name>/project.md`:**

   ```markdown
   # Project: <name>

   | Field | Value |
   |---|---|
   | Target repo | <absolute path> |
   | Branch | <branch> |
   | Commit analysed | <full hash> |
   | Working tree clean at start | yes / no |
   | Initialised | <YYYY-MM-DD> |
   | Output formats | md, docx, pdf — whatever the user prefers. Ask if not given; `md` alone is the minimum. |
   | SQL default schema | dbo (MS SQL Server); (none) for engines without schemas |
   | Word template | (optional) path to a corporate .docx whose styles are used for Word output |
   | Wiki publishing | off — off (default): never upload; on-request: upload when the user runs /re-wiki; auto: also upload at the end of /re-publish. Ask the user; if unsure, keep off. |
   | ADO org URL | (optional, for /re-wiki) e.g. https://dev.azure.com/myorg or https://ado.mycorp.local/DefaultCollection |
   | ADO project | (optional, for /re-wiki) |
   | Wiki name | (optional) default: the project wiki |
   | Wiki parent path | (optional) e.g. Business Requirements |
   | Wiki view | business |
   | Wiki split threshold | 25 |
   | ADO API version | 7.1 (cloud); 7.0 for Azure DevOps Server 2022; 6.0 for Server 2020 |

   All citations in `requirements/` are relative to the Target repo at the commit above.
   If the code moves on, record the new commit here with a date, before re-extracting.

   ## Notes
   ```

5. **Write `<name>`** to `projects/.active`.
6. **Never write anything into the target repo.** Never write an access token into `project.md`. The ADO token comes only from the `ADO_PAT` environment variable (or a local, git-ignored `ado.properties`).
7. **Final message:** the project path, the recorded commit, and the next step: `/re-discover`.
