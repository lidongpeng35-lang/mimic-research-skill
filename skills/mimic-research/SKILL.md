---
name: mimic-research-skill
description: Generate publication-oriented PostgreSQL SQL for MIMIC-IV data extraction from natural-language research requests. Resolve cohort, variables, time windows, aggregation and output grain against repository definitions; do not execute the database.
---

# MIMIC Research Skill

Use this packaged Skill with the repository root `SKILL.md` as the normative specification. The Skill performs only MIMIC-IV extraction design and SQL generation.

Workflow: parse the natural-language request; resolve definitions against `resources/website-variable-index.json`, `resources/current-definitions.json`, and `references/`; normalize cohort/analysis-unit/index-time/window/aggregation/output-grain semantics; generate complete PostgreSQL SQL; perform static review for join multiplicity, time-window, unit/specimen, aggregation, and MIMIC-IV schema errors.

Never execute patient queries, expose credentials, fabricate itemids/ICD/table/unit/score definitions, or claim observed patient results. Candidate definitions require study-specific validation; quarantined definitions must not be used as execution authority.

For full rules, read the repository root `SKILL.md`.
