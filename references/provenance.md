# Definition provenance

Use an evidence hierarchy rather than model memory. Preferred sources are: target MIMIC schema/dictionaries; official MIMIC-IV documentation/PhysioNet descriptions; versioned MIT-LCP MIMIC Code definitions; then peer-reviewed study definitions with an explicit rationale.

For each executable concept record: internal concept ID, source product/schema/table/view, code/itemid/column, specimen/method, unit, value type, transformation, time semantics, source version/commit, and validation status.

Statuses should distinguish at least `candidate`, `validated`, and `quarantined`. “Registered” means the system can resolve the concept; it does not mean every study may treat it as publication-grade without review.

When sources disagree, preserve both candidates and document the study-specific choice. Never silently overwrite provenance because a newer label looks similar.
