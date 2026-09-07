# NOMAD Ops — Local Authentication Behaviour

**Product:** NOMAD Ops
**Organization:** Asteria Manufacturing Group
**Spec:** 005-local-identity-and-authorization
**Status:** APPROVED

---

## 1. Accounts

- Accounts correspond to approved synthetic users.
- Login names use the reserved `@asteria.example` domain.
- Public registration is disabled.
- Accounts can be active, disabled or locked.
- Disabled and locked accounts cannot begin a session.

## 2. Passwords

- Passwords are never stored as readable text.
- Passwords are not part of the synthetic business-data exports.
- Demonstration credentials are supplied through the approved secret mechanism.
- Failed login messages must not reveal whether an account exists.
- Repeated failed attempts must be limited and recorded.

## 3. Sessions

- Successful login creates a server-controlled session.
- The browser receives only an opaque session reference.
- Sessions expire after 30 minutes without activity and after a maximum of 2 hours.
- Active use may reset the inactivity timer but never extends the 2-hour maximum.
- Background work does not keep a user's session active.
- No long-running interactive-screen exception exists in the first version.
- Logout and account disablement invalidate the session.
- A session cannot change its own user, role, department or site scope.

These timings apply only to the sandbox first version; production authentication controls remain a separate decision. A future long-running interactive use case requires separate specification and approval before it may extend a session.

## 4. User Context

After authentication, NOMAD Ops resolves the minimum current context from the authoritative local identity records:

- user identifier;
- account state;
- role;
- department;
- site scope.

Values claimed by the browser are ignored for authorization.

## 5. Service Identity

Calls from NOMAD Ops to the enterprise simulator use a separate service identity while retaining the initiating human identifier for traceability.
