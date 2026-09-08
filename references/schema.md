# MIMIC-IV schema guide

Use schema-qualified names in research SQL. Core products commonly include `mimiciv_hosp` and `mimiciv_icu`; optional ED/Note/CXR/ECG products are separate datasets and must not be assumed installed.

Key grains: `subject_id` = patient, `hadm_id` = hospital admission, `stay_id` = ICU stay. ICU events should normally be assigned through `stay_id`; hospital labs/diagnoses commonly use `hadm_id`. Preserve all available identifiers through extraction and verify join cardinality before aggregation.

Common core tables include `patients`, `admissions`, `transfers`, `labevents`, `diagnoses_icd`, `procedures_icd`, `prescriptions`, `emar`, `emar_detail`, `icustays`, `chartevents`, `inputevents`, `outputevents`, `procedureevents`, `datetimeevents`, `d_items`, and `d_labitems`.

MIMIC timestamps are deidentified/shifted; they are suitable for within-patient temporal relationships but are not the patient's real calendar dates or timezone. Never mix MIMIC-III keys/table names (for example `icustay_id`, `inputevents_mv`) into MIMIC-IV SQL.

For derived concepts, prefer a versioned MIT-LCP MIMIC Code derived view when its definition matches the study, and record the MIMIC Code version/commit. Dictionary presence proves a label/code exists; it does not by itself validate a clinical definition.
