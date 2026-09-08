# Procedures and treatments

Hospital procedures may be represented in `procedures_icd`; ICU bedside procedures/treatments may appear in `procedureevents`, `chartevents`, `inputevents`, or derived MIMIC Code concepts. Select the source based on the research meaning, not on label similarity.

For each procedure define whether the phenotype is billing-coded, device/event based, or derived; record code/itemid, version, start/end time, and analysis window. Examples include renal replacement therapy, invasive ventilation, vasopressors, surgery, and device placement.

QC should distinguish ordered vs performed treatment, overlapping events, duplicate codes, timing relative to ICU admission, and procedure definitions that change across MIMIC versions.
