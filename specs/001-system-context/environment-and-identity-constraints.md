# NOMAD Ops — Environment and Identity Constraints

**Product:** NOMAD Ops
**Organization:** Asteria Manufacturing Group
**Spec:** 001-system-context
**File:** `environment-and-identity-constraints.md`
**Status:** APPROVED

---

## 1. Purpose

This document defines system-level constraints related to identity, authentication context, environment separation and external processing governance.

Its purpose is to establish:

- the identity model expected for the first version;
- the distinction between authentication and authorization;
- separation between human users and service identities;
- future compatibility with external identity providers;
- environment isolation principles;
- rules for sandbox and simulated actions;
- provider-governance constraints;
- data-residency and retention considerations.

This document does not define detailed authentication protocols, token formats, cloud-provider configuration or deployment topology.

---

## 2. Identity Model for V1

The first version of NOMAD Ops will use a local identity model managed within the NOMAD Ops environment.

This may include:

- synthetic users;
- local authentication;
- role assignments;
- department context;
- site context;
- authorization attributes.

The use of local identity in V1 is a laboratory decision.

It must not imply that a production enterprise deployment should replace an existing corporate identity provider.

---

## 3. Future External Identity Provider Support

NOMAD Ops should be designed so that a future deployment can integrate with an external identity provider.

Possible examples may include:

- Microsoft Entra ID;
- Okta;
- Keycloak;
- another enterprise identity provider.

No provider is selected by this specification.

Future integration may use standards such as:

- OIDC;
- SAML;

where justified by later architecture decisions.

The platform should avoid unnecessary coupling between business authorization logic and the local authentication mechanism.

---

## 4. Authentication and Authorization Are Separate

Authentication answers:

**Who are you?**

Authorization answers:

**What are you allowed to do?**

Successful authentication must not automatically grant access to resources or actions.

Authorization remains governed by:

- role;
- department;
- site;
- resource;
- action;
- data classification;
- operational context;
- applicable policy.

A future change of identity provider must not require redefining the business authorization model.

---

## 5. Human and Service Identities

Human-user identities and service identities must remain distinguishable.

A service acting on behalf of NOMAD Ops must not be represented as though it were a human user.

Where an operation originates from a human request, auditability should preserve both:

- initiating human identity;
- executing service identity.

Service identities must follow least privilege.

---

## 6. Environment Separation

NOMAD Ops must distinguish between different operational contexts.

At minimum, the design must recognize the difference between:

- local development;
- sandbox / demonstration;
- production-like or future production environments.

The fact that environments may initially coexist on the same VPS does not remove the need for logical separation.

Where environment boundaries exist, they should not silently share:

- privileged credentials;
- unrestricted write permissions;
- production-impacting capabilities;
- security configuration.

Detailed deployment isolation will be defined later.

---

## 7. Sensitive Action Simulation

NOMAD Ops may simulate high-risk or sensitive actions for demonstration purposes.

Such actions must operate only against:

- mock services;
- sandbox systems;
- controlled synthetic environments.

A simulated action must not accidentally affect:

- real industrial equipment;
- real production infrastructure;
- real financial systems;
- real HR records;
- unrelated VPS services.

The purpose of simulation is to demonstrate:

- policy evaluation;
- tool calling;
- HITL;
- execution;
- rollback;
- audit;
- failure handling.

Simulation must preserve risk controls even though the target is synthetic.

---

## 8. Model and Provider Governance

External model and AI providers are separate processing domains.

The use of a provider must be governed by explicit policy.

Provider suitability may depend on:

- data classification;
- business purpose;
- privacy requirements;
- retention policy;
- provider logging;
- region or processing location;
- contractual requirements;
- model capability;
- cost;
- latency.

NOMAD Ops must not assume that any available provider may process any category of data.

---

## 9. Data Residency, Retention and External Processing

Where data is processed outside NOMAD Ops infrastructure, the platform must allow governance rules to consider:

- where data is processed;
- whether prompts or outputs are retained;
- whether provider logging is enabled;
- whether data may be used for provider training;
- contractual or regulatory restrictions;
- deletion or retention guarantees.

This specification does not define exact legal or geographical requirements for Asteria.

It establishes that these factors are relevant architecture and governance constraints and must not be ignored.

Where a data classification or policy prohibits external processing, NOMAD Ops must support:

- local processing;
- an approved restricted provider;
- or refusal to process.

The system must not weaken policy merely to obtain an AI answer.

---

## 10. Environment and Identity Principle

The central principle is:

> Identity proves who or what is acting; policy determines what that identity may do; environment boundaries determine where those actions may occur.

Local V1 authentication is an implementation choice for the laboratory, not a replacement for enterprise identity architecture.

Sensitive demo behaviour must remain isolated from real systems, and external AI processing must remain subject to explicit governance.
