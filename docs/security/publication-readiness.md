# Security and Public-Repository Readiness Review

**Review date:** 2026-09-07
**Scope:** current worktree, five Git commits, tracked prototype archive, Python/FastAPI backend, React/TypeScript frontend, synthetic data and public documentation
**Conclusion:** suitable for a public source repository after the remediations recorded below. This conclusion does not approve direct Internet deployment of the application.

## Executive summary

No private keys, provider tokens or other known secret formats were found in the current repository, its reachable Git history or the tracked prototype ZIP. Network and identity searches found only loopback addresses, package-registry URLs and addresses under the reserved `.example` domain in the new implementation. All business records are generated synthetic fixtures.

The review found vulnerable Python pins and host-specific operational disclosure. Both were corrected before publication. Production defaults, request validation, session rehydration and repository exclusions were also hardened. The remaining high-risk items are deployment gates: rate and body-size limits, forwarded-header trust, frontend security headers, runtime secret delivery and monitoring are not implemented in this repository.

## Resolved findings

### SEC-001 — Vulnerable Python dependency pins

- **Rule ID:** FASTAPI-SUPPLY-001 / REACT-SUPPLY-001
- **Severity:** High
- **Location:** `backend/requirements.txt:1-6`, `backend/requirements-dev.txt:1-2`, `backend/requirements.lock:1-28`
- **Evidence:** the pre-remediation lock resolved Starlette 0.49.3 and pytest 8.4.2. `pip-audit` reported eight advisory records across those two packages, including host/path parsing, form resource consumption and local temporary-directory issues.
- **Impact:** affected deployments or shared development hosts could be exposed to request interpretation flaws, resource exhaustion or local denial of service/privilege risk.
- **Fix:** upgraded FastAPI, Starlette and pytest; migrated the test client to httpx2; generated a complete transitive lock. A post-fix `pip-audit` reported no known vulnerabilities.
- **Mitigation:** continue auditing both the lock and npm dependency tree in CI or before each release.
- **False positive notes:** some individual Starlette advisories require features this slice does not use, but keeping a vulnerable framework pin was unnecessary.

### SEC-002 — Host-specific operational disclosure

- **Rule ID:** PUBLICATION-DATA-001
- **Severity:** Medium
- **Location:** `docs/operations/environment-baseline.md:1-37`, `docs/operations/change-log.md:1-21`
- **Evidence:** the pre-remediation drafts named unrelated workloads and described live host capacity, proxy, network and service state.
- **Impact:** publication would provide unnecessary infrastructure reconnaissance and disclose information about systems outside this repository's scope.
- **Fix:** replaced the drafts with a public-safe baseline and moved exact host evidence, identifiers and command output outside the repository.
- **Mitigation:** review future operations notes before committing and keep the public/private evidence boundary explicit.
- **False positive notes:** technology names in architecture specifications describe design constraints; they are not live host inventory.

### SEC-003 — Unsafe or ambiguous production defaults

- **Rule ID:** FASTAPI-OPENAPI-001 / FASTAPI-HEADERS-001 / FASTAPI-HOST-001 / FASTAPI-SESS-001
- **Severity:** Medium
- **Location:** `backend/app/main.py:33-63`, `backend/app/main.py:75-84`
- **Evidence:** the initial app used default documentation routes, had no host allowlist and did not attach defensive headers. Cookie security depended entirely on a string environment setting.
- **Impact:** a careless public deployment could expose API discovery, accept hostile Host values, permit caching of protected responses or emit an insecure session cookie.
- **Fix:** production now disables OpenAPI UI/routes, requires a non-wildcard host allowlist, forces secure cookies and adds no-store, CSP, framing, MIME, referrer and permissions headers to API responses.
- **Mitigation:** duplicate critical header and host controls at the edge and verify them against the deployed URL.
- **False positive notes:** some controls may also exist at an external proxy, but no deployable proxy configuration is committed here.

### SEC-004 — Input and session-state hardening gaps

