#!/usr/bin/env python3
from __future__ import annotations
import json, subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REQUIRED=[
  'README.md','README_EN.md','SKILL.md','LICENSE','CITATION.cff','plugin.json','mcp.json',
  '.claude-plugin/plugin.json','.codex-plugin/plugin.json','skills/mimic-research/SKILL.md',
  'resources/registry.json','runtime/mcp_server.py','scripts/launch_mcp.py',
  'references/schema.md','references/vital_signs.md','references/labs.md','references/diagnoses.md','references/common_queries.md',
  'references/medications.md','references/procedures.md','references/scores.md','references/outcomes.md','references/cohort_design.md',
  'references/quality_control.md','references/provenance.md','references/python_usage.md','references/runtime.md','references/security.md'
]
def fail(msg): print('ERROR:',msg,file=sys.stderr); raise SystemExit(1)
missing=[x for x in REQUIRED if not (ROOT/x).is_file()]
if missing: fail('missing: '+', '.join(missing))
for p in ['plugin.json','mcp.json','.claude-plugin/plugin.json','.codex-plugin/plugin.json','resources/registry.json']:
    json.loads((ROOT/p).read_text(encoding='utf-8'))
reg=json.loads((ROOT/'resources/registry.json').read_text(encoding='utf-8'))
if len(reg.get('concepts',[])) < 20: fail('starter registry unexpectedly small')
proc=subprocess.Popen([sys.executable,str(ROOT/'runtime/mcp_server.py')],stdin=subprocess.PIPE,stdout=subprocess.PIPE,text=True)
msgs=[
 {'jsonrpc':'2.0','id':1,'method':'initialize','params':{'protocolVersion':'2025-06-18','capabilities':{},'clientInfo':{'name':'ci','version':'1'}}},
 {'jsonrpc':'2.0','method':'notifications/initialized','params':{}},
 {'jsonrpc':'2.0','id':2,'method':'tools/list','params':{}}
]
for m in msgs: proc.stdin.write(json.dumps(m)+'\n'); proc.stdin.flush()
r1=json.loads(proc.stdout.readline()); r2=json.loads(proc.stdout.readline()); proc.terminate()
if r1.get('result',{}).get('serverInfo',{}).get('name')!='mimic-research-skill': fail('MCP initialize failed')
tools=r2.get('result',{}).get('tools',[])
if len(tools)!=15: fail(f'expected 15 tools, got {len(tools)}')
for t in tools:
    if t.get('inputSchema',{}).get('additionalProperties') is not False: fail('tool schema must fail closed on undeclared fields: '+t.get('name','?'))
print(f"OK: release-ready scaffold; concepts={len(reg['concepts'])}; tools={len(tools)}")
