# Security Baseline

The template sets conservative defaults: typed settings, redacted secrets,
safe error handling, bounded readiness checks, correlation IDs, non-root
containers, read-only runtime filesystems, lockfiles, and CI security scans.

Before adding external integrations, define least-privilege credentials,
egress controls, input validation, authorization, audit requirements, and
failure behavior. The capability deny set forbids raw SQL, filesystem access,
shell/process execution, secret-store access, arbitrary network access, and
external side effects by default. Relax it only through an explicit,
product-specific, tested policy.
