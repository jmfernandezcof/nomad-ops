# NOMAD Ops — Actors and Access Context

**Product:** NOMAD Ops
**Organization:** Asteria Manufacturing Group
**Spec:** 001-system-context
**File:** `actors.md`
**Status:** APPROVED

---

## 1. Purpose

This document defines the principal user actors that interact with NOMAD Ops and the context used to determine what each user may see or do.

It does not define the full authorization engine or technical implementation.

Its purpose is to establish:

- the initial actor types;
- the distinction between role, department and site;
- the expected scope of each actor;
- examples of allowed and restricted behaviour;
- the principle that authorization is enforced by the platform, not by an LLM.

---

## 2. Access Model Principle

NOMAD Ops must not determine access using role alone.

User access is based on a combination of:

- role;
- department;
- site;
- resource;
- action;
- data sensitivity;
- operational context.

Conceptually:

**Permission = Role + Resource + Action + Scope + Context**

A role describes what kind of responsibility a user has.

Department and site define where that responsibility applies.

Example:

A user may be:

- Role: `Plant Operations Manager`
- Department: `Operations`
- Site: `Plant 2 — Ciudad Real`

That user may be allowed to approve certain operational actions for Plant 2 without receiving equivalent permissions for Plant 1, Finance or HR.

---

## 3. Separation of Concerns

The following concepts must remain separate.

### Role

Defines the functional responsibility of the user.

Examples:

- Employee
- IT Operator
- Department Manager

### Department

Defines the organizational area to which the user belongs or has responsibility.

Initial departments may include:

- IT
- Operations
- Finance
- Human Resources
- Procurement
- Compliance
- Corporate

### Site

Defines the physical or organizational location relevant to the user's scope.

Initial sites are:

- Madrid HQ
- Plant 1 — Toledo
- Plant 2 — Ciudad Real
- Plant 3 — Valencia

A user may have access to:

- one site;
- multiple sites;
- corporate-wide resources;

depending on explicitly assigned permissions.

---

## 4. Initial Actor Set

NOMAD Ops begins with six principal actor types.

Additional roles must not be added unless a future SPEC demonstrates a concrete need.

---

## 5. Employee

### Purpose

Represents a standard Asteria employee using NOMAD Ops for general operational and knowledge tasks.

### Typical capabilities

May:

- search authorized internal knowledge;
- ask questions about internal procedures;
- view information available to their department or site;
- submit requests;
- use non-sensitive productivity functions;
- receive recommendations and drafts.

### Restrictions

Must not automatically be allowed to:

- view restricted HR information;
- access sensitive financial information;
- execute infrastructure actions;
- approve operational actions;
- modify policies;
- configure tools or workflows;
- access resources outside assigned scope.

### Example

An employee in Procurement at Madrid HQ may query the current supplier onboarding procedure.

That does not imply access to:

- employee medical or HR records;
- Plant 2 operational controls;
- NOMAD Ops administration;
- confidential Finance data.

---

## 6. IT Operator

### Purpose

Represents Service Desk or IT Operations personnel responsible for technical incidents and authorized IT actions.

### Typical capabilities

May:

- view authorized IT incidents;
- search runbooks;
- retrieve historical incidents;
- consult monitoring information;
- request diagnostics;
- create or update tickets;
- invoke approved low-risk IT tools;
- propose escalation.

### Restrictions

Must not automatically be allowed to:

- change NOMAD Ops security policy;
- grant themselves permissions;
- access unrelated HR or Finance data;
- perform high-risk production actions without required approval;
- bypass HITL policy.

### Example

An IT Operator may be allowed to restart a sandbox test service.

The same user may require approval before restarting a production-critical service.

---

## 7. Plant Operations Manager

### Purpose

Represents a manager responsible for operational activity at one or more manufacturing sites.

### Typical capabilities

May:

- view incidents relevant to assigned plants;
- consult plant documentation;
- review alarms and operational state;
- inspect recommended actions;
- approve certain operational actions;
- review activity affecting their site.

### Restrictions

Must not automatically be allowed to:

- access other plants outside their scope;
- access restricted HR or Finance resources;
- administer NOMAD Ops;
- bypass corporate safety or compliance controls;
- approve actions outside their assigned authority.

### Example

A Plant Operations Manager assigned to Plant 2 may approve a medium-risk action affecting Plant 2.

The same user must not gain identical approval rights for Plant 1 unless explicitly authorized.

---

## 8. Department Manager

### Purpose

Represents a manager responsible for a corporate or functional department.

### Typical capabilities

May:

- access information belonging to their authorized department;
- review department-specific workflows;
- approve defined actions;
- review operational activity;
- consult relevant costs and usage where permitted;
- manage business decisions within their scope.

### Restrictions

Must not automatically be allowed to:

- see all departments;
- access unrelated sensitive information;
- modify global authorization policies;
- administer infrastructure;
- approve actions outside their business authority.

### Example