- **Rule ID:** FASTAPI-VALID-001 / REACT-NET-001 / FASTAPI-CSRF-001
- **Severity:** Medium
- **Location:** `backend/app/main.py:18-22`, `backend/app/main.py:100-120`, `frontend/src/api.ts:6-11`, `frontend/src/main.tsx:42-50`
- **Evidence:** login models previously ignored unexpected fields, search/path values were unbounded, the generic browser helper accepted any target, and a page reload did not recover the CSRF token needed for logout.
- **Impact:** future handler changes could accidentally accept mass-assignment fields; unbounded input increases abuse surface; an unconstrained authenticated request helper increases the chance of credential leakage; session logout failed after reload.
- **Fix:** reject extra login fields, bound API identifiers and queries, restrict browser calls to same-origin API paths and rehydrate CSRF state from the server-side session.
- **Mitigation:** keep state-changing endpoints behind both authorization and CSRF validation and add schemas for each new contract.
- **False positive notes:** current request destinations were constants, so the outbound-request issue was defense-in-depth rather than a demonstrated exploit.

### SEC-005 — Repository exclusion and reproducibility gaps

- **Rule ID:** REPOSITORY-HYGIENE-001 / REACT-SUPPLY-001
- **Severity:** Low
- **Location:** `.gitignore:1-26`, `.env.example:1-5`, `backend/requirements.lock:1-28`, `frontend/package-lock.json`
- **Evidence:** the initial ignore file did not cover common environment variants, key containers, test artifacts, IDE state or TypeScript build metadata; Python transitive dependencies were not locked.
- **Impact:** a future contributor could accidentally stage local configuration or non-reproducible dependency changes.
- **Fix:** expanded exclusions, added a placeholder-only environment example and generated a complete Python lock. npm already had a lockfile.
- **Mitigation:** add automated secret scanning and lockfile audits when CI is introduced.
- **False positive notes:** ignore rules do not protect secrets already tracked; the current and historical scans are therefore still required.

## Open deployment gates

### SEC-006 — Internet-edge protections are not implemented here

- **Rule ID:** FASTAPI-LIMITS-001 / FASTAPI-PROXY-001 / REACT-CSP-001 / REACT-HEADERS-001
- **Severity:** High if the application is exposed directly to the Internet; not a blocker for publishing source
- **Location:** `README.md:74-76`, `specs/002-architecture-foundation/open-decisions.md:47-62`
- **Evidence:** there is no approved deployment configuration implementing request-body limits, login rate limiting, forwarded-header trust, static frontend CSP/headers, runtime secret delivery or monitoring.
- **Impact:** direct exposure could permit credential brute force, resource exhaustion, proxy-header spoofing or weaker browser isolation.
- **Fix:** approve and implement the deployment/network/observability decisions, then test headers and limits at the public URL.
- **Mitigation:** keep the application local or behind a non-public route until that work is complete. The repository itself may be public.
- **False positive notes:** controls may exist outside this repository; they must be verified at runtime rather than assumed.

### SEC-007 — Demo identity is not production authentication

- **Rule ID:** FASTAPI-AUTH-003 / AUTH-DESIGN-001
- **Severity:** Medium if reused outside the demonstration boundary
- **Location:** `backend/app/security.py:27-40`, `specs/002-architecture-foundation/open-decisions.md:45`, `specs/002-architecture-foundation/open-decisions.md:60`
- **Evidence:** all fictional accounts intentionally authenticate against one runtime-supplied demo password and sessions are held in process memory.
- **Impact:** using this implementation for real users would provide neither per-user credentials nor durable, multi-instance session and revocation behavior.
- **Fix:** replace it with the approved identity provider and production session design before using real identities.
- **Mitigation:** use only synthetic identities, a local-only password and non-production data; never reuse a real credential as the demo password.
- **False positive notes:** this is an explicit prototype boundary, not a claim that plaintext passwords are stored. The runtime password is hashed with the recommended password hasher and is absent from the repository.

## Privacy and ownership checks

- The Git remote URL exposes the expected public account/repository name.
- Git history contains one author identity and an Outlook email address. This metadata will be public; the repository owner should confirm that this is intentional.
- No license file is present. Public visibility permits viewing and forking through the hosting platform but does not grant a general open-source license. Choose a license only if reuse rights are intended.
- The tracked ZIP is an earlier static prototype. It contains no detected secret or network identifiers; its DOM construction uses only bundled fictional data, not network or URL input.

## Verification evidence

- Secret-format scan: current worktree, all five reachable commits and the tracked ZIP; no matches for the reviewed private-key and common provider-token formats.
- Address scan: only loopback, package registries and `.example` synthetic identities in the implementation.
- Python dependency audit after remediation: no known vulnerabilities.
- npm audit: 0 vulnerabilities across 68 dependencies.
- Final validation: 19 tests and 2 subtests passed; frontend typecheck/build passed; deterministic data validation passed with its expected fingerprint.
