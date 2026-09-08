# MCP runtime

The repository exposes a stdio MCP server through `scripts/launch_mcp.py`. The public runtime provides 15 tools for status, concept search, Contract compilation/resolution, state inspection, validation/provenance, Preview gating, retry/cancel, workflow documentation, and controlled export.

Core state flow:

`draft -> confirmation_required -> confirmed -> previewed -> exported`

A material revision increments the revision and invalidates prior Preview/export approval. Failed execution is a separate state and may be retried only after the failure is inspected.

Patient execution is fail-closed. Offline concept search/Contract compilation may run without a database; patient rows/counts must never be fabricated. The public starter runtime does not enable unrestricted SQL execution: a reviewed read-only executor must be configured before real Preview is permitted.

Run `python3 scripts/launch_mcp.py --doctor` to inspect local readiness without exposing password values.