A Finance Department Manager may have access to selected Finance processes and approvals.

This does not imply access to restricted HR records or Plant Operations actions.

---

## 9. Compliance / Governance

### Purpose

Represents users responsible for audit, governance, compliance and oversight.

### Typical capabilities

May:

- review audit records;
- inspect authorization decisions;
- inspect approval history;
- review AI usage;
- review model and tool activity;
- investigate policy violations;
- review access patterns where authorized;
- review governance-related configuration.

### Restrictions

Audit visibility does not automatically mean operational execution rights.

Compliance users must not automatically be able to:

- execute IT actions;
- change production state;
- modify business data;
- bypass approval controls;
- impersonate another user.

### Principle

**The ability to inspect an action is separate from the ability to perform that action.**

---

## 10. NOMAD Ops Admin

### Purpose

Represents authorized administrators responsible for operating the NOMAD Ops platform itself.

### Typical capabilities

May manage authorized platform configuration including:

- users;
- role assignments;
- integrations;
- tools;
- models;
- policies;
- workflows;
- platform settings.

### Restrictions

Administrative capability must remain subject to:

- audit logging;
- least privilege;
- explicit authorization;
- security controls;
- approval requirements where applicable.

The Admin role must not be treated as an invisible or unaudited superuser.

Sensitive administrative actions must remain traceable.

Administrative access to the NOMAD Ops platform does not imply automatic access to all business data or document content.

Business-data access must be granted separately according to role, department, site, resource sensitivity and explicit policy.

---

## 11. Example User Contexts

Synthetic users should demonstrate realistic combinations of role, department and site.

### Carlos Romero

- Role: Plant Operations Manager
- Department: Operations
- Site: Plant 2 — Ciudad Real

Expected behaviour:

- may view Plant 2 operational incidents;
- may access authorized Plant 2 procedures;
- may approve defined Plant 2 actions;
- may not automatically access Plant 1 operational resources;
- may not access restricted HR records.

### Laura Martín

- Role: Department Manager
- Department: Finance
- Site: Madrid HQ

Expected behaviour:

- may access authorized Finance information;
- may approve defined Finance processes;
- may not execute IT infrastructure actions;
- may not access restricted Plant Operations systems.

### Daniel Ortega

- Role: IT Operator
- Department: IT
- Site: Madrid HQ
- Scope: corporate IT where explicitly assigned

Expected behaviour:

- may inspect technical incidents across assigned sites;
- may use approved diagnostic tools;
- may execute low-risk IT actions;
- may require approval for high-risk actions.

These names and identities are synthetic and exist only for the Asteria demonstration environment.

---

## 12. Least Privilege

NOMAD Ops follows the principle of least privilege.

Users must receive only the access required for their responsibilities.

Permissions must not be granted merely because:

- a user is senior;
- a user belongs to a management role;
- the LLM considers the action reasonable;
- access would make a workflow easier to implement.

Access must be explicitly justified by policy.

---

## 13. Deny by Default

Where no explicit permission exists, access must be denied.

The absence of a rule must not be interpreted as permission.

This applies to:

- users;
- agents;
- tools;
- workflows;
- APIs;
- data access.

---

## 14. Authorization Must Be Deterministic

LLMs must never make final authorization decisions.

An LLM may:

- recommend an action;
- classify intent;
- provide context;
- explain why an action may be useful.

An LLM must not decide:

- whether a user is authorized;
- whether a permission may be bypassed;
- whether an approval is unnecessary;
- whether a user may access restricted data.

Authorization must be enforced by deterministic platform logic.

Conceptually:

**Request
→ determine required permission
→ evaluate user + resource + action + scope + context
→ ALLOW / DENY / REQUIRE_APPROVAL**

Only after this decision may execution continue.

---

## 15. Approval and Authorization Are Different

A user may be authorized to request an action without being authorized to execute it immediately.

Example:

An IT Operator may be authorized to request a restart of a critical production service.

Policy may return:

`REQUIRE_APPROVAL`

rather than:

`ALLOW`

The action must not execute until a valid authorized approver has approved it.

---

## 16. No Privilege Escalation Through AI

Neither an LLM nor an agent may:

- grant new permissions;
- expand its own tool access;
- change its own scope;
- alter HITL requirements;
- reinterpret a denial as permission;
- use another user's authority.

If a task requires unavailable permissions, the correct result is denial or escalation to an authorized human.

---

## 17. Auditability

Relevant access and authorization events must be traceable.

Where applicable, the platform must record:

- requesting user;
- assigned role;
- department;
- site;
- requested resource;
- requested action;
- authorization outcome;
- required approval;
- approver;
- execution result.

The detailed audit schema will be defined in a later specification.

---

## 18. Actor Model Principle

The central actor principle is:

> A user is not defined only by who they are, but by what responsibility they hold, where that responsibility applies, what resource they are accessing and what action they are attempting.

NOMAD Ops must enforce those boundaries independently of any AI model.
