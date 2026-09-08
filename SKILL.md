---
name: mimic-research-skill
description: Generate publication-oriented PostgreSQL SQL for MIMIC-IV data extraction from natural-language research requests. Resolve cohort, variables, time windows, aggregation and output grain against repository definitions; do not execute the database.
---

# MIMIC Research Skill

## Scope

Use this Skill only for MIMIC-IV data extraction design and SQL generation.

Primary task:

`natural-language research request -> explicit extraction specification -> MIMIC-IV mapping -> complete PostgreSQL SQL`

Do not use this Skill for:

- MIMIC-III or eICU unless the user explicitly requests a separate non-default analysis;
- database administration;
- patient-level query execution;
- CSV/XLSX export;
- downstream statistical modeling, causal inference, or manuscript result interpretation.

## Required workflow

### Step 1 — Parse the research request

Extract, when present:

- population / inclusion / exclusion criteria;
- analysis unit: patient, admission, ICU stay, event, or other explicit grain;
- stay-selection policy, e.g. first ICU stay;
- index time / anchor;
- requested variables;
- each variable's role: cohort filter, exposure, covariate, score, outcome, descriptive field;
- time window;
- aggregation: raw, first, last, min, max, mean, median, sum, count, duration, yes/no, etc.;
- output grain and identifiers.

Never silently infer a clinically meaningful choice when multiple plausible interpretations would materially change the result.

### Step 2 — Resolve definitions

Use repository resources before relying on model memory:

1. `resources/website-variable-index.json` for searchable controls and variable names;
2. `resources/current-definitions.json` for measurement/filter/window/anchor/aggregation definitions;
3. the most relevant file under `references/`;
4. source/provenance notes recorded in those resources.

Treat `status: candidate` as a candidate definition requiring study-specific review. Treat quarantined definitions as unusable unless the user explicitly asks to inspect them.

Do not invent or silently substitute:

- itemid;
- ICD-9/10 code;
- table or column;
- specimen type;
- unit conversion;
- score formula;
- time semantics;
- derived-table meaning.

If a requested concept has no reliable mapping, say it is unresolved and ask a focused question or provide a clearly labeled validation plan. Do not fabricate SQL for the unresolved component.

### Step 3 — Normalize the extraction specification

Before SQL, internally normalize the request to a specification with at least:

- `population`
- `analysis_unit`
- `stay_selection`
- `index_time`
- `variables[]`
  - concept
  - source/definition
  - role
  - window
  - aggregation
  - unit/specimen where relevant
- `output_grain`

Use half-open time windows `[start, end)` unless a source definition explicitly requires different semantics.

If aggregation is not specified and cannot be safely inferred, ask. Do not default all measurements to first/max/mean.

### Step 4 — Generate formal SQL

The final SQL must be complete PostgreSQL SQL, not pseudocode and not a placeholder scaffold.

Use the following structural rules:

- CTEs should separate cohort selection, stay selection, variable extraction, aggregation, and final assembly;
- joins must use explicit keys (`subject_id`, `hadm_id`, `stay_id`) appropriate to each table;
- one-to-many joins must be aggregated or semijoined before final assembly when the output grain is one row per patient/admission/stay;
- time filtering must be explicit relative to the chosen anchor;
- first/last values must use deterministic ordering and a documented tie-break policy;
- diagnosis/procedure code systems must distinguish ICD-9 from ICD-10;
- MIMIC-IV and MIMIC-III schema conventions must never be mixed;
- if `mimiciv_derived` is used, state the derived concept and any important dependency/time semantics;
- avoid DDL, writes, temporary destructive operations, privilege changes, and credential handling;
- do not include `INSERT`, `UPDATE`, `DELETE`, `DROP`, `ALTER`, `TRUNCATE`, `CREATE ROLE`, or similar administrative operations.

### Step 5 — Static quality review

Before presenting SQL, check:

- requested cohort logic is represented;
- analysis unit and final row grain match;
- first ICU / first admission logic, if requested, is explicit;
- every requested variable is present or explicitly unresolved;
- every time window is anchored correctly;
- aggregation matches the request;
- join multiplication cannot silently change the cohort;
- units/specimens are not silently mixed;
- aliases and CTE names are readable;
- SQL contains no write operations;
- assumptions are documented.

## Response format

For a substantive extraction request, return these sections in order:

1. **研究规格 / Extraction specification** — concise normalized interpretation.
2. **需要确认的歧义 / Blocking ambiguities** — only issues that materially change SQL. If none, say none.
3. **SQL** — one complete PostgreSQL code block.
4. **定义与来源 / Definition notes** — key table/field/derived/provenance notes and candidate-definition warnings.

If blocking ambiguity exists, do not pretend a single SQL is definitive. Either ask the minimum necessary question first, or present clearly labeled alternative SQL branches only when that is more useful.

## Research semantics rules

### Analysis unit

Always distinguish:

- patient-level (`subject_id`);
- hospitalization-level (`hadm_id`);
- ICU-stay-level (`stay_id`);
- event-level long-form outputs.

Do not use `DISTINCT` as a generic repair for an incorrect join.

### Time

MIMIC timestamps are deidentified and shifted. Use them for within-patient temporal relations, not as true real-world calendar dates/time zones.

For anchored windows, prefer:

```sql
WHERE event_time >= anchor_time + INTERVAL '0 hour'
  AND event_time <  anchor_time + INTERVAL '24 hour'
```

### Measurements

Same-name measurements may have multiple sources, itemids, specimens, or units. Resolve these explicitly. When using raw-event sources, return event time when it is important for auditability.

### First / last

Use deterministic ranking, typically `ROW_NUMBER()` with event time plus a stable secondary key when available. Do not rely on unordered `DISTINCT ON` or `MIN(value)` as a substitute for first observation.

### Scores

Prefer maintained MIMIC Code / validated derived concepts. Do not reconstruct SOFA, SAPS II, OASIS, LODS, Charlson, Sepsis-3, etc. from memory when a vetted definition is available.

### Diagnoses and procedures

Explicitly state whether codes are ICD-9 or ICD-10. Do not use truncated mappings unless the research definition explicitly calls for prefix/category matching.

### Medications

Distinguish prescription/order data from administered ICU input/infusion data. Drug name matching alone is not equivalent to dose-normalized exposure.

### Missingness

SQL generation should preserve missingness unless the study request explicitly defines imputation or a missing-value rule. Never silently coalesce missing clinical values to zero.

## Useful repository references

Start with the narrowest relevant file:

- `references/schema.md`
- `references/vital_signs.md`
- `references/labs.md`
- `references/diagnoses.md`
- `references/medications.md`
- `references/procedures.md`
- `references/scores.md`
- `references/outcomes.md`
- `references/cohort_design.md`
- `references/common_queries.md`
- `references/quality_control.md`
- `references/provenance.md`

## Final rule

The Skill succeeds when a researcher can inspect the SQL and understand exactly how the natural-language request was translated into MIMIC-IV data logic.

Do not claim that SQL was executed or that patient counts/results were observed unless the user independently provides those results.
