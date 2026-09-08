# Diagnoses and comorbidities

MIMIC-IV diagnosis rows are in `mimiciv_hosp.diagnoses_icd` with descriptions in `d_icd_diagnoses`. Always preserve and filter on `icd_version`; ICD-9 and ICD-10 code systems must not be mixed as if they were one vocabulary.

A diagnosis-code match is not automatically a cohort phenotype. For diseases such as sepsis, AKI, heart failure, diabetes, CKD, or MI, state whether the study uses billing ICD codes, a derived clinical phenotype, organ-dysfunction logic, treatment/lab criteria, or a published algorithm. Record code lists and version provenance.

For comorbidity indices, prefer a versioned, reviewable implementation (for example MIT-LCP MIMIC Code Charlson) when appropriate. Do not reconstruct a score from incomplete ad-hoc code groups and label it equivalent.

QC: code-system version, principal vs secondary diagnosis handling, admission/stay linkage, lookback period, duplicate code rows, and phenotype sensitivity analyses when materially relevant.
