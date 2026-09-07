# NOMAD Ops — Application Stack Boundaries

**Product:** NOMAD Ops
**Organization:** Asteria Manufacturing Group
**Spec:** 006-application-stack
**Status:** APPROVED

---

## 1. Browser and Backend

- The browser never decides permissions.
- Protected data is obtained only through the backend.
- Requests and responses use versioned JSON contracts under an `/api/v1` boundary.
- Backend inputs and outputs are validated before use.
- The deployed interface and API should share one trusted origin.
- Development access may allow only explicitly configured local origins.

## 2. Local Authentication

- Passwords are hashed with Argon2 using a maintained library.
- The browser receives an opaque, server-controlled session cookie rather than identity or permission claims.
- The cookie is inaccessible to browser scripts, restricted to the application and sent only over secure connections outside local development.
- State-changing browser requests require protection against cross-site request forgery.
- Session records and revocation state belong in PostgreSQL.
- The approved 30-minute inactivity and 2-hour absolute limits are enforced by the backend.

## 3. Backend Structure

Business logic is separated from web routes.

Routes translate validated requests into application operations. Application services coordinate policy, approvals and integrations. Data repositories isolate storage. Adapters isolate the simulator, n8n, retrieval and future model providers.

No route, AI model or frontend component may bypass policy by calling storage or an integration directly.

## 4. Enterprise Simulator

The existing simulator core remains behind a narrow adapter. The backend supplies verified human and service context; browser claims are not forwarded as authority.

The network transport and deployment boundary for the simulator remain subject to the later deployment decision.

## 5. Dependency Control

Exact compatible versions will be pinned when implementation begins. Dependencies are limited to those required by the approved stack and must be recorded, reviewed and tested before completion.

Approval of this specification authorizes the named application dependencies, but installation still requires the normal environment permission.
