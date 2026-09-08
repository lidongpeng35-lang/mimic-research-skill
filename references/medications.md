# Medications

Medication evidence can come from `prescriptions`, `emar`/`emar_detail`, and ICU `inputevents`; these represent different stages of the medication process. Do not treat an order, an administration record, and a continuous ICU infusion as interchangeable exposure definitions.

For each drug specify generic/ingredient concept, route, exposure source, start/stop logic, ICU/hospital window, dose/rate unit, and whether the study needs ordered, administered, or infused medication. Continuous vasoactive doses require explicit normalization and unit handling. Resolve raw itemids/medication strings against the target MIMIC version and retain provenance.

QC should cover duplicate administrations, cancelled/held orders, overlapping infusions, unit variants, weight normalization, and one-to-many join inflation.
