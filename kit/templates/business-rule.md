# <Component name> — Business Rules

**Component:** `<repo path>` · **Prefix:** `<PREFIX>` · **Capability:** [capability.md](capability.md)

## Summary

| ID | Title | Confidence | Status |
|---|---|---|---|
| BR-XXX-001 | | High / Medium / Low | Draft |

---

<!-- Copy this block for each rule. Keep the field names exactly as written; the scripts and commands rely on them. -->

### BR-XXX-NNN — <Short title in business words>

- **Statement:** <One decision, in business language. "When …, the system …">
- **Rationale (inferred):** <Why the business would want this. Leave blank if unknown.>
- **Trigger:** <The event, user action, message or schedule that applies the rule>
- **Conditions / exceptions:** <Thresholds, roles, states, time windows, exemptions>
- **Outcome on violation:** <Rejected with message "…", queued for approval, alert raised, …>
- **Used in:** <P-NNN, UJ-FO-NNN, entry point # in capability.md>
- **Source:**
  - `path/to/File.ext:120-145` — <what this code does>
  - `path/to/Test.ext:30` — test evidence
- **Confidence:** High | Medium | Low
- **Technical note:** <Mechanism, config keys, duplicates in other layers, "Reachability unconfirmed", verifier corrections>
- **Related:** <Q-XXX-NNN, D-XXX-NNN, BR-…>
- **Status:** Draft
- **Product comments:**
