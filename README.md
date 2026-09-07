# NOMAD Ops

NOMAD Ops is a security-first operations assistant prototype for a fictional manufacturing group. It demonstrates how an enterprise assistant can retrieve authorized context and perform controlled, auditable actions without giving an AI model authority over identity, policy or systems of record.

All organizations, people, email addresses, incidents, assets and operational records in this repository are synthetic.

## Current slice

The implemented vertical slice includes:

- a FastAPI backend with local demo authentication, server-side sessions and deterministic authorization;
- a React and TypeScript interface for authenticated knowledge and alert views;
- simulated ITSM, document, HR, ERP, plant and monitoring services;
- deterministic synthetic data with six cross-system scenarios;
- automated tests for login, expiry, CSRF, policy boundaries, approvals, idempotency and failure handling.

AI, RAG, Qdrant and n8n execution are intentionally outside this first slice.

## Security design

The browser receives an opaque `HttpOnly` session cookie. Identity context, permissions and CSRF state remain server-side. The backend enforces role and object scope before calling the simulator; the frontend never acts as the authorization boundary. Production mode requires an explicit host allowlist and disables interactive API documentation.

See [the publication-readiness review](docs/security/publication-readiness.md) for the repository audit and the controls still required before exposing the application itself to the public Internet.

## Run locally

Python 3.12 and Node.js with npm are required.

```bash
python3 -m venv .venv
.venv/bin/pip install -r backend/requirements.lock
export NOMAD_DEMO_PASSWORD='choose-a-local-demo-password'
export NOMAD_COOKIE_SECURE=false
.venv/bin/uvicorn backend.app.main:app --reload
```

In another terminal:

```bash
cd frontend
npm ci
npm run dev
```

The default login email shown by the UI is fictional. Use the local password you exported above.

## Verify

```bash
PYTHONDONTWRITEBYTECODE=1 .venv/bin/pytest -q -p no:cacheprovider
cd frontend
npm run typecheck
npm run build
npm audit
```

Regenerate and validate the synthetic dataset with:

```bash
python3 scripts/generate_synthetic_data.py
```

## Documentation map

- `specs/000-product/`: product intent, scope, principles and success criteria
- `specs/001-system-context/`: actors, trust boundaries and integration constraints
- `specs/002-architecture-foundation/`: components, data responsibilities and request flows
- `specs/003-synthetic-data/`: deterministic data model and scenarios
- `specs/004-simulated-enterprise-services/`: simulator contracts and failure modes
- `specs/005-local-identity-and-authorization/`: demo identity and policy
- `specs/006-application-stack/`: approved FastAPI and React stack
- `docs/adr/`: architecture decision records

## Deployment boundary

This repository is safe to review publicly, but the application is not approved for direct Internet exposure. A real deployment still needs an edge proxy with TLS, request-size limits, rate limiting, strict forwarded-header trust, runtime secret injection, monitoring and the deployment decisions recorded as open in the architecture register.
