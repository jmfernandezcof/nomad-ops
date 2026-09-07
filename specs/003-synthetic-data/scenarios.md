# NOMAD Ops — Synthetic Demonstration Scenarios

**Product:** NOMAD Ops
**Organization:** Asteria Manufacturing Group
**Spec:** 003-synthetic-data
**Status:** APPROVED

---

## 1. Scenario Set

The data must contain six named, connected scenarios matching the approved product scope.

### SD-001 — Authorized Procedure Search

An employee finds the current procedure permitted for their department and site. An outdated version also exists so the system must not present it as current.

### SD-002 — IT Incident Investigation

An IT operator reviews an incident, related monitoring alerts, the affected asset, a previous incident and an authorized runbook. The records must form one consistent timeline.

### SD-003 — Plant Access Boundary

A Ciudad Real plant manager can review a local operational alert and related records. An equivalent Valencia record exists but must be denied because it falls outside the manager's scope.

### SD-004 — Controlled Action With Approval

An authorized user requests a simulated sensitive action. The correct manager approves it, the approval is rechecked and the action completes with evidence.

### SD-005 — Compliance Review

A compliance user reviews the request, authorization decision, approval and execution history for SD-004 but has no permission to perform the operational action.

### SD-006 — Uncertain Action Outcome

A simulated action times out after execution may have started. Its state remains uncertain, it is not automatically repeated and the records support a safe human investigation.

## 2. Supporting Cases

The dataset must also include ordinary background records and negative cases so the six journeys are not isolated demonstrations with only one possible answer.

Negative cases must cover denied access, rejected approval, expired approval, missing evidence, outdated documents, broken relationships detected during validation and dependency failure.

## 3. Cross-System Coherence

Each scenario must include a manifest listing all participating records. Every reference in that manifest must resolve to the same canonical Asteria entity.
