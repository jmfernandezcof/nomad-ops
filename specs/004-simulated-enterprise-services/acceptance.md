# NOMAD Ops — Simulated Enterprise Services Acceptance

**Product:** NOMAD Ops
**Organization:** Asteria Manufacturing Group
**Spec:** 004-simulated-enterprise-services
**Status:** APPROVED

---

## 1. Acceptance Criteria

The first-version simulation is acceptable when:

1. All six modules load the approved synthetic dataset.
2. Shared identifiers refer to the same fictional entity across modules.
3. Each approved read capability returns only authorized and necessary fields.
4. Cross-site and cross-department denied examples are enforced.
5. Current documents are distinguishable from superseded documents.
6. Incident, alert, asset and runbook records form the approved investigation journey.
7. HR returns only the minimum identity context required.
8. The controlled action cannot run without the required authorization and approval.
9. Rejected, expired or mismatched approval prevents execution.
10. Reusing an action's idempotency key cannot create a duplicate effect.
11. Success includes evidence; known failure is reported as failure.
12. An uncertain write remains `UNKNOWN` and is not automatically repeated.
13. Required failure profiles can be demonstrated predictably.
14. Calls and outcomes are traceable without exposing secrets or unnecessary sensitive content.
15. No operation can affect real systems, host services or industrial equipment.
16. The six approved product journeys pass their applicable checks.

## 2. Required Evidence

Acceptance requires repeatable automated checks plus a short demonstration of:

- an allowed read;
- a denied read;
- current-versus-superseded document handling;
- a successful approved action;
- a rejected or expired action;
- an uncertain outcome;
- audit reconstruction of the action journey.

## 3. Implementation Gate

The simulated service must not be implemented until this specification is approved. Approval also authorizes recording the first-version mock-service shape in the architecture decision register.
