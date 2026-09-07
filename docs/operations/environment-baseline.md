# NOMAD Ops — Sanitized Deployment Baseline

**Captured:** 2026-09-06
**Classification:** public portfolio summary
**Purpose:** record the deployment constraints learned from a read-only environment review without publishing host-specific evidence

## Public-safe findings

- An existing edge proxy owns public HTTP and HTTPS ingress and terminates TLS.
- Application containers are discovered through controlled service metadata; exposure is opt-in.
- NOMAD Ops must expose only its intended web edge and keep backend, simulator and storage traffic on an isolated internal network.
- Existing workloads share the host, so routine NOMAD Ops changes must not restart or reconfigure unrelated services.
- Runtime credentials, hostnames, addresses and provider configuration must be supplied outside the repository.
- Internal health checks must pass before public routing is enabled; route, logs and resource use must be verified afterward.

## Deliberately excluded from the public repository

The private review evidence contains operational details that are unnecessary for evaluating this project and could aid infrastructure reconnaissance. The public version therefore excludes:

- hostnames, addresses, domains and account identifiers;
- unrelated service and project names;
- exact host capacity, utilization and process state;
- live container, network and proxy identifiers;
- certificate, DNS and provider configuration;
- command output and any credential-bearing configuration.

## Change safety rules

1. Capture a read-only snapshot before an infrastructure change.
2. Validate deployment configuration before applying it.
3. Build and test images before attaching public routing.
4. Change one layer at a time.
5. Do not restart shared or unrelated services during routine deployment.
6. Verify health internally before enabling a route.
7. Verify the public route, logs and resource use afterward.
8. Record affected services, validation, outcome and rollback method in the private operations log.
9. Keep credentials and host-specific evidence out of commits, issues, pull requests and CI logs.
