#!/usr/bin/env python3
"""Dependency-free stdio MCP server for the public MIMIC Research Skill.

The server is intentionally fail-closed: concept search and Contract compilation
work offline; patient Preview/Export require an explicitly confirmed revision and
an available read-only PostgreSQL/psql environment.
"""
from __future__ import annotations

import csv
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time
import uuid
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "resources" / "registry.json"
STATE_DIR = Path(os.environ.get("MIMIC_CONTRACT_DIR", Path.home() / ".mimic-research-skill" / "state")).expanduser()
EXPORT_DIR = Path(os.environ.get("MIMIC_EXPORT_DIR", Path.home() / ".mimic-research-skill" / "exports")).expanduser()
EXPORT_PHRASE = "确认导出"


def canonical(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def sha(value: Any) -> str:
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def registry() -> dict[str, Any]:
    return json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))


def concepts() -> list[dict[str, Any]]:
    return registry().get("concepts", [])


def search_concepts(query: str, limit: int = 10) -> list[dict[str, Any]]:
    q = query.casefold().strip()
    scored = []
    for c in concepts():
        blob = " ".join(str(c.get(k, "")) for k in ("id", "label_cn", "label_en", "kind", "source", "column", "unit", "note")).casefold()
        if q in blob:
            score = 0 if q in {str(c.get("id", "")).casefold(), str(c.get("label_cn", "")).casefold(), str(c.get("label_en", "")).casefold()} else 1
            scored.append((score, c))
    scored.sort(key=lambda x: (x[0], str(x[1].get("id"))))
    return [x[1] for x in scored[:limit]]


def state_path(request_id: str) -> Path:
    safe = "".join(ch for ch in request_id if ch.isalnum() or ch in "-_.")
    if not safe or safe != request_id:
        raise ValueError("invalid request_id")
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    return STATE_DIR / f"{safe}.json"


def load_state(request_id: str) -> dict[str, Any]:
    p = state_path(request_id)
    if not p.is_file():
        raise FileNotFoundError(request_id)
    return json.loads(p.read_text(encoding="utf-8"))


def save_state(st: dict[str, Any]) -> None:
    p = state_path(st["request_id"])
    tmp = p.with_suffix(".tmp")
    tmp.write_text(json.dumps(st, ensure_ascii=False, indent=2), encoding="utf-8")
    tmp.replace(p)


def compile_contract(contract: dict[str, Any]) -> dict[str, Any]:
    variables = contract.get("variables") or []
    resolved = []
    unresolved = []
    for v in variables:
        name = v if isinstance(v, str) else v.get("concept") or v.get("id") or v.get("name")
        hits = search_concepts(str(name), 3)
        if len(hits) == 1:
            resolved.append({"request": v, "definition": hits[0]})
        else:
            unresolved.append({"request": v, "candidates": hits})
    frozen = dict(contract)
    frozen["resolved_variables"] = resolved
    frozen["unresolved_variables"] = unresolved
    contract_hash = sha(frozen)
    grain = contract.get("analysis_unit", "stay_id")
    sql_lines = [
        "-- MIMIC Research Skill generated SQL scaffold",
        f"-- contract_sha256: {contract_hash}",
        "-- Review all candidate definitions against the target MIMIC/MIMIC Code version before execution.",
        "WITH cohort AS (",
        "  SELECT i.subject_id, i.hadm_id, i.stay_id, i.intime, i.outtime",
        "  FROM mimiciv_icu.icustays i",
        ")",
        f"SELECT cohort.* FROM cohort ORDER BY {grain};",
    ]
    return {
        "ok": not unresolved,
        "contract": frozen,
        "contract_sha256": contract_hash,
        "sql": "\n".join(sql_lines),
        "sql_sha256": hashlib.sha256("\n".join(sql_lines).encode()).hexdigest(),
        "resolved": resolved,
        "unresolved": unresolved,
        "execution_state": "generated_not_executed",
    }


def db_status() -> dict[str, Any]:
    env_names = ["PGHOST", "PGPORT", "PGDATABASE", "PGUSER"]
    return {
        "psql_available": shutil.which("psql") is not None,
        "configured_environment": {k: bool(os.environ.get(k)) for k in env_names},
        "password_present": bool(os.environ.get("PGPASSWORD")),
        "note": "Password value is never returned.",
    }


