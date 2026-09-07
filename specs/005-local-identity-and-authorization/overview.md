# NOMAD Ops — Local Identity and Authorization

**Product:** NOMAD Ops
**Organization:** Asteria Manufacturing Group
**Spec:** 005-local-identity-and-authorization
**Status:** APPROVED

---

## 1. Purpose

This specification defines how fictional users enter the first-version laboratory and how NOMAD Ops decides what each user may see or do.

## 2. First-Version Approach

The laboratory will use local accounts for the approved synthetic users.

Each person signs in with their Asteria demonstration email and a password held separately from the synthetic business dataset. There is no public registration and no real employee account is required.

Changing to a future company identity provider must not change the business permission rules.

## 3. Separation of Responsibilities

- Authentication confirms which fictional user is present.
- User context supplies the approved role, department and site scope.
- Deterministic policy decides whether a request is allowed, denied or needs human approval.
- The simulator independently checks the context it receives.
- AI may explain or propose an action but never decides access.

## 4. Proposed Policy Shape

First-version permission rules will be versioned application rules rather than a new external policy service.

This avoids adding another platform component while keeping all decisions explicit and testable. A dedicated policy service may be considered later if scale or governance demonstrates a need.

## 5. Environment Boundary

Local accounts authorize access only to the sandbox demonstration. They are not production identities and cannot affect real company systems, industrial equipment or unrelated VPS services.
