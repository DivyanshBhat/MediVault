# MediVault Development Roadmap

## Project vision

MediVault is a secure family medical-record management platform.

> Your family's complete medical history. One tap away.

The goal is to build a working full-stack application while learning and applying sound software-engineering practices. This roadmap distinguishes completed planning from features that have not yet been implemented.

## Project status

- Repository and initial documentation exist.
- The React + TypeScript frontend and Python + FastAPI backend are the selected architecture.
- PostgreSQL schema design is documented.
- Backend and frontend implementation have not yet been marked complete.

---

## Phase 0 — Repository and development environment

- [x] GitHub repository created.
- [x] Git initialized and initial files committed.
- [x] README and LICENSE added.
- [x] `.gitignore` configured.
- [x] Define the Python backend project configuration and dependency groups.
- [x] Add the initial FastAPI application entry point and health-check endpoint.
- [x] Add backend setup instructions and test-directory placeholder.
- [ ] Confirm local Python version and virtual-environment workflow.
- [ ] Confirm PostgreSQL installation and local connection.
- [ ] Set up frontend tooling when frontend work begins.
- [ ] Add environment-variable examples without committing secrets.

## Phase 1 — Architecture and database design

- [x] Define the application purpose and core capabilities.
- [x] Select React + TypeScript + Vite for the frontend.
- [x] Select Python + FastAPI for the backend.
- [x] Select PostgreSQL, SQLAlchemy 2, and Alembic.
- [x] Identify core entities and relationships.
- [x] Plan UUID identifiers and soft deletion.
- [x] Document family-level membership and access control.
- [x] Create the ER diagram and keep its editable DBML source in the repository.
- [x] Document the composite family/patient integrity constraint in the schema and diagram.
- [ ] Validate the DBML in dbdiagram.io and export/verify the final diagram rendering.

## Phase 2 — SQL and PostgreSQL fundamentals (next)

### Learn

- [ ] Relational database concepts and PostgreSQL basics.
- [ ] SQL data types, including UUID, VARCHAR, DATE, TIMESTAMPTZ, BOOLEAN, BIGINT, and JSONB.
- [ ] CREATE DATABASE and CREATE TABLE.
- [ ] Primary keys and foreign keys.
- [ ] NOT NULL, UNIQUE, CHECK, and DEFAULT constraints.
- [ ] INSERT, SELECT, UPDATE, and DELETE.
- [ ] WHERE, ORDER BY, LIMIT, and pagination basics.
- [ ] JOIN operations.
- [ ] GROUP BY and aggregate functions.
- [ ] Index fundamentals and query plans.
- [ ] Transactions and isolation basics.

### Apply to MediVault

- [ ] Create the local `medivault` database.
- [ ] Create the initial schema in a development database.
- [ ] Insert and query sample, non-sensitive test data.
- [ ] Verify constraints and relationships.

## Phase 3 — Python and FastAPI backend foundation

The repository currently contains only a minimal FastAPI starter and health-check endpoint. The remaining tasks below are still pending.

- [ ] Create a Python virtual environment.
- [x] Create the initial FastAPI application entry point (health check only).
- [ ] Add configuration and environment-variable handling.
- [ ] Connect FastAPI to PostgreSQL using SQLAlchemy 2.
- [ ] Configure Alembic migrations.
- [x] Add a starter health-check endpoint.
- [ ] Establish a consistent API response and error-handling approach.
- [x] Add Pytest, an initial test structure, and a health-check test.
- [ ] Organize the backend into modules without unnecessary abstractions.

## Phase 4 — Authentication and authorization

- [ ] Implement registration and login.
- [ ] Hash passwords using Argon2.
- [ ] Implement short-lived access tokens.
- [ ] Design and persist refresh-token/session records before implementing refresh-token rotation.
- [ ] Store refresh-token secrets hashed at rest.
- [ ] Implement refresh, rotation, logout, and token-reuse handling.
- [ ] Configure secure HttpOnly cookies for browser refresh tokens.
- [ ] Add authentication dependencies and protected endpoints.
- [ ] Add rate limiting for sensitive authentication routes.
- [ ] Test authentication failure and authorization boundaries.

