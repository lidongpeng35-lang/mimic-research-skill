# Manuscript and supplement reporting

For reproducible MIMIC-IV extraction, record more than the database name. A Methods/Supplement package should preserve at least:

- MIMIC-IV version and installed optional products;
- MIMIC Code/derived version or commit when used;
- cohort phenotype and stepwise inclusion/exclusion counts;
- analysis unit and repeated-admission/stay selection rule;
- index time and every extraction window;
- source table/view, code/itemid/column, specimen/method and unit;
- variable role and aggregation/tie-breaking rules;
- unit conversion, missingness and plausibility/outlier handling;
- Contract revision and SHA-256;
- generated/reviewed SQL SHA-256;
- repository release/commit;
- definition maturity/provenance;
- QC summary including join multiplicity, duplicate handling and missingness.

Do not place patient-level records or restricted exports in a public supplement/repository. Share non-sensitive extraction specifications, code and hashes instead, subject to the applicable PhysioNet/MIMIC agreement.
