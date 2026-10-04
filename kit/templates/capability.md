# <Component name> — Capability

**Component:** `<repo path>` · **Prefix:** `<PREFIX>` · **Tech:** <stack> · **Last extracted:** <YYYY-MM-DD> · **Status:** Draft

## Purpose

<2–3 sentences in business terms: what this component is responsible for and why the business needs it.>

## Responsibilities

- <Business responsibility 1>
- <Business responsibility 2>

## Not owned here

<Things a reader might expect in this component that are actually handled elsewhere, with a pointer to where.>

## Entry points

| # | Type (API / Event / Job / File / Screen) | Name / route / topic | Business meaning | Called by | Rules | Source |
|---|---|---|---|---|---|---|
| 1 | API | `POST /clients/{id}/lock` | Reserve the client for a trade in progress | Front-end trade screen | BR-XXX-004 | `path:line` |

## Data owned / touched

| Entity | Access (Read / Write / Owner) | Notes |
|---|---|---|
| [ENT-Client](../../01-domain/entities/client.md) | Owner | |

## Dependencies

| Depends on | Why (business reason) | How (sync REST / async event / DB / file) | Source |
|---|---|---|---|

## Events / messages published

| Event / topic | Business meaning | Consumers | Source |
|---|---|---|---|

## Configuration with business meaning

| Key | Business meaning | Value in repo | Production value known? |
|---|---|---|---|

## Business rules

See [rules.md](rules.md). <Count by confidence: High n / Medium n / Low n.>

## Open questions and suspected defects

See [_questions.md](_questions.md) and [_defects.md](_defects.md).
