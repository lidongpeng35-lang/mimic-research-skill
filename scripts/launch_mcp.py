#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, os, shutil, subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SERVER=ROOT/"runtime"/"mcp_server.py"

def doctor():
    reg=ROOT/"resources"/"registry.json"
    concepts=0
    if reg.is_file():
        concepts=len(json.loads(reg.read_text(encoding="utf-8")).get("concepts",[]))
    report={
        "server": SERVER.is_file(),
        "registry": reg.is_file(),
        "registry_concepts": concepts,
        "python": sys.version.split()[0],
        "psql": bool(shutil.which("psql")),
        "database_env": {k:bool(os.environ.get(k)) for k in ("PGHOST","PGPORT","PGDATABASE","PGUSER")},
        "note":"Patient execution remains fail-closed unless a reviewed read-only executor is enabled."
    }
    print(json.dumps(report,ensure_ascii=False,indent=2)); return 0 if report["server"] and report["registry"] else 1

def main():
    p=argparse.ArgumentParser();p.add_argument("--doctor",action="store_true");a=p.parse_args()
    if a.doctor:return doctor()
    os.execv(sys.executable,[sys.executable,str(SERVER)])
if __name__=="__main__":raise SystemExit(main())
