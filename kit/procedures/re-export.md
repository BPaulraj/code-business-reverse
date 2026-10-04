# /re-export — Export a generated Markdown document to Word and/or PDF

**ARGUMENTS:** `[<file.md>] [docx | pdf | both] [template=<corporate.docx>]`
- **File:** defaults to `projects/<name>/deliverables/Business-Requirements-Specification.md`.
- **Format:** defaults to the project's **Output formats** preference in `projects/<name>/project.md` (any of `md`, `docx`, `pdf`). If none is set, ask the user once and record the answer there.
- **Template:** defaults to the **Word template** in `project.md`, if set.

Follow `kit/RULES.md` §0 to resolve the active project.

## Steps

1. **Resolve the file, formats and template** as above. `md` needs no export; it's the source.
2. **Check prerequisites** (run once per machine, read-only checks):
   - `python --version` (3.9+) and `python -c "import docx"`.
   - If `python-docx` is missing, tell the user to run `pip install -r kit/tools/requirements.txt` (or install it from their internal package mirror) and stop. **Don't install packages without the user's agreement.**
3. **Run the exporter:**
   ```
   python kit/tools/export_doc.py "<file.md>" --format <docx|pdf|both> [--template "<template.docx>"]
   ```
   - It writes `<name>.docx` / `<name>.pdf` next to the Markdown file.
   - **PDF engine:** Edge or Chrome in headless mode by default. Each browser is tested before use. Microsoft Word is the fallback (`--pdf-engine word` forces Word).
   - **Diagrams** are rendered offline with the bundled Mermaid. If a diagram fails to render, its source is shown instead, and the console names the diagram and the error.
   - **Word** (if installed) is used to refresh the table of contents and page numbers in the `.docx`.
4. **Report a diagram error as a source problem.** A diagram error means the Markdown diagram is invalid (it would also fail on GitHub). Fix it in the **working file** it came from, then regenerate. Never patch the exported files.
5. **Final message:** the files written with their sizes, the diagrams rendered (n/n), the engine used, and any warnings.

## Notes

- Exported files are **generated artefacts**: regenerate them, never edit them. To change styling or branding, pass a corporate Word template, whose styles (headings, tables, fonts) are reused.
- Review packs can be exported too, e.g. `/re-export projects/<name>/requirements/_review/<pack>.md docx`, so product can fill in decisions in Word. Copy their decisions back into the Markdown pack before running `/re-apply-review`.
