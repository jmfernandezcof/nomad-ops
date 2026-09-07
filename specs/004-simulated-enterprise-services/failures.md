# NOMAD Ops — Simulated Failures and State

**Product:** NOMAD Ops
**Organization:** Asteria Manufacturing Group
**Spec:** 004-simulated-enterprise-services
**Status:** APPROVED

---

## 1. Purpose

The simulations must demonstrate safe behaviour when dependencies fail. Failure modes are selected explicitly by scenario and must never occur randomly during acceptance tests.

## 2. Required Failure Modes

The simulation must support:

- unavailable service;
- slow response and timeout;
- missing record;
- denied access;
- invalid input;
- incomplete response;
- changed or invalid response contract;
- rate limit;
- known failed write;
- write with uncertain outcome.

## 3. Safe Repetition

Read-only operations may be repeated within an approved limit.

`restart_simulated_service` must use an idempotency key. Repeating the same confirmed request must not create a second restart.

If the simulation receives an action but loses confirmation after execution may have begun, it returns `UNKNOWN`. NOMAD Ops must inspect state or request human review instead of automatically repeating it.

## 4. Scenario Control

Failure behaviour must be activated through a controlled test profile linked to an approved scenario. Ordinary users and AI models cannot change that profile.

## 5. Recovery

Clearing a failure profile restores normal simulated operation without changing the canonical dataset unless the scenario explicitly records a state transition.
