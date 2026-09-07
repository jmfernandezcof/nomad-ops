# NOMAD Ops — Local Identity and Authorization Acceptance

**Product:** NOMAD Ops
**Organization:** Asteria Manufacturing Group
**Spec:** 005-local-identity-and-authorization
**Status:** APPROVED

---

## 1. Authentication Criteria

The first version is acceptable when:

1. A valid active synthetic user can sign in.
2. An invalid password produces a generic rejection.
3. Disabled and locked accounts cannot sign in.
4. Repeated failed attempts are limited and recorded.
5. Logout, 30 minutes of inactivity, the 2-hour absolute limit and account disablement invalidate sessions.
6. Background work cannot extend a user session.
7. Passwords and session references are not exposed in source, logs or business data.
8. Browser-supplied role, department or site values cannot change authorization.

## 2. Authorization Criteria

9. Each protected request returns `ALLOW`, `DENY` or `REQUIRE_APPROVAL`.
10. Missing policy produces `DENY`.
11. Lucía can retrieve the current Procurement procedure but not restricted HR or plant records.
12. Daniel can investigate assigned-site incidents but cannot access unrelated Finance or HR data.
13. Carlos can inspect and approve the defined Ciudad Real action but cannot do so for Valencia.
14. Laura can access authorized Finance information but cannot execute an IT action.
15. Elena can review the action history but cannot execute the action.
16. Miguel's admin role does not grant automatic access to all business data.
17. Unauthorized search results reveal neither content nor record existence.
18. A sensitive action cannot start before valid approval.
19. Authorization and approval are rechecked immediately before execution.
20. Rejected, expired, stale or mismatched approval cannot execute.
21. Human and service identities remain separately traceable.

## 3. Evidence

Acceptance requires automated examples for successful and failed login, session invalidation, every actor type, cross-site denial, cross-department denial, approval lifecycle and attempted context manipulation.

## 4. Implementation Gate

Implementation begins only after approval of this specification and an approved decision for the application framework. Approval authorizes the local-account approach and versioned in-application policy rules for the first-version sandbox.
