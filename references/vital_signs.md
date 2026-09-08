# Vital signs

Preferred route: resolve a registered derived concept (for example `mimiciv_derived.vitalsign`) when the target MIMIC Code version is installed and matches the intended definition. Otherwise resolve raw `chartevents.itemid` values through `d_items` and document every included itemid/unit.

Typical concepts: heart rate, systolic/diastolic/mean blood pressure, respiratory rate, temperature, SpO2, and bedside glucose. Do not assume one itemid per concept; invasive/non-invasive BP, Fahrenheit/Celsius temperature, and device-specific recordings may need explicit harmonization.

For ICU-window extraction use the confirmed ICU anchor, normally `icustays.intime`, with explicit boundaries such as `[0h,24h)`. If no aggregation is requested, return event-level data. If first/last is requested, define tie-breaking. If min/max/mean/median is requested, define eligible records and unit conversion before aggregation.

QC: check duplicate timestamps, implausible values, mixed units, unexpected multiple stays, and whether join logic multiplies measurements. Preserve source time, raw value, raw unit, itemid/source column, and stay identifiers for auditability.
