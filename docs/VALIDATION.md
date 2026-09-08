# Validation

Validation has two levels.

## Repository validation

`python3 scripts/validate_repo.py` checks:

- required Skill/manifests/reference files exist;
- MCP/runtime configuration is absent;
- structured resources parse as JSON;
- variable index contains 359 entries;
- acceptance resource contains at least 20 cases;
- the root and packaged Skill both declare SQL generation rather than database execution;
- common write-SQL/admin verbs are prohibited by the Skill rules.

## Research validation

Generated SQL still requires study-specific review. In particular, candidate definitions, derived-table version semantics, unit/specimen choices, diagnosis/procedure code sets, medication exposure definitions and score definitions must be checked against the intended manuscript protocol and target MIMIC-IV installation.

A passing repository CI is not evidence that a specific study SQL has been executed successfully.
