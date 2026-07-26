# Overview

This repository provides an operational foundation for a new backend service.
It deliberately starts with no product API beyond health and readiness checks.
Add domain behavior only after documenting its requirements, data boundaries,
and acceptance tests.

The template supports a modular monolith first. Keep business rules in the
domain layer and isolate persistence, external APIs, cache, telemetry, and
model providers in infrastructure adapters.
