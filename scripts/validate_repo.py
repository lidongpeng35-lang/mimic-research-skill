#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED = [
    "README.md",
    "README_EN.md",
    "SKILL.md",
    "LICENSE",
    "CITATION.cff",
    "plugin.json",
    ".claude-plugin/plugin.json",
    ".codex-plugin/plugin.json",
    "skills/mimic-research/SKILL.md",
    "resources/core-registry.json",
    "resources/acceptance-cases.json",
    "references/schema.md",
    "references/vital_signs.md",
    "references/labs.md",
    "references/diagnoses.md",
    "references/common_queries.md",
    "references/medications.md",
    "references/procedures.md",
    "references/scores.md",
    "references/outcomes.md",
    "references/cohort_design.md",
    "references/quality_control.md",
    "references/provenance.md",
    "docs/ARCHITECTURE.md",
]

FORBIDDEN = [
    "mcp.json",
    "runtime/mcp_server.py",
    "scripts/launch_mcp.py",
]


def fail(message: str) -> None:
    raise SystemExit(f"ERROR: {message}")


missing = [p for p in REQUIRED if not (ROOT / p).is_file()]
if missing:
    fail("missing required files: " + ", ".join(missing))

present_forbidden = [p for p in FORBIDDEN if (ROOT / p).exists()]
if present_forbidden:
    fail("pure Skill must not contain MCP/runtime execution files: " + ", ".join(present_forbidden))

for path in ["plugin.json", ".claude-plugin/plugin.json", ".codex-plugin/plugin.json", "resources/core-registry.json", "resources/acceptance-cases.json"]:
    json.loads((ROOT / path).read_text(encoding="utf-8"))

registry = json.loads((ROOT / "resources/core-registry.json").read_text(encoding="utf-8"))
concepts = registry.get("concepts", [])
if len(concepts) < 30:
    fail(f"core registry unexpectedly small: {len(concepts)}")

cases = json.loads((ROOT / "resources/acceptance-cases.json").read_text(encoding="utf-8")).get("cases", [])
if len(cases) < 20:
    fail(f"acceptance cases unexpectedly small: {len(cases)}")

root_skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
packaged_skill = (ROOT / "skills/mimic-research/SKILL.md").read_text(encoding="utf-8")
for text, label in [(root_skill, "root SKILL"), (packaged_skill, "packaged SKILL")]:
    if "MIMIC-IV" not in text:
        fail(f"{label} must explicitly target MIMIC-IV")
    if "PostgreSQL SQL" not in text:
        fail(f"{label} must explicitly target PostgreSQL SQL generation")

for token in ["itemid", "ICD", "analysis unit", "time window", "aggregation"]:
    if token.lower() not in root_skill.lower():
        fail(f"root SKILL missing critical rule: {token}")

architecture = (ROOT / "docs/ARCHITECTURE.md").read_text(encoding="utf-8")
if "There is no MCP server" not in architecture:
    fail("architecture must explicitly state MCP is out of scope")

print(f"OK: pure MIMIC-IV SQL-generation Skill; core_concepts={len(concepts)}; acceptance_cases={len(cases)}")
