import unittest

from simulator import SimulationService


def request(operation, actor_id, **values):
    contexts = {
        "USR-001": {
            "role": "plant_operations_manager",
            "department_id": "DEPT-OPS",
            "site_scope": ["SITE-CR"],
        },
        "USR-003": {
            "role": "it_operator",
            "department_id": "DEPT-IT",
            "site_scope": ["SITE-MAD", "SITE-TOL", "SITE-CR", "SITE-VLC"],
        },
        "USR-006": {
            "role": "employee",
            "department_id": "DEPT-PROC",
            "site_scope": ["SITE-MAD"],
        },
    }
    return {
        "request_id": values.pop("request_id", f"test-{operation}"),
        "caller_service_id": "nomad-ops-svc",
        "actor_id": actor_id,
        "actor_context": contexts.get(actor_id, {}),
        "operation": operation,
        **values,
    }


class SimulationServiceTests(unittest.TestCase):
    def setUp(self):
        self.service = SimulationService()

    def test_employee_finds_current_authorized_procedure(self):
        result = self.service.call(request("documents.search_documents", "USR-006", query="supplier onboarding"))
        self.assertEqual("SUCCESS", result["outcome"])
        self.assertEqual(["DOC-001"], [item["id"] for item in result["data"]])

    def test_plant_manager_cannot_read_other_plant_alert(self):
        allowed = self.service.call(request("monitoring.get_alert", "USR-001", record_id="ALT-003"))
        denied = self.service.call(request("monitoring.get_alert", "USR-001", record_id="ALT-004"))
        self.assertEqual("SUCCESS", allowed["outcome"])
        self.assertEqual("DENIED", denied["outcome"])

    def test_it_operator_can_follow_incident_history(self):
        result = self.service.call(request("itsm.get_incident_history", "USR-003", record_id="INC-001"))
        self.assertEqual("SUCCESS", result["outcome"])
        self.assertEqual(["INC-001", "INC-002"], [item["id"] for item in result["data"]])

    def test_hr_context_is_minimized_and_self_only(self):
        own = self.service.call(request("hr.get_user_context", "USR-003", record_id="USR-003"))
        other = self.service.call(request("hr.get_user_context", "USR-003", record_id="USR-001"))
        self.assertEqual("SUCCESS", own["outcome"])
        self.assertNotIn("email", own["data"])
        self.assertEqual("DENIED", other["outcome"])

    def test_action_requires_matching_approval(self):
        result = self.service.call(request(
            "operations.restart_simulated_service", "USR-003",
            record_id="telemetry-service-cr", action_id="ACT-001",
            approval_id="APR-002", idempotency_key="key-denied",
        ))
        self.assertEqual("DENIED", result["outcome"])

    def test_rejected_and_expired_approvals_do_not_execute(self):
        cases = [("ACT-002", "APR-002"), ("ACT-003", "APR-003")]
        for index, (action_id, approval_id) in enumerate(cases):
            with self.subTest(approval_id=approval_id):
                result = self.service.call(request(
                    "operations.restart_simulated_service", "USR-003",
                    request_id=f"blocked-{index}", record_id="telemetry-service-cr",
                    action_id=action_id, approval_id=approval_id,
                    idempotency_key=f"blocked-key-{index}",
                ))
                self.assertEqual("DENIED", result["outcome"])

    def test_approved_action_is_idempotent(self):
        first = self.service.call(request(
            "operations.restart_simulated_service", "USR-003",
            request_id="restart-one", record_id="telemetry-service-cr",
            action_id="ACT-001", approval_id="APR-001", idempotency_key="same-action",
        ))
        second = self.service.call(request(
            "operations.restart_simulated_service", "USR-003",
            request_id="restart-two", record_id="telemetry-service-cr",
            action_id="ACT-001", approval_id="APR-001", idempotency_key="same-action",
        ))
        self.assertEqual("SUCCESS", first["outcome"])
        self.assertEqual(first["data"], second["data"])
        self.assertEqual(1, len(self.service._idempotent_results))

    def test_uncertain_action_is_preserved(self):
        result = self.service.call(request(
            "operations.restart_simulated_service", "USR-003",
            record_id="telemetry-service-cr", action_id="ACT-006",
            approval_id="APR-006", idempotency_key="unknown-action",
        ))
        self.assertEqual("UNKNOWN", result["outcome"])
        self.assertEqual("uncertain", result["completeness"])

    def test_failure_profile_is_controlled_and_explicit(self):
        service = SimulationService(failure_profiles={"monitoring.get_alert": "unavailable"})
        result = service.call(request("monitoring.get_alert", "USR-003", record_id="ALT-003"))
        self.assertEqual("UNAVAILABLE", result["outcome"])
        self.assertEqual("unavailable", result["error"])

    def test_unknown_service_identity_is_rejected(self):
        payload = request("itsm.get_incident", "USR-003", record_id="INC-001")
        payload["caller_service_id"] = "untrusted-service"
        result = self.service.call(payload)
        self.assertEqual("INVALID_REQUEST", result["outcome"])

    def test_mismatched_actor_context_is_rejected(self):
        payload = request("itsm.get_incident", "USR-003", record_id="INC-001")
        payload["actor_context"]["site_scope"] = ["SITE-CR"]
        result = self.service.call(payload)
        self.assertEqual("DENIED", result["outcome"])
        self.assertEqual("actor_context_mismatch", result["error"])

    def test_approved_action_audit_history_is_reconstructable(self):
        approvals = {item["id"]: item for item in self.service._data["approvals"]}
        actions = {item["id"]: item for item in self.service._data["actions"]}
        events = [item for item in self.service._data["audit_events"] if item["action_id"] == "ACT-001"]
        self.assertEqual("ACT-001", approvals["APR-001"]["action_id"])
        self.assertEqual("APR-001", actions["ACT-001"]["approval_id"])
        self.assertEqual(
            ["request_received", "authorization_checked", "approval_decided", "execution_recorded"],
            [item["event_type"] for item in events],
        )


if __name__ == "__main__":
    unittest.main()
