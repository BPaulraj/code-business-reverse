# Templates for _questions.md and _defects.md

Every output folder has its own `_questions.md` and `_defects.md`. Copy the matching header below when creating one.
Append rows; never delete them. `/re-coverage` consolidates them into `06-open-questions.md` and `07-suspected-defects.md`.

---

## _questions.md

```markdown
# Open questions — <folder / component>

| ID | Question for product | What the code does today | Related | Raised | Answer | Status |
|---|---|---|---|---|---|---|
| Q-XXX-001 | Should a locked client be unlocked automatically after 30s? | Lock expires after 30s via config `client.lock.ttl` (`path:line`) | BR-XXX-004 | YYYY-MM-DD | | Open |
```

Status values: Open · Answered · Not needed

---

## _defects.md

```markdown
# Suspected defects — <folder / component>

| ID | Observation | Evidence | Possible impact | Related | Raised | Decision | Status |
|---|---|---|---|---|---|---|---|
| D-XXX-001 | UI limits quantity to 10,000 but service limits to 50,000 | `fe/...:12`, `svc/...:88` | Users blocked from valid trades | BR-FO-003, BR-STK-007 | YYYY-MM-DD | | Open |
```

Kinds of things that belong here:
- likely bugs
- dead or unreachable code
- hard-coded client or account special cases
- contradictory copies of a rule
- missing compensation when a step fails
- security or permission gaps noticed in passing

Status values: Open · Confirmed bug · Intended (becomes a rule) · Won't fix
