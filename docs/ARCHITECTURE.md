# Architecture

MIMIC Research Skill is intentionally a **static SQL-generation Skill**, not a database runtime.

```text
Natural-language research request
        |
        v
SKILL.md semantic workflow
        |
        +--> resources/website-variable-index.json
        +--> resources/current-definitions.json
        +--> references/*.md
        |
        v
Normalized extraction specification
        |
        v
Complete PostgreSQL SQL + definition notes
```

There is no MCP server, database executor, patient-data preview service, or export runtime in the repository.

The host model performs language understanding and SQL composition under the constraints in `SKILL.md`; repository resources provide structured definitions and provenance constraints. CI validates package integrity and research-safety rules, not patient-data execution.
