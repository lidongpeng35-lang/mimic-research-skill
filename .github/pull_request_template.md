## Summary

Describe the change and why it is needed.

## Change type

- [ ] Skill behavior / SQL-generation rules
- [ ] Clinical definition / registry
- [ ] Reference / documentation
- [ ] Acceptance test / CI

## Research-definition checklist

For clinical-definition changes:

- [ ] MIMIC-IV product/schema/table/view recorded
- [ ] code/itemid/column and version recorded
- [ ] unit/specimen/method documented where relevant
- [ ] time semantics and aggregation documented
- [ ] provenance supplied
- [ ] acceptance/regression case supplied
- [ ] candidate/quarantined maturity status preserved

## Safety and scope

- [ ] no credentials
- [ ] no patient-level MIMIC data or exports
- [ ] no database executor or MCP runtime introduced
- [ ] generated SQL remains read-only

## Validation

```bash
python3 scripts/validate_repo.py
```
