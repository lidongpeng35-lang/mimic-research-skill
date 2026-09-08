# Architecture

The public v0.1 package is intentionally small and auditable.

```text
SKILL.md / references/
        ↓
resources/registry.json
        ↓
runtime/mcp_server.py
        ↓
versioned Contract + hashes
        ↓
confirmation / revision state
        ↓
reviewed read-only Preview executor (not enabled by default)
        ↓
QC → exact export authorization
```

The Skill layer defines research semantics. The registry stores candidate concept mappings. The MCP runtime handles discovery, compilation, state transitions and fail-closed gates. Patient execution is deliberately a separate security boundary: the public scaffold will not turn arbitrary generated SQL into unrestricted database reads.

A future full registry/compiler release may replace or extend the starter registry while preserving the same Contract, provenance, revision and export-gating principles.
