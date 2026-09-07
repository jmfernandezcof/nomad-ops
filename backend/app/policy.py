from dataclasses import dataclass


@dataclass(frozen=True)
class Decision:
    outcome: str
    policy_version: str = "v1"


class PolicyEngine:
    RULES = {
        "documents.search": {"employee", "it_operator", "plant_operations_manager", "department_manager"},
        "alerts.read": {"it_operator", "plant_operations_manager"},
    }

    def decide(self, user: dict, capability: str) -> Decision:
        return Decision("ALLOW" if user["role"] in self.RULES.get(capability, set()) else "DENY")
