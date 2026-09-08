## Summary

Describe the change and why it is needed.

## Change type

- [ ] Runtime / tooling
- [ ] Clinical definition / registry
- [ ] Reference / documentation
- [ ] Test / CI

## Research-definition checklist

For clinical-definition changes:

- [ ] source product/schema/table/view recorded
- [ ] code/itemid/column and version recorded
- [ ] unit/specimen/method documented where relevant
- [ ] time semantics and aggregation documented
- [ ] provenance supplied
- [ ] validation/regression case supplied

## Safety

- [ ] no credentials
- [ ] no patient-level MIMIC data or exports
- [ ] fail-closed behavior preserved

## Validation

```bash
python3 scripts/validate_repo.py
python3 scripts/launch_mcp.py --doctor
```
