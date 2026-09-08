# Laboratory tests

Raw hospital laboratory results are primarily in `mimiciv_hosp.labevents` and their dictionary in `mimiciv_hosp.d_labitems`. Many publication workflows can also use versioned `mimiciv_derived` laboratory views when their definitions match the study.

Do not map a lab by label alone. Resolve itemid, specimen/fluid, method where relevant, numeric versus text result, unit, and the MIMIC version. Common high-value labs include creatinine, BUN, sodium, potassium, bicarbonate, chloride, glucose, lactate, bilirubin, albumin, AST/ALT, hemoglobin, WBC, platelets, INR/PT/PTT, and blood-gas variables.

Hospital labs commonly attach by `hadm_id`; assign them to an ICU stay only with an explicit temporal rule. For an ICU-centered window, define whether pre-ICU values are allowed and use explicit half-open boundaries. Never silently convert units; retain raw value/unit and record conversion rules.

If a user says “24 h lactate” without first/max/mean/etc., return eligible raw events. For first/last, define tie-breaking. For extrema/means/medians, define the eligible specimen/unit set before aggregation.

QC: unit distribution, specimen distribution, duplicate events, text/number mismatch, impossible values, missingness by cohort subgroup, and event-to-stay assignment.
