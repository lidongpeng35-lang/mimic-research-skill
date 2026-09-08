# MIMIC Research Skill

A reproducibility-oriented MIMIC-IV extraction Skill and plugin package for retrospective clinical research.

It preserves the simple `SKILL.md + references/` interface of lightweight MIMIC skills while adding a semantic registry, versioned research Contract, SQL compiler, controlled Preview, quality checks, provenance, revision-aware approvals, and explicit CSV/XLSX export authorization.

## Design goal

The main risk in MIMIC extraction is often not SQL syntax. It is silently choosing the wrong clinical meaning: an incorrect item/code, MIMIC-III/IV mismatch, wrong analysis unit or time zero, implicit aggregation, unit mixing, or a one-to-many join that changes the cohort. This project makes those choices explicit and reviewable before patient-data execution.

## Current snapshot

- 359 searchable runtime indicator/cohort-filter entries (303 indicators, 56 cohort filters).
- 20 acceptance cases.
- 263 measurement definitions in the research registry; 262 are currently marked `candidate` and 1 is `quarantined`.
- 15-tool MCP workflow covering concept search, Contract compilation/resolution, Preview, QC/state, and controlled export.
- 130 SQL template variants in the bundled compiler snapshot.

A registered or executable definition is not automatically a publication-grade clinical definition. See `docs/DEFINITION_LIFECYCLE.md` for maturity and validation rules.

## Workflow

```text
Research question
  -> concept/provenance resolution
  -> complete versioned Contract
  -> compiler -> SQL + hash
  -> researcher confirmation
  -> controlled Preview
  -> QC / revision loop
  -> exact export authorization
  -> CSV/XLSX + receipt
```

Any material revision invalidates the earlier Preview/export approval.

## Install

OpenClaw skill mode:

```bash
openclaw skills install git:lidongpeng35-lang/mimic-research-skill@main
```

Claude Code local development:

```bash
git clone https://github.com/lidongpeng35-lang/mimic-research-skill.git
cd mimic-research-skill
python3 scripts/bootstrap_catalog.py
python3 scripts/launch_mcp.py --doctor
claude --plugin-dir .
```

Codex / Agent Plugins clients can load the repository as a plugin package. It contains both the portable Agent Plugins 1.0.0 surfaces (`plugin.json`, `skills/`, `mcp.json`) and a Codex-native compatibility surface (`.codex-plugin/plugin.json`) with an inline MCP launcher/environment pass-through.

## Database configuration

Use an authorized PostgreSQL read-only role. Supply connection values through the process environment; never commit credentials:

```bash
export PGHOST=localhost
export PGPORT=5432
export PGDATABASE=mimiciv
export PGUSER=readonly_user
export PGPASSWORD='...'
```

If no compatible database is available, static concept review, Contract design, SQL generation, and offline validation may still be used, but patient counts/rows/Preview/export must not be fabricated.

## Validation

```bash
python3 scripts/validate_repo.py
node runtime/dist/mcp-smoke.js
python3 scripts/launch_mcp.py --doctor
```

The repository validator checks manifests, Skill synchronization, registry/acceptance assets, catalog integrity, GitHub file-size safety, and common accidental-secret patterns. The offline MCP smoke test exercises tool discovery and fail-closed workflow gating without patient data.

## Research reporting

For a manuscript or supplement, archive the non-sensitive extraction specification: cohort and stay-selection rules, analysis unit, index time, windows, source/code/itemid/unit, aggregation and missingness rules, Contract revision/hash, SQL hash, repository version/commit, definition provenance, and QC summary. See `docs/MANUSCRIPT_REPORTING.md`.

## Scope

Primary target: MIMIC-IV core hospital/ICU data. MIMIC-IV-ED, Note, CXR, and ECG are separate optional products. eICU and downstream statistical/causal modeling are outside this repository's extraction scope.

The repository contains no patient data, PhysioNet credentials, or database passwords. MIT applies to this software only and does not alter the MIMIC/PhysioNet data-use agreement.

## Sources and acknowledgements

Primary technical provenance should trace to MIMIC-IV documentation, PhysioNet data descriptions, MIT-LCP MIMIC Code, and the repository's recorded source corpus. The lightweight public presentation was informed by `yongfanbeta/mimic-skill`; its example SQL is not used as this project's execution authority.

See `ACKNOWLEDGEMENTS.md`, `CONTRIBUTING.md`, `SECURITY.md`, `CITATION.cff`, and `CHANGELOG.md`.
