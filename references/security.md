# Security and data governance

Operate against an authorized local/institutional MIMIC installation with a dedicated PostgreSQL read-only role. Credentials belong in process environment variables or a secure secret manager, never in repository files, prompts, logs, issues, or exported artifacts.

The runtime must reject non-read-only/unreviewed patient execution, use timeouts and Preview row limits, and separate Preview from final export authorization. Final export requires the exact phrase `确认导出` after a successful current-revision Preview.

Do not commit patient-level MIMIC data. Keep exported CSV/XLSX/Parquet and workflow state outside the repository. Public issues and pull requests must contain synthetic examples only.

MIMIC access and data use remain governed by PhysioNet/MIMIC agreements; the repository's MIT software license does not grant data access rights.
