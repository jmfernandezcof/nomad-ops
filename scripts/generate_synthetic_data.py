#!/usr/bin/env python3
"""Generate and validate the deterministic fictional Asteria dataset."""

from __future__ import annotations

import hashlib
import json
import random
import shutil
import tempfile
from datetime import datetime, timedelta, timezone
from pathlib import Path


SEED = 20260906
VERSION = "1.0.0"
BASE_TIME = datetime(2026, 9, 1, 8, 0, tzinfo=timezone.utc)
ROOT = Path(__file__).resolve().parents[1]
DATA_ROOT = ROOT / "data" / "synthetic"


def iso(value: datetime) -> str:
    return value.isoformat().replace("+00:00", "Z")


def dump(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def build_dataset() -> dict[str, object]:
    rng = random.Random(SEED)

    sites = [
        {"id": "SITE-MAD", "name": "Madrid HQ", "kind": "headquarters", "city": "Madrid"},
        {"id": "SITE-TOL", "name": "Plant 1 — Toledo", "kind": "plant", "city": "Toledo"},
        {"id": "SITE-CR", "name": "Plant 2 — Ciudad Real", "kind": "plant", "city": "Ciudad Real"},
        {"id": "SITE-VLC", "name": "Plant 3 — Valencia", "kind": "plant", "city": "Valencia"},
    ]
    departments = [
        {"id": "DEPT-IT", "name": "Information Technology", "site_ids": [s["id"] for s in sites]},
        {"id": "DEPT-OPS", "name": "Operations", "site_ids": ["SITE-TOL", "SITE-CR", "SITE-VLC"]},
        {"id": "DEPT-FIN", "name": "Finance", "site_ids": ["SITE-MAD"]},
        {"id": "DEPT-HR", "name": "Human Resources", "site_ids": ["SITE-MAD"]},
        {"id": "DEPT-PROC", "name": "Procurement", "site_ids": ["SITE-MAD"]},
        {"id": "DEPT-COMP", "name": "Compliance", "site_ids": ["SITE-MAD"]},
        {"id": "DEPT-WH", "name": "Warehouse and Logistics", "site_ids": ["SITE-CR", "SITE-VLC"]},
        {"id": "DEPT-PKG", "name": "Packaging", "site_ids": ["SITE-TOL", "SITE-CR", "SITE-VLC"]},
    ]

    fixed_users = [
        ("Carlos", "Romero", "plant_operations_manager", "DEPT-OPS", "SITE-CR", ["SITE-CR"]),
        ("Laura", "Martín", "department_manager", "DEPT-FIN", "SITE-MAD", ["SITE-MAD"]),
        ("Daniel", "Ortega", "it_operator", "DEPT-IT", "SITE-MAD", [s["id"] for s in sites]),
        ("Elena", "Santos", "compliance_governance", "DEPT-COMP", "SITE-MAD", [s["id"] for s in sites]),
        ("Miguel", "Navarro", "nomad_ops_admin", "DEPT-IT", "SITE-MAD", ["SITE-MAD"]),
        ("Lucía", "Vega", "employee", "DEPT-PROC", "SITE-MAD", ["SITE-MAD"]),
    ]
    first_names = ["Ana", "Pablo", "Marta", "Javier", "Sara", "Álvaro", "Irene", "Diego", "Nuria"]
    last_names = ["Ruiz", "Moreno", "Gil", "Iglesias", "Molina", "Cano", "Suárez", "Prieto"]
    roles = [
        "employee", "employee", "employee", "it_operator",
        "plant_operations_manager", "department_manager",
        "compliance_governance", "nomad_ops_admin",
    ]
    dept_ids = [d["id"] for d in departments]
    site_ids = [s["id"] for s in sites]
    users = []
    for index in range(60):
        if index < len(fixed_users):
            first, last, role, dept, site, scope = fixed_users[index]
        else:
            first = first_names[index % len(first_names)]
            last = f"{last_names[(index // len(first_names)) % len(last_names)]}-{index + 1:02d}"
            role = roles[index % len(roles)]
            dept = dept_ids[index % len(dept_ids)]
            possible_sites = next(d["site_ids"] for d in departments if d["id"] == dept)
            site = possible_sites[index % len(possible_sites)]
            scope = list(site_ids) if role in {"it_operator", "compliance_governance"} else [site]
        users.append({
            "id": f"USR-{index + 1:03d}",
            "display_name": f"{first} {last}",
            "email": f"user{index + 1:03d}@asteria.example",
            "role": role,
            "department_id": dept,
            "primary_site_id": site,
            "site_scope": scope,
            "classification": "CONFIDENTIAL",
            "synthetic": True,
        })

    asset_types = ["application_server", "network_device", "packaging_line", "warehouse_scanner"]
    assets = []
    for index in range(24):
        site = sites[index % 4]
        assets.append({
            "id": f"AST-{index + 1:03d}",
            "name": f"{asset_types[index % 4].replace('_', ' ').title()} {index + 1:02d}",
            "asset_type": asset_types[index % 4],
            "site_id": site["id"],
            "responsible_department_id": "DEPT-IT" if index % 4 < 2 else "DEPT-OPS",
            "status": "active",
            "classification": "INTERNAL",
        })

    supplier_categories = ["packaging", "raw_materials", "maintenance", "logistics"]
    suppliers = [{
        "id": f"SUP-{i + 1:03d}",
        "name": f"Proveedor Ficticio {i + 1:02d}",
        "category": supplier_categories[i % 4],
        "status": "active" if i != 10 else "under_review",
        "classification": "CONFIDENTIAL",
        "synthetic": True,
    } for i in range(12)]

    documents = []
    for index in range(40):
        family = f"PROC-{(index // 2) + 1:03d}"
        version = 2 if index % 2 == 0 else 1
        current = index % 2 == 0
        dept = dept_ids[(index // 2) % len(dept_ids)]
        allowed_sites = ["SITE-MAD"] if dept in {"DEPT-FIN", "DEPT-HR", "DEPT-PROC", "DEPT-COMP"} else site_ids
        title = "Supplier onboarding procedure" if index < 2 else f"Asteria procedure {(index // 2) + 1:02d}"
        if index < 2:
            dept, allowed_sites = "DEPT-PROC", ["SITE-MAD"]
        if index == 2:
            title, dept, allowed_sites = "IT incident diagnosis runbook", "DEPT-IT", site_ids
        documents.append({
            "id": f"DOC-{index + 1:03d}",
            "family_id": family,
            "title": title,
            "version": version,
            "is_current": current,
            "status": "current" if current else "superseded",
            "department_id": dept,
            "allowed_site_ids": allowed_sites,
            "published_at": iso(BASE_TIME - timedelta(days=200 - index)),
            "classification": "INTERNAL" if dept not in {"DEPT-FIN", "DEPT-HR"} else "CONFIDENTIAL",
            "content": f"Fictional controlled guidance for {title.lower()}, version {version}.",
        })

    alerts = []
    alert_states = ["open", "acknowledged", "resolved"]
    for index in range(80):
        asset = assets[index % len(assets)]
        created = BASE_TIME + timedelta(hours=index * 2)
        alerts.append({
            "id": f"ALT-{index + 1:03d}",
            "asset_id": asset["id"],
            "site_id": asset["site_id"],
            "severity": rng.choice(["low", "medium", "high"]),
            "status": alert_states[index % 3],
            "summary": f"Synthetic {asset['asset_type']} alert {index + 1:03d}",
            "created_at": iso(created),
            "resolved_at": iso(created + timedelta(hours=2)) if index % 3 == 2 else None,
            "classification": "INTERNAL",
        })

    incidents = []
    for index in range(60):
        asset = assets[index % len(assets)]
        opened = BASE_TIME + timedelta(hours=index * 3)
        incidents.append({
            "id": f"INC-{index + 1:03d}",
            "title": f"Synthetic operational incident {index + 1:03d}",
            "site_id": asset["site_id"],
            "asset_id": asset["id"],
            "requester_id": users[(index + 5) % len(users)]["id"],
            "assignee_id": "USR-003",
            "related_alert_ids": [f"ALT-{(index % 80) + 1:03d}"],
            "related_document_ids": ["DOC-003"],
            "previous_incident_id": f"INC-{index:03d}" if index > 0 else "INC-002",
            "status": ["open", "investigating", "resolved"][index % 3],
            "opened_at": iso(opened),
            "classification": "CONFIDENTIAL",
        })
    incidents[0].update({
        "title": "Packaging line telemetry interruption — Ciudad Real",
        "site_id": "SITE-CR",
        "asset_id": "AST-003",
        "requester_id": "USR-001",
        "related_alert_ids": ["ALT-003"],
        "previous_incident_id": "INC-002",
    })

    decisions = ["APPROVED", "REJECTED", "EXPIRED", "APPROVED"]
    outcomes = ["SUCCESS", "NOT_STARTED", "NOT_STARTED", "FAILED", "SUCCESS", "UNKNOWN"]
    approvals = []
    actions = []
    for index in range(12):
        requested = BASE_TIME + timedelta(days=10, hours=index)
        decision = decisions[index % len(decisions)]
        approval_id = f"APR-{index + 1:03d}"
        action_id = f"ACT-{index + 1:03d}"
        approvals.append({
            "id": approval_id,
            "action_id": action_id,
            "requester_id": "USR-003",
            "eligible_approver_id": "USR-001",
            "site_id": "SITE-CR",
            "decision": decision,
            "requested_at": iso(requested),
            "decided_at": iso(requested + timedelta(minutes=20)) if decision in {"APPROVED", "REJECTED"} else None,
            "expires_at": iso(requested + timedelta(hours=1)),
            "classification": "CONFIDENTIAL",
        })
        outcome = outcomes[index % len(outcomes)]
        if decision != "APPROVED":
            outcome = "NOT_STARTED"
        actions.append({
            "id": action_id,
            "approval_id": approval_id,
            "incident_id": "INC-001",
            "action_type": "restart_simulated_service",
            "site_id": "SITE-CR",
            "requested_by": "USR-003",
            "outcome": outcome,
            "executed_at": iso(requested + timedelta(minutes=25)) if outcome != "NOT_STARTED" else None,
            "evidence": f"Synthetic execution evidence for {action_id}" if outcome == "SUCCESS" else None,
            "classification": "CONFIDENTIAL",
        })
    # Ensure the approved journey and the uncertain journey have explicit outcomes.
    approvals[0]["decision"] = "APPROVED"
    actions[0]["outcome"] = "SUCCESS"
    actions[0]["evidence"] = "Simulated service healthy after controlled restart"
    approvals[5]["decision"] = "APPROVED"
    approvals[5]["decided_at"] = iso(BASE_TIME + timedelta(days=10, hours=5, minutes=20))
    actions[5]["outcome"] = "UNKNOWN"
    actions[5]["evidence"] = None

    audit_events = []
    for index, action in enumerate(actions):
        approval = approvals[index]
        for step, event_type in enumerate(["request_received", "authorization_checked", "approval_decided", "execution_recorded"]):
            audit_events.append({
                "id": f"AUD-{index * 4 + step + 1:04d}",
                "request_id": f"REQ-{index + 1:03d}",
                "approval_id": approval["id"],
                "action_id": action["id"],
                "event_type": event_type,
                "occurred_at": iso(BASE_TIME + timedelta(days=10, hours=index, minutes=step * 8)),
                "actor_id": "USR-001" if event_type == "approval_decided" else "USR-003",
                "classification": "CONFIDENTIAL",
            })

    scenarios = [
        {"id": "SD-001", "name": "Authorized procedure search", "records": {"users": ["USR-006"], "documents": ["DOC-001", "DOC-002"]}},
        {"id": "SD-002", "name": "IT incident investigation", "records": {"users": ["USR-003"], "incidents": ["INC-001", "INC-002"], "alerts": ["ALT-003"], "assets": ["AST-003"], "documents": ["DOC-003"]}},
        {"id": "SD-003", "name": "Plant access boundary", "records": {"users": ["USR-001"], "alerts": ["ALT-003", "ALT-004"], "assets": ["AST-003", "AST-004"], "sites": ["SITE-CR", "SITE-VLC"]}},
        {"id": "SD-004", "name": "Controlled action with approval", "records": {"users": ["USR-001", "USR-003"], "incidents": ["INC-001"], "approvals": ["APR-001"], "actions": ["ACT-001"]}},
        {"id": "SD-005", "name": "Compliance review", "records": {"users": ["USR-004"], "approvals": ["APR-001"], "actions": ["ACT-001"], "audit_events": ["AUD-0001", "AUD-0002", "AUD-0003", "AUD-0004"]}},
        {"id": "SD-006", "name": "Uncertain action outcome", "records": {"users": ["USR-003"], "incidents": ["INC-001"], "approvals": ["APR-006"], "actions": ["ACT-006"], "audit_events": ["AUD-0021", "AUD-0022", "AUD-0023", "AUD-0024"]}},
    ]

    return {
        "sites": sites,
        "departments": departments,
        "users": users,
        "assets": assets,
        "suppliers": suppliers,
        "documents": documents,
        "incidents": incidents,
        "alerts": alerts,
        "approvals": approvals,
        "actions": actions,
        "audit_events": audit_events,
        "scenarios": scenarios,
    }


def validate(data: dict[str, object]) -> list[str]:
    errors: list[str] = []
    minimums = {
        "sites": 4, "departments": 8, "users": 60, "assets": 24,
        "suppliers": 12, "documents": 40, "incidents": 60,
        "alerts": 80, "approvals": 12,
    }
    indexes: dict[str, dict[str, dict]] = {}
    for name, records in data.items():
        if name == "scenarios":
            continue
        typed_records = records if isinstance(records, list) else []
        ids = [record["id"] for record in typed_records]
        if len(ids) != len(set(ids)):
            errors.append(f"{name}: duplicate identifiers")
        indexes[name] = {record["id"]: record for record in typed_records}
    for name, minimum in minimums.items():
        if len(indexes[name]) < minimum:
            errors.append(f"{name}: expected at least {minimum}")

    def require(group: str, record_id: str | None, context: str) -> None:
        if not record_id or record_id not in indexes[group]:
            errors.append(f"{context}: missing {group} reference {record_id}")

    for user in indexes["users"].values():
        require("departments", user["department_id"], user["id"])
        require("sites", user["primary_site_id"], user["id"])
        for site_id in user["site_scope"]:
            require("sites", site_id, user["id"])
        if user.get("synthetic") is not True or not user["email"].endswith("@asteria.example"):
            errors.append(f"{user['id']}: synthetic identity marker missing")
    for asset in indexes["assets"].values():
        require("sites", asset["site_id"], asset["id"])
        require("departments", asset["responsible_department_id"], asset["id"])
    for alert in indexes["alerts"].values():
        require("assets", alert["asset_id"], alert["id"])
        require("sites", alert["site_id"], alert["id"])
        asset = indexes["assets"].get(alert["asset_id"])
        if asset and asset["site_id"] != alert["site_id"]:
            errors.append(f"{alert['id']}: asset and alert sites differ")
    for incident in indexes["incidents"].values():
        for group, key in [("sites", "site_id"), ("assets", "asset_id"), ("users", "requester_id"), ("users", "assignee_id")]:
            require(group, incident[key], incident["id"])
        for alert_id in incident["related_alert_ids"]:
            require("alerts", alert_id, incident["id"])
        for document_id in incident["related_document_ids"]:
            require("documents", document_id, incident["id"])
    for approval in indexes["approvals"].values():
        require("actions", approval["action_id"], approval["id"])
        require("users", approval["requester_id"], approval["id"])
        require("users", approval["eligible_approver_id"], approval["id"])
    for action in indexes["actions"].values():
        require("approvals", action["approval_id"], action["id"])
        require("incidents", action["incident_id"], action["id"])
        approval = indexes["approvals"].get(action["approval_id"])
        if action["outcome"] != "NOT_STARTED" and approval and approval["decision"] != "APPROVED":
            errors.append(f"{action['id']}: action started without approval")
        if action["outcome"] == "SUCCESS" and not action["evidence"]:
            errors.append(f"{action['id']}: success has no evidence")

    if not any(a["decision"] == "REJECTED" for a in indexes["approvals"].values()):
        errors.append("approvals: rejected example missing")
    if not any(a["decision"] == "EXPIRED" for a in indexes["approvals"].values()):
        errors.append("approvals: expired example missing")
    for outcome in ["SUCCESS", "FAILED", "UNKNOWN", "NOT_STARTED"]:
        if not any(a["outcome"] == outcome for a in indexes["actions"].values()):
            errors.append(f"actions: {outcome} example missing")

    for scenario in data["scenarios"]:
        for group, record_ids in scenario["records"].items():
            for record_id in record_ids:
                require(group, record_id, scenario["id"])
    if {s["id"] for s in data["scenarios"]} != {f"SD-{i:03d}" for i in range(1, 7)}:
        errors.append("scenarios: approved six-scenario set is incomplete")
    return errors


def fingerprint(data: dict[str, object]) -> str:
    payload = json.dumps(data, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def write_dataset(data: dict[str, object], root: Path) -> None:
    source = root / "source"
    exports = root / "exports"
    scenarios_dir = root / "scenarios"
    for name in [
        "sites", "departments", "users", "assets", "suppliers", "documents",
        "incidents", "alerts", "approvals", "actions", "audit_events",
    ]:
        dump(source / f"{name}.json", data[name])
    export_map = {
        "hr.json": {"users": data["users"], "departments": data["departments"], "sites": data["sites"]},
        "itsm.json": {"incidents": data["incidents"]},
        "monitoring.json": {"alerts": data["alerts"]},
        "erp.json": {"suppliers": data["suppliers"]},
        "documents.json": {"documents": data["documents"]},
        "plant_operations.json": {"assets": data["assets"]},
        "nomad_ops.json": {"approvals": data["approvals"], "actions": data["actions"], "audit_events": data["audit_events"]},
    }
    for filename, records in export_map.items():
        dump(exports / filename, records)
    for scenario in data["scenarios"]:
        dump(scenarios_dir / f"{scenario['id'].lower()}.json", scenario)


def main() -> int:
    data = build_dataset()
    repeat = build_dataset()
    errors = validate(data)
    deterministic = fingerprint(data) == fingerprint(repeat)
    if not deterministic:
        errors.append("generation is not deterministic")

    with tempfile.TemporaryDirectory(prefix="nomad-synthetic-") as temp_dir:
        staging = Path(temp_dir)
        write_dataset(data, staging)
        for directory in ["source", "exports", "scenarios", "reports"]:
            target = DATA_ROOT / directory
            if target.exists():
                shutil.rmtree(target)
            source = staging / directory
            if source.exists():
                shutil.copytree(source, target)
            else:
                target.mkdir(parents=True)

    report = {
        "dataset": "Asteria Manufacturing Group synthetic demonstration data",
        "version": VERSION,
        "seed": SEED,
        "fingerprint_sha256": fingerprint(data),
        "deterministic_regeneration": deterministic,
        "synthetic_data_only": True,
        "record_counts": {name: len(records) for name, records in data.items()},
        "mandatory_checks": "PASSED" if not errors else "FAILED",
        "errors": errors,
    }
    dump(DATA_ROOT / "reports" / "validation-report.json", report)
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
