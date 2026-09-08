# Extraction quality control

Minimum QC for a publication-oriented extraction:

1. Cohort grain: row count and distinct `subject_id`/`hadm_id`/`stay_id` at every major step.
2. Join multiplicity: compare before/after counts and never hide unexplained multiplication with `DISTINCT`.
3. Time windows: verify min/max event offsets from the confirmed anchor and boundary cases.
4. Units/specimens: tabulate unit and specimen/method distributions before normalization.
5. Duplicates/ties: define deterministic handling for same-time measurements.
6. Missingness: report absence separately from exclusion and characterize missingness by key strata when relevant.
7. Plausibility: flag implausible values; do not silently delete them without a documented rule.
8. Reproducibility: save Contract revision/hash, SQL hash, software commit/version, source definition/version, and QC summary.

A query that executes without SQL error has passed syntax/execution, not clinical validation.