def tool_defs() -> list[dict[str, Any]]:
    obj = {"type": "object", "additionalProperties": False, "properties": {}}
    def t(name: str, desc: str, props: dict[str, Any] | None = None, required: list[str] | None = None):
        schema = {"type":"object","additionalProperties":False,"properties":props or {}}
        if required: schema["required"] = required
        return {"name":name,"description":desc,"inputSchema":schema}
    return [
        t("mimic_system_status", "Check registry/state/export/database readiness."),
        t("mimic_v2_search", "Search registered MIMIC concepts.", {"query":{"type":"string"},"limit":{"type":"integer","minimum":1,"maximum":50}}, ["query"]),
        t("mimic_v2_compile", "Compile a complete research Contract into an auditable SQL scaffold.", {"contract":{"type":"object"}}, ["contract"]),
        t("mimic_start_resolution", "Create a versioned research request.", {"prompt":{"type":"string"},"contract":{"type":"object"},"idempotency_key":{"type":"string"}}, ["prompt","contract"]),
        t("mimic_continue_resolution", "Confirm or revise a research request.", {"request_id":{"type":"string"},"action":{"type":"string","enum":["confirm","revise"]},"contract":{"type":"object"}}, ["request_id","action"]),
        t("mimic_run_preview", "Run controlled Preview for the confirmed current revision.", {"request_id":{"type":"string"},"limit":{"type":"integer","minimum":1,"maximum":1000}}, ["request_id"]),
        t("mimic_export", "Export the current preview after exact authorization phrase.", {"request_id":{"type":"string"},"authorization":{"type":"string"},"format":{"type":"string","enum":["csv"]}}, ["request_id","authorization"]),
        t("mimic_status", "Read request status.", {"request_id":{"type":"string"}}, ["request_id"]),
        t("mimic_inspect", "Inspect the frozen Contract/SQL hashes without patient data.", {"request_id":{"type":"string"}}, ["request_id"]),
        t("mimic_retry", "Clear a failed preview and return to confirmed state.", {"request_id":{"type":"string"}}, ["request_id"]),
        t("mimic_cancel", "Cancel a request.", {"request_id":{"type":"string"}}, ["request_id"]),
        t("mimic_list_requests", "List local request metadata."),
        t("mimic_validate_contract", "Validate semantic completeness of a proposed Contract.", {"contract":{"type":"object"}}, ["contract"]),
        t("mimic_get_provenance", "Return registry provenance for a concept.", {"concept":{"type":"string"}}, ["concept"]),
        t("mimic_get_flowchart", "Return the workflow state machine."),
    ]


def validate_contract(contract: dict[str, Any]) -> dict[str, Any]:
    recommended = ["population", "analysis_unit", "index_time", "variables", "output_grain"]
    missing = [x for x in recommended if not contract.get(x)]
    return {"valid_for_compilation": bool(contract.get("variables")), "missing_recommended_fields": missing, "rule": "Material ambiguities must be resolved before patient execution."}


