# MIMIC Research Skill

[![CI](https://github.com/lidongpeng35-lang/mimic-research-skill/actions/workflows/ci.yml/badge.svg)](https://github.com/lidongpeng35-lang/mimic-research-skill/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![MIMIC-IV](https://img.shields.io/badge/Data-MIMIC--IV-informational.svg)](https://mimic.mit.edu/docs/IV/)

A reproducibility-oriented MIMIC-IV data-extraction Skill / Agent Plugin / Codex Plugin / Claude Code Plugin for retrospective clinical research.

The project keeps the lightweight `SKILL.md + references/` experience, but makes the research workflow explicit: **concept resolution → versioned research Contract → SQL/provenance → confirmation → Preview/QC → controlled export**.

> The goal is not merely to generate SQL that runs. Cohort definitions, analysis unit, time zero, windows, variables, aggregation, units, missingness and output grain should be auditable and reproducible.

## Why this project

High-risk MIMIC errors are often semantic rather than syntactic: incorrect itemids or ICD codes, MIMIC-III/IV mixing, wrong analysis unit or time zero, implicit first/max/mean choices, unit/specimen mixing, or one-to-many joins that silently change the cohort.

This repository therefore follows several rules:

- do not invent itemids, ICD codes, tables, units or score formulas from model memory;
- define research semantics before generating SQL;
- preserve raw events when aggregation is not specified;
- a dictionary match is not equivalent to a clinically validated definition;
- Preview and Export are separate gates;
- a material revision invalidates earlier Preview/export approval;
- without an authorized database, fail closed rather than fabricate patient rows, counts, missingness or export receipts.

## Public v0.1 capabilities

| Capability | Status |
|---|---|
| MIMIC-IV schema / vital / lab / diagnosis references | ✅ |
| medication / procedure / score / outcome references | ✅ |
| cohort design / QC / provenance / security guidance | ✅ |
| auditable starter semantic registry | ✅ |
| research request → versioned Contract | ✅ |
| Contract and SQL SHA-256 hashes | ✅ |
| 15-tool stdio MCP server | ✅ |
| confirmation / revision state machine | ✅ |
| Preview / Export fail-closed gates | ✅ |
| exact `确认导出` export authorization rule | ✅ |
| unrestricted patient SQL execution | ❌ intentionally disabled |
| publication-grade certification of every definition | ❌ study-specific validation required |
| eICU | ❌ out of scope |

`resources/registry.json` is a public starter registry. Definitions are marked as candidates by default. Registered/executable does not mean publication-validated.

## Workflow

```text
Research question
  -> concept/provenance resolution
  -> complete versioned Contract
  -> SQL scaffold + Contract hash + SQL hash
  -> researcher confirmation
  -> controlled Preview (only with a reviewed read-only executor)
  -> QC / revision loop
  -> exact export authorization: 确认导出
  -> CSV + receipt
```

## Install

OpenClaw / skill mode:

```bash
openclaw skills install git:lidongpeng35-lang/mimic-research-skill@main
```

Claude Code local development:

```bash
git clone https://github.com/lidongpeng35-lang/mimic-research-skill.git
cd mimic-research-skill
python3 scripts/launch_mcp.py --doctor
claude --plugin-dir .
```

Codex / Agent Plugins clients can load the repository package. It contains:

- `plugin.json` — portable plugin manifest
- `mcp.json` — portable MCP config
- `.codex-plugin/plugin.json` — Codex compatibility surface
- `.claude-plugin/plugin.json` — Claude Code manifest
- `skills/mimic-research/SKILL.md` — packaged Agent Skill

## Database safety

Real patient Preview must use an authorized MIMIC installation and a dedicated read-only PostgreSQL role. Supply credentials only through environment variables or a secure secret manager:

```bash
export PGHOST=localhost
export PGPORT=5432
export PGDATABASE=mimiciv
export PGUSER=readonly_user
export PGPASSWORD='...'
```

Check local readiness with:

```bash
python3 scripts/launch_mcp.py --doctor
```

The public scaffold deliberately does not enable unrestricted patient execution. If a reviewed read-only executor is unavailable, `mimic_run_preview` fails closed.

## MCP tools

The runtime exposes 15 tools:

`mimic_system_status`, `mimic_v2_search`, `mimic_v2_compile`, `mimic_start_resolution`, `mimic_continue_resolution`, `mimic_run_preview`, `mimic_export`, `mimic_status`, `mimic_inspect`, `mimic_retry`, `mimic_cancel`, `mimic_list_requests`, `mimic_validate_contract`, `mimic_get_provenance`, and `mimic_get_flowchart`.

Tool schemas reject undeclared fields.

## References

The same core entry points present in lightweight MIMIC skills are retained:

- `references/schema.md`
- `references/vital_signs.md`
- `references/labs.md`
- `references/diagnoses.md`
- `references/common_queries.md`

Additional references cover medications, procedures, severity scores, outcomes, cohort design, quality control, provenance, Python usage, runtime behavior, and security.

## Validation

```bash
python3 scripts/validate_repo.py
python3 scripts/launch_mcp.py --doctor
```

GitHub Actions validates repository structure, JSON manifests, the starter registry, MCP initialization, discovery of exactly 15 tools, and fail-closed tool schemas.

## Research reporting

For a manuscript or supplement, preserve the non-sensitive extraction specification: cohort rules and stepwise counts, analysis unit, ICU/stay selection, index time, time windows, source/code/itemid/unit/specimen, aggregation and missingness rules, Contract revision/hash, SQL hash, repository release/commit, definition provenance, and QC summary.

## Scope and data governance

MIMIC-IV core and MIMIC-IV-ED / Note / CXR / ECG are separate products and are not assumed to all be installed. MIMIC timestamps are deidentified/shifted and should not be interpreted as real patient calendar dates or timezone. MIMIC-IV ICU stays use `stay_id`, not the MIMIC-III `icustay_id` convention.

The repository contains no patient data, PhysioNet credentials or database passwords. The MIT License applies to this software only and does not alter PhysioNet/MIMIC data-use agreements.

## Sources and acknowledgements

Primary technical provenance should trace to MIMIC-IV documentation, PhysioNet MIMIC-IV descriptions, MIT-LCP MIMIC Code and the source records stored with each project definition.

The lightweight public presentation was informed by `yongfanbeta/mimic-skill`; its example SQL is not used as this project's clinical-definition or execution authority. See `ACKNOWLEDGEMENTS.md`.

See also `CONTRIBUTING.md`, `SECURITY.md`, `CITATION.cff`, and `CHANGELOG.md`.
