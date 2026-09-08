# Definition lifecycle

Clinical mappings should move through explicit maturity states rather than being treated as correct because they compile.

- `candidate`: a plausible mapping with recorded provenance; requires study-specific review.
- `validated`: tested against the intended MIMIC/MIMIC Code version with documented clinical and technical checks.
- `quarantined`: known ambiguity, mismatch, defect, or unsupported source prevents routine use.

Promotion to `validated` should include source/version provenance, semantic rationale, unit/specimen/method checks where relevant, timing behavior, positive/negative test cases, and regression evidence. A label or itemid dictionary match alone is insufficient.

Material changes to code lists, itemids, formulas, time semantics, unit conversion, or aggregation should be treated as a new definition revision and revalidated.
