---
name: mimic-research-skill
description: Evidence-backed MIMIC-IV cohort and clinical-variable extraction for ICU research. Use for MIMIC-IV cohort definitions, variable/code/itemid resolution, reproducible SQL, time-windowed extraction, QC, preview, and controlled export. Do not use for eICU or unrestricted patient-data queries.
---

# MIMIC-IV Research Data Extraction Skill

Convert a natural-language research question into an auditable MIMIC-IV extraction specification and PostgreSQL query. The governing principle is simple: do not invent `itemid`, ICD codes, tables, units, formulas, cohort definitions, or validation results from memory.

## Workflow

1. Parse the complete research question: population, inclusion/exclusion, analysis unit, index time, time window, variables, aggregation, missingness, and output grain.
2. Resolve every named clinical concept against the bundled references/registry before compiling SQL.
3. Keep materially different candidates separate. If a mapping is unresolved, say so instead of selecting the closest label.
4. Freeze the complete request as a versioned Contract.
5. Compile the Contract to SQL and preserve a SQL hash/provenance record.
6. With an authorized read-only database, run only a controlled Preview first.
7. Check cohort grain, joins, time windows, duplicates, units, missingness, and row multiplicity.
8. Any material revision creates a new Contract revision and invalidates earlier Preview/export approval.
9. Final CSV/XLSX export requires the current revision to have passed Preview and the exact phrase `确认导出`.

## Research semantics

A complete extraction specification should record:

- dataset and dependency version;
- population and disease definition;
- analysis unit (`subject_id`, `hadm_id`, or `stay_id`);
- ICU-selection rule and time zero;
- each variable's role (filter/output/both);
- source table/view and code/itemid/column;
- specimen/method and unit when relevant;
- time anchor and half-open window boundaries;
- raw records or explicit aggregation (first/min/max/mean/median/etc.);
- tie-breaking, duplicate, missingness, conversion, and outlier rules;
- expected columns and final row grain.

If a measurement window is requested without an aggregation, default to event-level raw records rather than silently selecting first/max/mean.

## Schema boundaries

MIMIC-IV core, MIMIC-IV-ED, MIMIC-IV-Note, MIMIC-CXR, and MIMIC-IV-ECG are separate products. Do not assume optional products are installed. ICU stays use `stay_id`; hospital events commonly use `hadm_id`; patient-level data use `subject_id`. MIMIC timestamps are deidentified/shifted and must not be interpreted as real patient calendar time.

## Query rules

- Build the cohort once at the confirmed analysis unit.
- Preserve `subject_id`, `hadm_id`, and `stay_id` where available.
- Use explicit time windows such as `event_time >= intime AND event_time < intime + INTERVAL '24 hour'`.
- Separate cohort selection, event filtering, calculated-result filtering, and output display.
- Preserve raw value/unit/source identifiers when normalizing data.
- Never hide join multiplication with `DISTINCT` before understanding the join cardinality.
- Parameterize user-controlled values and never splice arbitrary user text into SQL identifiers/fragments.

## Quality control

Before calling an extraction ready, verify:

- row grain and distinct analysis-unit counts;
- expected stay/admission assignment;
- window boundaries and timestamps;
- duplicate/tie behavior;
- source, specimen/method, unit, and value type;
- compatible unit handling;
- missingness versus exclusion;
- implausible-value handling;
- final columns/order/types.

Treat zero rows, unresolved definitions, missing sources, database unavailability, and SQL failure as different outcomes.

## Offline behavior

Without an authorized database, static concept resolution, Contract design, SQL generation, and validation planning may proceed, but outputs must be labeled `not executed`. Never fabricate patient rows, sample size, prevalence, missingness, or export receipts.

## Reference map

- `references/schema.md`
- `references/vital_signs.md`
- `references/labs.md`
- `references/diagnoses.md`
- `references/common_queries.md`
- `references/medications.md`
- `references/procedures.md`
- `references/scores.md`
- `references/outcomes.md`
- `references/cohort_design.md`
- `references/quality_control.md`
- `references/provenance.md`
- `references/python_usage.md`
- `references/runtime.md`
- `references/security.md`
