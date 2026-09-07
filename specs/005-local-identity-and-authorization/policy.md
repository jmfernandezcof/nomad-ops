# NOMAD Ops — First-Version Authorization Policy

**Product:** NOMAD Ops
**Organization:** Asteria Manufacturing Group
**Spec:** 005-local-identity-and-authorization
**Status:** APPROVED

---

## 1. Decision Model

Every protected request produces exactly one decision:

- `ALLOW`;
- `DENY`;
- `REQUIRE_APPROVAL`.

No matching rule means `DENY`.

The decision uses the current user, role, department, site scope, target record, requested action, data classification, environment and action risk.

## 2. Initial Permissions

### Employee

- Search and read current internal documents for their own department and site.
- Read their own minimum organizational context.
- Procurement employees may read supplier status.
- No operational actions or approval rights.

### IT Operator

- Read assigned-site IT incidents, monitoring and technical assets.
- Search authorized IT runbooks.
- Add an internal incident note or request escalation.
- Request a simulated service restart.
- A sensitive restart requires approval from an eligible manager for the affected site.

### Plant Operations Manager

- Read incidents, alerts, assets and procedures for assigned plants.
- Approve the defined simulated action for an assigned plant.
- No access to other plants or unrelated HR and Finance information.

### Department Manager

- Read authorized documents and business information for their department and site.
- Finance and Procurement managers may read supplier information.
- Approval is limited to actions explicitly assigned to their department.

### Compliance / Governance

- Review authorization, approval, action and audit records within assigned oversight scope.
- Cannot perform the operational action being reviewed.

### NOMAD Ops Admin

- Manage approved platform configuration.
- Administration does not automatically grant access to business records.
- Sensitive administrative activity remains auditable and may require approval.

## 3. Approval Binding

An approval is valid only for its exact:

- requester;
- action;
- target;
- site;
- important input values;
- environment;
- validity period.

Permissions and context are checked again after approval and before execution. Rejected, expired, mismatched or stale approval leaves execution at `NOT_STARTED`.

## 4. Data Rules

- Authorization occurs before protected retrieval.
- Search cannot reveal the existence or contents of unauthorized records.
- Current classification applies even if an older cached copy exists.
- Unknown classification is restricted.
- Returned fields are minimized for the request.

## 5. Audit

Relevant decisions record references to the user, policy version, resource, action, scope, decision, approval and result without copying unnecessary protected content.
