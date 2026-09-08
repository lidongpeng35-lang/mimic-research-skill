# Python usage

Keep clinical-definition logic in SQL/Contract rather than reimplementing it differently in Python. Python should be a parameterized read-only wrapper around the reviewed SQL.

Use credentials from environment variables or a secure connection manager. Prefer a dedicated read-only database role, statement timeout, and server-side/limited fetch for Preview. Never commit credentials or patient-derived exports.

Example skeleton:

```python
import os
import psycopg

with psycopg.connect(
    host=os.environ['PGHOST'], port=os.environ.get('PGPORT','5432'),
    dbname=os.environ['PGDATABASE'], user=os.environ['PGUSER'],
    password=os.environ.get('PGPASSWORD')
) as conn:
    conn.execute('SET TRANSACTION READ ONLY')
    with conn.cursor() as cur:
        cur.execute(SQL, params)
        rows = cur.fetchmany(100)
```

Do not use Python-side filtering to silently change cohort, time-window, unit, or aggregation semantics after the SQL hash has been frozen.
