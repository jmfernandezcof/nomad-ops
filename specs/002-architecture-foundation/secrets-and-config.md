# NOMAD Ops — Secrets and Configuration Boundaries

**Product:** NOMAD Ops
**Organization:** Asteria Manufacturing Group
**Spec:** 002-architecture-foundation
**File:** `secrets-and-config.md`
**Status:** APPROVED

---

## 1. Purpose

This document defines logical boundaries for configuration and secrets. It contains no credentials and selects no secrets-management technology, configuration product or deployment mechanism.

## 2. Configuration and Secrets

Configuration describes approved system behaviour. A secret grants or protects access. Secret values must not be treated as ordinary configuration or exposed through configuration interfaces.

## 3. Critical Secrets

Passwords, API keys, tokens, private keys, signing secrets, encryption secrets and privileged credentials are `CRITICAL`. They must not enter LLM context, RAG, embeddings, Qdrant, frontend responses, tool outputs, source code, SPECs, tests or application, model, workflow and audit logs.

## 4. Secret Resolution

Components and tools requiring credentials must resolve them outside model and user-facing context through a later-approved mechanism. An LLM may receive only a safe abstraction such as `credential_available = true`.

## 5. Least Privilege

Credentials and service identities must be scoped to the minimum approved systems, resources, operations and environments. Credential possession does not establish user authorization or permit policy bypass.

## 6. Human and Service Identity

Executing service identity and initiating human identity must remain distinguishable. A shared or powerful service credential must not transfer equivalent authority to the requester.

## 7. Environment Separation

Development, sandbox, production-like and future production contexts must not silently share privileged credentials, unrestricted writes or security configuration. Sensitive simulations must use only approved mock or sandbox targets.

## 8. Frontend and Client Boundary

Privileged secrets must not be sent to browsers or clients. Frontend-visible configuration must be treated as public to the receiving user and must not be relied upon as a security boundary.

## 9. Tools, Workflows and Providers

Tools and workflows receive only credentials needed for their narrow approved capability. n8n credentials remain outside LLM control. Provider configuration must preserve classification, processing and eligibility policy.

## 10. Configuration Authority and Validation

Security-relevant configuration must have an explicit owner, be validated before use and remain auditable where appropriate. Frontend, LLM output, retrieved content and external responses must not redefine it.

## 11. Failure Behaviour

Missing, invalid or unavailable required configuration must produce an explicit controlled failure or unavailable capability. NOMAD Ops must not fabricate values, weaken policy or silently fall back to a less secure configuration.

## 12. Logging and Audit

Secret values must never be logged. Safe identifiers, credential references, operation type and outcome may be recorded when required. Configuration audit must avoid copying unnecessary protected values.

## 13. Lifecycle and Technology Decisions

Storage technology, provisioning, rotation, revocation, expiry, recovery and access-review mechanisms remain open until approved. This document does not select environment files, a vault product, cloud service or key-management system.

## 14. Secrets and Configuration Principle

> Configuration may direct approved behaviour; credentials enable narrowly scoped access; neither may bypass deterministic authorization, environment boundaries or audit requirements.
