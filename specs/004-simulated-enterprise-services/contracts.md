# NOMAD Ops — Simulated Service Contracts

**Product:** NOMAD Ops
**Organization:** Asteria Manufacturing Group
**Spec:** 004-simulated-enterprise-services
**Status:** APPROVED

---

## 1. Contract Principle

NOMAD Ops communicates with the simulations through narrow named operations. It must not expose unrestricted database queries, arbitrary commands or a generic “do anything” operation.

## 2. Required Request Context

Every request must identify:

- a unique request;
- the calling service identity;
- the initiating human where applicable;
- the named operation;
- the target record or approved search filters;
- the user's role, department and site scope;
- an idempotency key for a state-changing operation;
- an approval reference when required.

Missing or invalid context must produce an explicit rejection.

## 3. Required Response

Every response must identify:

- the original request;
- the source system;
- the operation;
- the outcome;
- returned data or an error category;
- source record identifiers;
- the simulated time;
- whether the response is complete, partial or uncertain.

Allowed outcomes are:

- `SUCCESS`;
- `FAILED`;
- `UNKNOWN`;
- `DENIED`;
- `NOT_FOUND`;
- `INVALID_REQUEST`;
- `UNAVAILABLE`;
- `PARTIAL`.

## 4. Authorization

The simulation enforces its boundary even when NOMAD Ops has already checked authorization.

Access is evaluated against operation, record classification, role, department and site. Read and write permissions remain separate.

A model suggestion, document instruction or client-side flag is never sufficient authorization.

## 5. Data Minimization

Responses contain only fields needed by the named operation. For example, confirmation of an employee's department must not return unrelated HR information.

## 6. Traceability

Every call produces a traceable event containing references and outcomes, but not unnecessary sensitive payloads or secrets.
