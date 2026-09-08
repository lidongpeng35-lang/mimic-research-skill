# Natural language to SQL example

## Request

> MIMIC-IV 中首次 ICU 入住的成人患者，以 ICU 入科为 time zero，提取 0–24 h 首次乳酸、最大 SOFA、机械通气暴露和 28 天死亡。

## Normalized interpretation

- analysis unit: ICU stay (`stay_id`)
- stay selection: first ICU stay per patient (must be stated explicitly in a real study protocol)
- index time: `icustays.intime`
- lactate: first value in `[0,24h)`
- SOFA: maximum score in `[0,24h)` only if the chosen derived source supports the requested temporal semantics
- ventilation: any overlap with `[0,24h)`
- mortality: death within 28 days after ICU intime
- output grain: one row per selected ICU stay

## Important note

This example documents the expected reasoning pattern. The Skill must still resolve the exact local MIMIC-IV/MIMIC Code sources before presenting a definitive study SQL. It must not invent itemids or assume a derived table exists in every installation.
