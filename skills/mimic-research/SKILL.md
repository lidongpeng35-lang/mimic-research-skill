---
name: mimic-research-skill
description: Evidence-backed MIMIC-IV cohort and clinical-variable extraction for ICU research. Use for MIMIC-IV cohort definitions, variable/code/itemid resolution, reproducible SQL, time-windowed extraction, QC, preview, and controlled export. Do not use for eICU or unrestricted patient-data queries.
---

# MIMIC-IV Research Data Extraction Skill

Use the repository root `SKILL.md` as the canonical workflow specification. Resolve concepts before SQL, preserve the complete research Contract, treat unresolved definitions explicitly, use read-only/fail-closed execution, invalidate old approvals after revision, and require the exact phrase `确认导出` after a successful current-revision Preview before final export.

Reference material is under `../../references/`; the executable starter registry is `../../resources/registry.json`; the MCP launcher is `../../scripts/launch_mcp.py`.
