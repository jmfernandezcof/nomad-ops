# NOMAD Ops — Observability Responsibilities

**Product:** NOMAD Ops
**Organization:** Asteria Manufacturing Group
**Spec:** 002-architecture-foundation
**File:** `observability.md`
**Status:** APPROVED

---

## 1. Purpose

This document defines logical observability responsibilities. It does not select a telemetry stack, vendor, storage product, retention period, SLO or deployment topology.

## 2. Core Principle

NOMAD Ops must make relevant requests, decisions, executions, failures, degradation, usage and cost traceable without turning telemetry into an uncontrolled copy of business data.

## 3. Audit and Telemetry

Audit evidence and operational telemetry are related but distinct. Audit supports accountability; metrics, logs and traces support operational diagnosis. Neither is a system of record for enterprise business data.

## 4. Correlation

Relevant operations should carry a request or correlation identifier across frontend, backend, policy, retrieval, models, tools, workflows and external integrations. Human and executing service identities must remain distinguishable.

## 5. Authorization and HITL Evidence

Where applicable, evidence must identify the request, resource, action, authorization outcome, approval reference and execution outcome. Approval records must preserve their binding context and post-approval revalidation outcome without exposing unnecessary protected payloads.

## 6. Execution and Failure

Telemetry must preserve `NOT_STARTED`, `SUCCESS`, `FAILED` and `UNKNOWN`. `DENY` maps to `NOT_STARTED`. Partial workflows must expose relevant step outcomes, and uncertain writes must remain `UNKNOWN`.

## 7. Retrieval

Retrieval telemetry should expose source references, version context, result counts, latency and failure category where appropriate. It must not reveal unauthorized documents or protected chunks.

## 8. Models and Cost

Model telemetry may record provider and model references, latency, token usage, cost, validation outcome and failure category. Failed calls retain usage accounting. Full prompts and outputs are not required when safe metadata is sufficient.

## 9. Tools, Workflows and Integrations

Telemetry should identify the approved capability, target, operation, latency, retry count, rate-limit or contract error and execution state. Model proposals must remain distinguishable from backend-authorized execution.

## 10. Dependency Health and Degradation

The platform must make capability-specific dependency failures and explicit degradation visible. Observability must not imply that an unavailable dependency succeeded or that unrelated healthy capabilities failed.

## 11. Data Protection

Telemetry is data and remains subject to authorization, classification, minimization, masking and access control. Critical secrets must never appear in application, model, workflow, audit, log or trace content.

## 12. Access, Retention and Integrity

Access, integrity, retention and deletion controls must be defined by approved policy. This document does not set durations or select storage; those matters remain open decisions.

## 13. Capacity and Service Objectives

Metrics may support future capacity, performance, availability and SLO decisions. No workload target, threshold, alert value or service objective is established here.

## 14. Environment Separation

Telemetry must preserve logical environment identity and must not silently combine development, sandbox, production-like or future production data where doing so violates policy or scope.

## 15. Logical Responsibility

Observability responsibilities may be implemented by one or more later-approved components. They do not imply a monitoring vendor, collector, dashboard, tracing backend or separate service.

## 16. Observability Principle

> NOMAD Ops must provide enough trustworthy operational evidence to reconstruct relevant behaviour while collecting no more protected data than the purpose requires.