## Phase 5 — Families, memberships, and patients

- [ ] Create family workspaces.
- [ ] Add the creator as the initial family owner.
- [ ] Implement family membership and role checks.
- [ ] Implement family invitations and invitation acceptance.
- [ ] Create and update patient profiles.
- [ ] Implement soft deletion and ordinary-query filtering.
- [ ] Enforce the free-plan limit of three active patients per family.
- [ ] Add transaction-safe checks for patient limits.
- [ ] Test that users cannot access another family's data.

## Phase 6 — Medical records and private file storage

- [ ] Implement medical-record metadata endpoints.
- [ ] Validate that each record's patient and family match.
- [ ] Configure a private AWS S3 bucket and least-privilege credentials.
- [ ] Generate server-controlled object keys.
- [ ] Implement short-lived pre-signed upload URLs.
- [ ] Verify uploaded objects before persisting record metadata.
- [ ] Implement authorized pre-signed download URLs.
- [ ] Validate file size and permitted content types.
- [ ] Handle failed uploads, orphaned objects, and soft-deleted records.
- [ ] Add audit events for sensitive record operations.

## Phase 7 — Frontend foundation and API integration

- [ ] Initialize React + TypeScript + Vite.
- [ ] Configure styling and reusable UI components.
- [ ] Set up routing.
- [ ] Create registration and login screens.
- [ ] Implement authenticated application layout.
- [ ] Build family and patient management screens.
- [ ] Build medical-record listing and detail screens.
- [ ] Integrate API calls and server-state handling.
- [ ] Implement upload and download flows.
- [ ] Add loading, empty, validation, and error states.

## Phase 8 — Subscriptions and product rules

- [ ] Implement the default free family subscription.
- [ ] Enforce three active patient profiles on the free plan.
- [ ] Define premium-plan behavior and unlimited patient profiles.
- [ ] Decide on a payment provider before implementing billing.
- [ ] Add payment-provider integration only after core workflows are stable.
- [ ] Test subscription changes and limit enforcement.

## Phase 9 — Security, testing, and hardening

- [ ] Test family and patient authorization at API level.
- [ ] Test cross-family access attempts.
- [ ] Test file-upload and download authorization.
- [ ] Test input validation and error handling.
- [ ] Review secret handling and logging.
- [ ] Add database backup and restoration procedures.
- [ ] Review soft-delete and retention behavior.
- [ ] Add frontend and end-to-end tests.
- [ ] Add CI checks with GitHub Actions.

## Phase 10 — Deployment and production readiness

- [ ] Containerize the services where appropriate.
- [ ] Choose hosting for frontend and backend.
- [ ] Provision production PostgreSQL.
- [ ] Configure private S3 storage and IAM permissions.
- [ ] Configure production secrets and environment variables.
- [ ] Configure HTTPS, domains, and CORS.
- [ ] Run database migrations safely.
- [ ] Verify backups, monitoring, and error reporting.
- [ ] Complete production smoke and security checks.

## Later — Future enhancements

- [ ] OCR-based medical-document extraction.
- [ ] Search across medical records.
- [ ] Medical-history summaries.
- [ ] Medication and appointment reminders.
- [ ] Expanded family-sharing permissions.
- [ ] Doctor or hospital portals.
- [ ] Mobile application.
- [ ] Redis and Celery if background jobs or caching become necessary.

These are future possibilities, not part of the initial implementation scope.

---

## Guiding principles

- Learn the concepts before implementing them.
- Design before coding, but avoid designing speculative features too early.
- Keep the backend authoritative for authorization and validation.
- Use migrations for database changes.
- Write tests as features are introduced.
- Make small, understandable Git commits.
- Do not commit credentials, private medical information, or production data.
- Update this roadmap when actual progress changes.

## Project goal

Build a secure, maintainable family medical-record platform while developing a practical understanding of full-stack engineering, databases, APIs, authentication, cloud storage, testing, and deployment.
