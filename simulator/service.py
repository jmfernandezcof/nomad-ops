"""Application core for the approved Asteria enterprise-system simulator."""

from __future__ import annotations

import json
from copy import deepcopy
from datetime import datetime
from pathlib import Path
from typing import Any


OUTCOMES = {
    "SUCCESS", "FAILED", "UNKNOWN", "DENIED", "NOT_FOUND",
    "INVALID_REQUEST", "UNAVAILABLE", "PARTIAL",
}
READ_OPERATIONS = {
    "itsm.get_incident", "itsm.search_incidents", "itsm.get_incident_history",
    "documents.search_documents", "documents.get_document", "documents.get_current_document",
    "hr.get_user_context", "hr.get_department", "hr.confirm_employee_active",
    "erp.get_supplier", "erp.get_supplier_status", "erp.search_suppliers",
    "plant.get_asset", "plant.get_asset_state", "plant.list_assets",
    "monitoring.get_alert", "monitoring.list_alerts", "monitoring.get_service_health",
}
WRITE_OPERATIONS = {
    "itsm.add_incident_note", "itsm.escalate_incident",
    "operations.restart_simulated_service",
}
KNOWN_OPERATIONS = READ_OPERATIONS | WRITE_OPERATIONS


class SimulationService:
    """In-process boundary for the six simulated Asteria modules.

    A future transport adapter may expose this class without moving policy into
    that adapter. Tests call the same boundary directly.
    """

    def __init__(
        self,
        data_root: Path | None = None,
        failure_profiles: dict[str, str] | None = None,
    ) -> None:
        root = data_root or Path(__file__).resolve().parents[1] / "data" / "synthetic" / "exports"
        self._data = self._load(root)
        self._failures = failure_profiles or {}
        self._idempotent_results: dict[str, dict[str, Any]] = {}
        self.trace: list[dict[str, Any]] = []
        self.incident_notes: dict[str, list[str]] = {}
        self.escalated_incidents: set[str] = set()

    @staticmethod
    def _load(root: Path) -> dict[str, list[dict[str, Any]]]:
        filenames = [
            "hr.json", "itsm.json", "monitoring.json", "erp.json",
            "documents.json", "plant_operations.json", "nomad_ops.json",
        ]
        combined: dict[str, list[dict[str, Any]]] = {}
        for filename in filenames:
            path = root / filename
            if not path.is_file():
                raise FileNotFoundError(f"Required synthetic export missing: {path}")
            content = json.loads(path.read_text(encoding="utf-8"))
            for group, records in content.items():
                combined[group] = records
        return combined

    def call(self, request: dict[str, Any]) -> dict[str, Any]:
        request_id = request.get("request_id")
        operation = request.get("operation")
        actor_id = request.get("actor_id")
        if not request_id or not operation or not actor_id or request.get("caller_service_id") != "nomad-ops-svc":
            return self._respond(request, "INVALID_REQUEST", error="required_context_missing")
        if operation not in KNOWN_OPERATIONS:
            return self._respond(request, "INVALID_REQUEST", error="unknown_operation")

        actor = self._find("users", actor_id)
        if not actor:
            return self._respond(request, "DENIED", error="unknown_actor")
        actor_context = request.get("actor_context")
        expected_context = {
            "role": actor["role"],
            "department_id": actor["department_id"],
            "site_scope": actor["site_scope"],
        }
        if actor_context != expected_context:
            return self._respond(request, "DENIED", error="actor_context_mismatch")
        if operation in WRITE_OPERATIONS:
            key = request.get("idempotency_key")
            if not isinstance(key, str) or not key:
                return self._respond(request, "INVALID_REQUEST", error="idempotency_key_required")
            if key in self._idempotent_results:
                cached = deepcopy(self._idempotent_results[key])
                return self._respond(request, cached["outcome"], cached["data"], cached["error"])

        failure = self._failures.get(operation)
        if failure:
            mapped = {
                "unavailable": "UNAVAILABLE",
                "timeout_read": "FAILED",
                "timeout_write": "UNKNOWN",
                "partial": "PARTIAL",
                "rate_limit": "UNAVAILABLE",
                "contract_error": "FAILED",
            }.get(failure, "FAILED")
            return self._respond(request, mapped, error=failure)

        handler_name = "_" + operation.replace(".", "_")
        response = getattr(self, handler_name)(request, actor)
        if response["outcome"] not in OUTCOMES:
            raise RuntimeError("Simulator produced an invalid outcome")
        if operation in WRITE_OPERATIONS:
            self._idempotent_results[request["idempotency_key"]] = {
                "outcome": response["outcome"],
                "data": deepcopy(response["data"]),
                "error": response["error"],
            }
        return response

    def _respond(
        self,
        request: dict[str, Any],
        outcome: str,
        data: Any = None,
        error: str | None = None,
    ) -> dict[str, Any]:
        operation = request.get("operation", "unknown")
        response = {
            "request_id": request.get("request_id"),
            "source_system": operation.split(".", 1)[0],
            "operation": operation,
            "outcome": outcome,
            "simulated_time": "2026-09-06T12:00:00Z",
            "completeness": "uncertain" if outcome == "UNKNOWN" else ("partial" if outcome == "PARTIAL" else "complete"),
            "data": deepcopy(data),
            "error": error,
        }
        self.trace.append({
            "request_id": response["request_id"],
            "actor_id": request.get("actor_id"),
            "operation": operation,
            "outcome": outcome,
        })
        return response

    def _find(self, group: str, record_id: str | None) -> dict[str, Any] | None:
        return next((item for item in self._data[group] if item["id"] == record_id), None)

    @staticmethod
    def _site_allowed(actor: dict[str, Any], site_id: str) -> bool:
        return site_id in actor["site_scope"]

    def _incident_allowed(self, actor: dict[str, Any], incident: dict[str, Any]) -> bool:
        return actor["role"] in {"it_operator", "plant_operations_manager"} and self._site_allowed(actor, incident["site_id"])

    def _document_allowed(self, actor: dict[str, Any], document: dict[str, Any]) -> bool:
        return actor["department_id"] == document["department_id"] and any(
            site in actor["site_scope"] for site in document["allowed_site_ids"]
        )

    def _asset_allowed(self, actor: dict[str, Any], asset: dict[str, Any]) -> bool:
        return actor["role"] in {"it_operator", "plant_operations_manager"} and self._site_allowed(actor, asset["site_id"])

    def _itsm_get_incident(self, request: dict[str, Any], actor: dict[str, Any]) -> dict[str, Any]:
        incident = self._find("incidents", request.get("record_id"))
        if not incident:
            return self._respond(request, "NOT_FOUND", error="incident_not_found")
        if not self._incident_allowed(actor, incident):
            return self._respond(request, "DENIED", error="incident_scope_denied")
        return self._respond(request, "SUCCESS", incident)

    def _itsm_search_incidents(self, request: dict[str, Any], actor: dict[str, Any]) -> dict[str, Any]:
        query = str(request.get("query", "")).casefold()
        records = [
            item for item in self._data["incidents"]
            if self._incident_allowed(actor, item) and query in item["title"].casefold()
        ]
        return self._respond(request, "SUCCESS", records)

    def _itsm_get_incident_history(self, request: dict[str, Any], actor: dict[str, Any]) -> dict[str, Any]:
        incident = self._find("incidents", request.get("record_id"))
        if not incident:
            return self._respond(request, "NOT_FOUND", error="incident_not_found")
        if not self._incident_allowed(actor, incident):
            return self._respond(request, "DENIED", error="incident_scope_denied")
        history = [incident]
        previous = self._find("incidents", incident.get("previous_incident_id"))
        if previous and self._incident_allowed(actor, previous):
            history.append(previous)
        return self._respond(request, "SUCCESS", history)

    def _itsm_add_incident_note(self, request: dict[str, Any], actor: dict[str, Any]) -> dict[str, Any]:
        incident = self._find("incidents", request.get("record_id"))
        note = request.get("note")
        if not incident:
            return self._respond(request, "NOT_FOUND", error="incident_not_found")
        if actor["role"] != "it_operator" or not self._site_allowed(actor, incident["site_id"]):
            return self._respond(request, "DENIED", error="incident_write_denied")
        if not isinstance(note, str) or not note.strip() or len(note) > 500:
            return self._respond(request, "INVALID_REQUEST", error="invalid_note")
        self.incident_notes.setdefault(incident["id"], []).append(note.strip())
        return self._respond(request, "SUCCESS", {"incident_id": incident["id"], "note_added": True})

    def _itsm_escalate_incident(self, request: dict[str, Any], actor: dict[str, Any]) -> dict[str, Any]:
        incident = self._find("incidents", request.get("record_id"))
        if not incident:
            return self._respond(request, "NOT_FOUND", error="incident_not_found")
        if actor["role"] != "it_operator" or not self._site_allowed(actor, incident["site_id"]):
            return self._respond(request, "DENIED", error="incident_write_denied")
        self.escalated_incidents.add(incident["id"])
        return self._respond(request, "SUCCESS", {"incident_id": incident["id"], "escalated": True})

    def _documents_get_document(self, request: dict[str, Any], actor: dict[str, Any]) -> dict[str, Any]:
        document = self._find("documents", request.get("record_id"))
        if not document:
            return self._respond(request, "NOT_FOUND", error="document_not_found")
        if not self._document_allowed(actor, document):
            return self._respond(request, "DENIED", error="document_scope_denied")
        return self._respond(request, "SUCCESS", document)

    def _documents_search_documents(self, request: dict[str, Any], actor: dict[str, Any]) -> dict[str, Any]:
        query = str(request.get("query", "")).casefold()
        records = [
            item for item in self._data["documents"]
            if item["is_current"] and self._document_allowed(actor, item)
            and (query in item["title"].casefold() or query in item["content"].casefold())
        ]
        return self._respond(request, "SUCCESS", records)

    def _documents_get_current_document(self, request: dict[str, Any], actor: dict[str, Any]) -> dict[str, Any]:
        family_id = request.get("family_id")
        document = next((d for d in self._data["documents"] if d["family_id"] == family_id and d["is_current"]), None)
        if not document:
            return self._respond(request, "NOT_FOUND", error="current_document_not_found")
        if not self._document_allowed(actor, document):
            return self._respond(request, "DENIED", error="document_scope_denied")
        return self._respond(request, "SUCCESS", document)

    def _hr_get_user_context(self, request: dict[str, Any], actor: dict[str, Any]) -> dict[str, Any]:
        if request.get("record_id") not in {None, actor["id"]}:
            return self._respond(request, "DENIED", error="hr_scope_denied")
        fields = {key: actor[key] for key in ["id", "role", "department_id", "primary_site_id", "site_scope"]}
        return self._respond(request, "SUCCESS", fields)

    def _hr_get_department(self, request: dict[str, Any], actor: dict[str, Any]) -> dict[str, Any]:
        if request.get("record_id") != actor["department_id"]:
            return self._respond(request, "DENIED", error="hr_scope_denied")
        return self._respond(request, "SUCCESS", self._find("departments", actor["department_id"]))

    def _hr_confirm_employee_active(self, request: dict[str, Any], actor: dict[str, Any]) -> dict[str, Any]:
        if request.get("record_id") not in {None, actor["id"]}:
            return self._respond(request, "DENIED", error="hr_scope_denied")
        return self._respond(request, "SUCCESS", {"user_id": actor["id"], "active": True})

    def _erp_allowed(self, actor: dict[str, Any]) -> bool:
        return actor["department_id"] in {"DEPT-PROC", "DEPT-FIN"}

    def _erp_get_supplier(self, request: dict[str, Any], actor: dict[str, Any]) -> dict[str, Any]:
        supplier = self._find("suppliers", request.get("record_id"))
        if not supplier:
            return self._respond(request, "NOT_FOUND", error="supplier_not_found")
        if not self._erp_allowed(actor):
            return self._respond(request, "DENIED", error="supplier_scope_denied")
        return self._respond(request, "SUCCESS", supplier)

    def _erp_get_supplier_status(self, request: dict[str, Any], actor: dict[str, Any]) -> dict[str, Any]:
        supplier = self._find("suppliers", request.get("record_id"))
        if not supplier:
            return self._respond(request, "NOT_FOUND", error="supplier_not_found")
        if not self._erp_allowed(actor):
            return self._respond(request, "DENIED", error="supplier_scope_denied")
        return self._respond(request, "SUCCESS", {"supplier_id": supplier["id"], "status": supplier["status"]})

    def _erp_search_suppliers(self, request: dict[str, Any], actor: dict[str, Any]) -> dict[str, Any]:
        if not self._erp_allowed(actor):
            return self._respond(request, "DENIED", error="supplier_scope_denied")
        query = str(request.get("query", "")).casefold()
        records = [s for s in self._data["suppliers"] if query in s["name"].casefold() or query == s["category"].casefold()]
        return self._respond(request, "SUCCESS", records)

    def _plant_get_asset(self, request: dict[str, Any], actor: dict[str, Any]) -> dict[str, Any]:
        asset = self._find("assets", request.get("record_id"))
        if not asset:
            return self._respond(request, "NOT_FOUND", error="asset_not_found")
        if not self._asset_allowed(actor, asset):
            return self._respond(request, "DENIED", error="asset_scope_denied")
        return self._respond(request, "SUCCESS", asset)

    def _plant_get_asset_state(self, request: dict[str, Any], actor: dict[str, Any]) -> dict[str, Any]:
        asset = self._find("assets", request.get("record_id"))
        if not asset:
            return self._respond(request, "NOT_FOUND", error="asset_not_found")
        if not self._asset_allowed(actor, asset):
            return self._respond(request, "DENIED", error="asset_scope_denied")
        return self._respond(request, "SUCCESS", {"asset_id": asset["id"], "status": asset["status"]})

    def _plant_list_assets(self, request: dict[str, Any], actor: dict[str, Any]) -> dict[str, Any]:
        site_id = request.get("site_id")
        if site_id not in actor["site_scope"] or actor["role"] not in {"it_operator", "plant_operations_manager"}:
            return self._respond(request, "DENIED", error="asset_scope_denied")
        return self._respond(request, "SUCCESS", [a for a in self._data["assets"] if a["site_id"] == site_id])

    def _monitoring_get_alert(self, request: dict[str, Any], actor: dict[str, Any]) -> dict[str, Any]:
        alert = self._find("alerts", request.get("record_id"))
        if not alert:
            return self._respond(request, "NOT_FOUND", error="alert_not_found")
        if actor["role"] not in {"it_operator", "plant_operations_manager"} or not self._site_allowed(actor, alert["site_id"]):
            return self._respond(request, "DENIED", error="alert_scope_denied")
        return self._respond(request, "SUCCESS", alert)

    def _monitoring_list_alerts(self, request: dict[str, Any], actor: dict[str, Any]) -> dict[str, Any]:
        site_id = request.get("site_id")
        if site_id not in actor["site_scope"] or actor["role"] not in {"it_operator", "plant_operations_manager"}:
            return self._respond(request, "DENIED", error="alert_scope_denied")
        records = [a for a in self._data["alerts"] if a["site_id"] == site_id]
        return self._respond(request, "SUCCESS", records)

    def _monitoring_get_service_health(self, request: dict[str, Any], actor: dict[str, Any]) -> dict[str, Any]:
        if actor["role"] != "it_operator":
            return self._respond(request, "DENIED", error="health_scope_denied")
        return self._respond(request, "SUCCESS", {"service_id": request.get("record_id"), "status": "healthy", "simulated": True})

    def _operations_restart_simulated_service(self, request: dict[str, Any], actor: dict[str, Any]) -> dict[str, Any]:
        key = request.get("idempotency_key")
        if actor["role"] != "it_operator":
            return self._respond(request, "DENIED", error="action_role_denied")
        approval = self._find("approvals", request.get("approval_id"))
        action = self._find("actions", request.get("action_id"))
        if not approval or not action or approval["action_id"] != action["id"] or action["approval_id"] != approval["id"]:
            return self._respond(request, "DENIED", error="approval_mismatch")
        if approval["requester_id"] != actor["id"] or approval["decision"] != "APPROVED":
            return self._respond(request, "DENIED", error="approval_not_valid")
        decided_at = datetime.fromisoformat(approval["decided_at"].replace("Z", "+00:00"))
        expires_at = datetime.fromisoformat(approval["expires_at"].replace("Z", "+00:00"))
        if decided_at > expires_at:
            return self._respond(request, "DENIED", error="approval_expired")
        outcome = action["outcome"]
        result = {
            "outcome": outcome,
            "data": {
                "action_id": action["id"],
                "service_id": request.get("record_id"),
                "evidence": action["evidence"],
                "simulated": True,
            },
            "error": "execution_confirmation_lost" if outcome == "UNKNOWN" else ("simulated_action_failed" if outcome == "FAILED" else None),
        }
        return self._respond(request, result["outcome"], result["data"], result["error"])
