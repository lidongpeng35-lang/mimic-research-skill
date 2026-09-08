# Outcomes

Define each outcome with an anchor, horizon, censoring rule, and source. Distinguish ICU mortality, in-hospital mortality, and fixed-horizon mortality; they are not interchangeable.

Hospital mortality can use `admissions.hospital_expire_flag` when appropriate. ICU mortality requires an explicit relation between death time and ICU stay. Fixed-horizon mortality requires a stated index time and available follow-up semantics. Do not infer a 28/90-day outcome if the required death/follow-up data are unavailable in the installed product/version.

QC: index-time alignment, deaths after discharge, competing discharge/censoring conventions, duplicate admissions/stays, and whether the target is patient-, admission-, or stay-level.
