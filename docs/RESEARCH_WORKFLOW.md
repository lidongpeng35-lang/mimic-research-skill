# Research workflow

1. Provide the study question in natural language.
2. The Skill identifies population, analysis unit, stay selection, index time, variables, windows, aggregation and output grain.
3. Definitions are resolved from repository resources and MIMIC-IV references.
4. Material ambiguities are surfaced before a definitive SQL is presented.
5. The Skill generates complete PostgreSQL SQL.
6. A static quality pass checks row grain, joins, time windows, aggregation, units/specimens and schema version.
7. The researcher reviews the SQL and executes it in an authorized MIMIC-IV environment.

The repository never claims that generated SQL has been run against patient data.
