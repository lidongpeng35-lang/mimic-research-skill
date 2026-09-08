# Common research query patterns

These are patterns, not publication-ready phenotypes. Resolve all concepts and codes before execution.

## First ICU stay per patient

```sql
WITH ranked AS (
  SELECT i.*,
         ROW_NUMBER() OVER (PARTITION BY subject_id ORDER BY intime, stay_id) AS rn
  FROM mimiciv_icu.icustays i
)
SELECT * FROM ranked WHERE rn = 1;
```

Only use this when the study explicitly chooses first ICU stay.

## ICU-centered event window

```sql
SELECT e.*
FROM cohort c
JOIN some_event_table e ON e.stay_id = c.stay_id
WHERE e.charttime >= c.intime
  AND e.charttime <  c.intime + INTERVAL '24 hour';
```

Use the correct event key/time column. Hospital-level events may require `hadm_id` plus temporal assignment.

## First eligible measurement

```sql
WITH eligible AS (...),
ranked AS (
  SELECT e.*,
         ROW_NUMBER() OVER (
           PARTITION BY stay_id
           ORDER BY charttime, source_priority, itemid
         ) AS rn
  FROM eligible e
)
SELECT * FROM ranked WHERE rn = 1;
```

Define `eligible` (specimen, unit, value type, window) before ranking and specify deterministic tie-breaking.

## Avoid accidental cohort multiplication

Build the base cohort at one row per analysis unit, aggregate each one-to-many domain separately, and only then join summary tables back to the cohort. Do not use `SELECT DISTINCT` as a substitute for understanding join cardinality.

## Read-only safety

Generated research SQL should be SELECT/CTE based and executed with a read-only database role, statement timeout, preview row limit, and controlled export. Never interpolate arbitrary user text as SQL identifiers or fragments.