def call_tool(name: str, a: dict[str, Any]) -> dict[str, Any]:
    if name == "mimic_system_status":
        return {"ok": True, "registry": {"path": str(REGISTRY_PATH), "concept_count": len(concepts())}, "database": db_status(), "state_dir": str(STATE_DIR), "export_dir": str(EXPORT_DIR)}
    if name == "mimic_v2_search":
        hits = search_concepts(a["query"], int(a.get("limit", 10)))
        return {"ok": True, "query": a["query"], "count": len(hits), "candidates": hits, "warning": "Registry matches are candidates; validate study-specific semantics and version."}
    if name == "mimic_v2_compile":
        return compile_contract(a["contract"])
    if name == "mimic_validate_contract":
        return validate_contract(a["contract"])
    if name == "mimic_get_provenance":
        hits = search_concepts(a["concept"], 10)
        return {"ok": bool(hits), "concept": a["concept"], "definitions": hits}
    if name == "mimic_get_flowchart":
        return {"ok": True, "states": ["draft","confirmation_required","confirmed","previewed","exported","failed","cancelled"], "flow": "draft -> confirmation_required -> confirmed -> previewed -> exported; revision invalidates preview/export approval"}
    if name == "mimic_start_resolution":
        compiled = compile_contract(a["contract"])
        rid = a.get("idempotency_key") or str(uuid.uuid4())
        try:
            old = load_state(rid)
            return {"ok": True, "idempotent": True, "request": old}
        except FileNotFoundError:
            pass
        st = {"request_id":rid,"revision":1,"prompt":a["prompt"],"contract":compiled["contract"],"contract_sha256":compiled["contract_sha256"],"sql":compiled["sql"],"sql_sha256":compiled["sql_sha256"],"state":"confirmation_required","preview":None,"created_at":time.time()}
        save_state(st)
        return {"ok": True, "outcome":"confirmation_required", "request": st}
    if name in {"mimic_status","mimic_inspect"}:
        st = load_state(a["request_id"])
        if name == "mimic_inspect":
            st = {k:st.get(k) for k in ("request_id","revision","state","contract","contract_sha256","sql","sql_sha256")}
        return {"ok": True, "request": st}
    if name == "mimic_list_requests":
        STATE_DIR.mkdir(parents=True, exist_ok=True)
        out=[]
        for p in sorted(STATE_DIR.glob("*.json")):
            try:
                st=json.loads(p.read_text()); out.append({k:st.get(k) for k in ("request_id","revision","state","contract_sha256","sql_sha256")})
            except Exception: pass
        return {"ok":True,"requests":out}
    if name == "mimic_continue_resolution":
        st=load_state(a["request_id"])
        if a["action"] == "confirm":
            if st["state"] != "confirmation_required": return {"ok":False,"error":"confirmation_not_allowed_in_current_state","state":st["state"]}
            st["state"]="confirmed"; save_state(st); return {"ok":True,"outcome":"contract_ready","request":st}
        new_contract=a.get("contract")
        if not new_contract: return {"ok":False,"error":"revised_contract_required"}
        compiled=compile_contract(new_contract); st.update({"revision":int(st["revision"])+1,"contract":compiled["contract"],"contract_sha256":compiled["contract_sha256"],"sql":compiled["sql"],"sql_sha256":compiled["sql_sha256"],"state":"confirmation_required","preview":None}); save_state(st)
        return {"ok":True,"outcome":"confirmation_required","request":st}
    if name == "mimic_run_preview":
        st=load_state(a["request_id"])
        if st["state"] != "confirmed": return {"ok":False,"error":"preview_requires_confirmed_current_revision","state":st["state"]}
        status=db_status()
        if not status["psql_available"] or not all(status["configured_environment"].values()):
            st["state"]="failed"; st["last_error"]="database_or_psql_unavailable"; save_state(st)
            return {"ok":False,"error":"database_or_psql_unavailable","database":status,"note":"Fail closed; no patient data were read."}
        return {"ok":False,"error":"executor_not_enabled_in_public_scaffold","note":"Generated SQL is available via mimic_inspect. Enable a reviewed read-only executor before patient-data execution."}
    if name == "mimic_retry":
        st=load_state(a["request_id"])
        if st["state"]!="failed": return {"ok":False,"error":"retry_requires_failed_state"}
        st["state"]="confirmed"; st.pop("last_error",None); save_state(st); return {"ok":True,"request":st}
    if name == "mimic_cancel":
        st=load_state(a["request_id"]); st["state"]="cancelled"; save_state(st); return {"ok":True,"request":st}
    if name == "mimic_export":
        st=load_state(a["request_id"])
        if a["authorization"] != EXPORT_PHRASE: return {"ok":False,"error":"exact_export_authorization_required","required_phrase":EXPORT_PHRASE}
        if st["state"] != "previewed" or not st.get("preview"): return {"ok":False,"error":"current_revision_has_no_successful_preview"}
        EXPORT_DIR.mkdir(parents=True, exist_ok=True); out=EXPORT_DIR/f"{st['request_id']}-r{st['revision']}.csv"
        rows=st["preview"].get("rows",[])
        with out.open("w",newline="",encoding="utf-8") as f:
            if rows:
                w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
        st["state"]="exported"; st["export_path"]=str(out); save_state(st)
        return {"ok":True,"receipt":{"path":str(out),"revision":st["revision"],"contract_sha256":st["contract_sha256"],"sql_sha256":st["sql_sha256"]}}
    return {"ok": False, "error": "unknown_tool"}


def emit(obj: dict[str, Any]) -> None:
    sys.stdout.write(json.dumps(obj, ensure_ascii=False) + "\n"); sys.stdout.flush()


def main() -> int:
    for line in sys.stdin:
        try:
            msg=json.loads(line); mid=msg.get("id"); method=msg.get("method"); params=msg.get("params") or {}
            if method == "initialize":
                emit({"jsonrpc":"2.0","id":mid,"result":{"protocolVersion":params.get("protocolVersion","2025-06-18"),"capabilities":{"tools":{}},"serverInfo":{"name":"mimic-research-skill","version":"0.1.0"}}})
            elif method == "notifications/initialized":
                continue
            elif method == "tools/list":
                emit({"jsonrpc":"2.0","id":mid,"result":{"tools":tool_defs()}})
            elif method == "tools/call":
                name=params.get("name"); args=params.get("arguments") or {}
                result=call_tool(name,args)
                emit({"jsonrpc":"2.0","id":mid,"result":{"content":[{"type":"text","text":json.dumps(result,ensure_ascii=False)}],"structuredContent":result,"isError":not result.get("ok",False)}})
            elif mid is not None:
                emit({"jsonrpc":"2.0","id":mid,"error":{"code":-32601,"message":"Method not found"}})
        except Exception as exc:
            if isinstance(locals().get("msg"),dict) and locals()["msg"].get("id") is not None:
                emit({"jsonrpc":"2.0","id":locals()["msg"].get("id"),"error":{"code":-32603,"message":str(exc)}})
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
