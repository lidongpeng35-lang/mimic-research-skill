# MIMIC Research Skill

A focused research Skill for **MIMIC-IV data-extraction SQL generation**.

Its job is deliberately narrow:

> **natural-language research request → explicit study semantics → MIMIC-IV table/field/definition mapping → reviewable, reproducible PostgreSQL SQL**

This repository does not connect to a database, execute patient-level queries, export data, or expose an MCP server.

## Current v0.2 resources

- `resources/core-registry.json`: a first curated set of high-frequency MIMIC-IV cohort, measurement, score, treatment, medication and outcome concepts;
- `resources/acceptance-cases.json`: 20 natural-language behavior acceptance cases;
- `references/`: schema, vitals, labs, diagnoses, medications, procedures, scores, outcomes, cohort design, QC and provenance guidance;
- `SKILL.md`: normative agent instructions.

A larger variable/definition resource set prepared during development is being migrated into the pure-Skill structure. It is not counted as an online repository capability until committed and validated by CI.

## Workflow

For a request such as:

> Build a first-ICU-stay sepsis cohort and extract first lactate in 0–24 h, maximum SOFA, mechanical ventilation exposure, norepinephrine exposure, and 28-day mortality.

The Skill should identify the cohort and study semantics, resolve definitions against repository resources, ask only for ambiguities that materially change the SQL, generate complete PostgreSQL SQL, and report key provenance/assumptions.

## Principles

Use MIMIC-IV only; define semantics before SQL; never invent itemids/ICD/table/unit/score logic; do not silently choose first/max/mean when aggregation is unspecified; treat dictionary matches as candidates rather than proof of clinical equivalence; prefer official MIMIC-IV and MIT-LCP MIMIC Code logic; produce explicit CTE-based PostgreSQL with clear join keys and time boundaries; and never claim database execution from this repository.

## Validation

```bash
python3 scripts/validate_repo.py
```

CI validates the Skill package, core registry, acceptance cases, and absence of MCP/runtime execution surfaces. It does not claim that generated SQL has been executed against patient data.

Primary technical provenance: MIMIC-IV documentation, PhysioNet, and MIT-LCP MIMIC Code. The lightweight public repository `yongfanbeta/mimic-skill` informed presentation structure only.
