# Changelog

## 0.2.0 - 2026-09-08

- Refocused the repository as a pure MIMIC-IV data-extraction SQL-generation Skill.
- Removed MCP configuration, MCP server, database execution, Preview/export workflow, and runtime state machinery.
- Rewrote `SKILL.md` around natural-language request parsing, definition resolution, extraction specification, complete PostgreSQL SQL generation, and static quality review.
- Added a curated high-frequency `resources/core-registry.json` and 20 natural-language acceptance cases.
- Updated Claude/Codex manifests, architecture, validation, roadmap, examples, CI, and contribution templates to match the SQL-only scope.
- CI now validates that MCP/runtime execution surfaces are absent.

## 0.1.0 - 2026-09-08

- Initial public scaffold. This release included an MCP/runtime direction that was removed in 0.2.0 after narrowing the project scope to a pure data-extraction Skill.
