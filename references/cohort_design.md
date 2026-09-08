# Cohort design

Freeze cohort semantics before variable extraction. Record population source, inclusion/exclusion, disease phenotype, age rule, ICU/admission selection, analysis unit, index time, and row grain.

Do not add “adult only”, “first ICU stay”, minimum length of stay, or complete-case restrictions unless the protocol requests them. If multiple ICU stays/admissions are eligible, specify whether all are retained or how one is selected.

Separate cohort filters from event-level filters. A lab criterion used to define eligibility may require different timing from the same lab used as an output predictor. Use explicit half-open windows and state whether pre-index values are eligible.

QC: base counts after each inclusion/exclusion step, distinct subject/hadm/stay counts, overlap of exclusion rules, repeated stays, and the exact point at which post-index information enters the cohort.
