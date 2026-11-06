# MediVault — System Architecture

## 1. Overview

MediVault is a family medical-record management platform for organizing patient profiles and medical documents in one place. It uses a **client-server architecture** with a React frontend, a Python/FastAPI backend, PostgreSQL for structured data, and private object storage for uploaded documents.

The backend will begin as a **modular monolith**: one deployable FastAPI application divided into modules with clear responsibilities. Redis, Celery, and additional infrastructure will be introduced only when the product needs them.

### Architectural goals

- Protect sensitive personal and medical information.
- Enforce family-level data isolation on every protected operation.
- Keep frontend, backend, database, and file storage responsibilities separate.
- Preserve relational integrity and maintainable code.
- Build incrementally without prematurely introducing distributed services.

## 2. Technology stack

### 2.1 Frontend

**React + TypeScript + Vite**

| Technology | Responsibility |
|---|---|
| React | Component-based user interface |
| TypeScript | Static type checking |
| Vite | Development server and build tooling |
| Tailwind CSS | Styling and responsive layouts |
| shadcn/ui | Reusable interface components |
| React Router | Client-side routing |
| TanStack Query | Server-state management and API caching |
| React Hook Form | Form management |
| Zod | Frontend form and data validation |

The frontend handles pages, navigation, forms, user interactions, and API communication. Frontend validation improves usability, but it is not a security boundary. The backend must repeat all security-relevant validation and authorization checks.

### 2.2 Backend

**Python + FastAPI**

| Technology | Responsibility |
|---|---|
| Python | Backend programming language |
| FastAPI | REST API framework |
| Pydantic | Request and response validation |
| SQLAlchemy 2 | Database ORM |
| Alembic | Database schema migrations |
| PyJWT | JWT encoding and verification |
| pwdlib with Argon2 | Password hashing |
| Pytest | Backend testing |

The backend is responsible for authentication, authorization, business rules, request validation, database operations, file-upload authorization, subscription enforcement, and audit logging.

The application will remain one deployable service initially, with modules such as authentication, users, families, patients, medical records, storage, subscriptions, and audit.

### 2.3 Database

**PostgreSQL**

PostgreSQL stores structured application data, including users, families, memberships, invitations, patient profiles, medical-record metadata, subscriptions, and audit logs.

- SQLAlchemy 2 manages database interactions.
- Alembic manages schema changes through versioned migrations.
- UUIDs are used as identifiers from the initial implementation.
- Foreign keys, unique constraints, check constraints, and indexes enforce data integrity.

The full schema is documented in [database-design.md](database-design.md).

### 2.4 File storage

**Private Amazon S3 bucket**

Medical documents are stored in S3 rather than as binary data in PostgreSQL. The database stores metadata and the S3 object key.

The bucket must remain private. The backend authorizes each upload or download and issues short-lived pre-signed URLs. A pre-signed URL is a temporary bearer credential, so it must not be logged or exposed unnecessarily.

### 2.5 Authentication and security

The planned authentication design includes:

- Argon2 password hashing.
- Short-lived JWT access tokens.
- Refresh-token rotation.
- Refresh tokens stored securely and hashed at rest; session/refresh-token persistence must be included before refresh-token authentication is implemented.
- HttpOnly, Secure, appropriately SameSite-configured cookies for browser refresh-token handling.
- Backend-enforced family membership and role checks.
- Rate limiting and audit logging for sensitive operations.

JWTs and UUIDs do not grant authorization by themselves. The backend must check the user's current permissions for the requested resource.

### 2.6 Infrastructure

| Technology | Responsibility | Introduction |
|---|---|---|
| Git + GitHub | Version control and repository hosting | Initial |
| Docker | Repeatable local and deployment environments | Initial foundation |
| AWS | Cloud infrastructure and S3 storage | File-storage/deployment phase |
| Redis | Caching or task-broker support | Later, if needed |
| Celery | Background jobs | Later, if needed |
| GitHub Actions | CI automation | After tests are established |

Redis and Celery are not prerequisites for the first working backend.

## 3. High-level architecture

```text
                    USER
                      |
                      v
             React + TypeScript
                      |
                 HTTPS / REST
                      |
                      v
              Python + FastAPI
                /     |      \
               v      v       v
          PostgreSQL  AWS S3  Redis
          structured  private (later)
             data     files
```

The frontend communicates with FastAPI over HTTP/HTTPS. FastAPI applies authentication, authorization, validation, and business rules before accessing PostgreSQL or issuing S3 upload/download permissions.

## 4. Authenticated request lifecycle

A typical protected API request follows this sequence:

1. The frontend sends the request with its access credential.
2. FastAPI verifies the credential and identifies the user.
3. The backend loads or verifies the user's relevant family membership and role.
4. The request data is validated with Pydantic.
5. The service layer applies business rules.
6. SQLAlchemy performs the required database operations.
7. The backend returns only data the user is authorized to receive.

Authorization must be enforced on the server for every protected resource. Do not rely on hidden frontend controls or unpredictable identifiers.

## 5. Medical document upload and access

### Upload flow

1. A user selects a document in the frontend.
2. The frontend requests an upload authorization from FastAPI.
3. FastAPI authenticates the user and verifies access to the patient and family.
4. The backend validates permitted file type, size, and metadata.
5. FastAPI creates a short-lived pre-signed upload URL for a server-generated object key.
6. The frontend uploads the file directly to the private S3 bucket.
7. The backend verifies the uploaded object and persists its metadata in PostgreSQL.

The implementation must account for failed uploads and orphaned objects so incomplete uploads do not create misleading medical-record entries.

### Download flow

1. The user requests a medical document.
2. FastAPI authenticates the user.
3. The backend verifies family membership and permission to access the patient and record.
4. FastAPI issues a short-lived pre-signed download URL.
5. The frontend uses that URL to retrieve the private object.

Public S3 object access is not permitted.

## 6. Core data model

| Entity | Responsibility |
|---|---|
| Users | Login accounts and profile information |
| Families | Family workspaces and tenant boundary |
| Family Memberships | User-family relationship and role |
| Family Invitations | Pending and historical invitations |
| Patients | Patient profiles owned by a family |
| Medical Records | Document metadata linked to a patient and family |
| Subscriptions | Family-level plan and billing references |
| Audit Logs | Append-only security and activity history |

A user may belong to multiple families. Each family may have multiple members and patient profiles. The detailed columns, constraints, and relationships are in [database-design.md](database-design.md).

## 7. Backend module layout

The backend will be organized by responsibility. A starting structure is:

```text
medivault-backend/
├── app/
│   ├── api/
│   ├── core/
│   ├── db/
│   ├── models/
│   ├── schemas/
│   ├── services/
│   ├── repositories/
│   ├── modules/
│   └── main.py
├── migrations/
├── tests/
└── pyproject.toml
```

The exact layout can be adjusted during project initialization. Avoid adding empty abstractions before there is a clear use for them.

## 8. Security requirements

### Authentication

- Hash passwords with Argon2; never store plaintext passwords.
- Use short-lived access tokens.
- Rotate refresh tokens and detect reuse.
- Store refresh-token/session secrets hashed at rest.
- Protect refresh-token cookies with HttpOnly, Secure, and appropriate SameSite settings.

### Authorization and tenant isolation

- Verify family membership and role on every protected family resource.
- Check that the patient and medical record belong to the same family.
- Do not treat a UUID as proof of access.
- Apply least-privilege rules to owners, administrators, and members.

### File security

- Keep S3 buckets private.
- Use short-lived pre-signed URLs.
- Generate storage keys on the server; do not trust client-supplied paths.
- Validate file size and content type, and consider content inspection before production.
- Avoid logging pre-signed URLs or document contents.

### Database and application security

- Use parameterized ORM/database operations.
- Keep credentials and secrets outside source control.
- Restrict database and cloud permissions.
- Apply rate limits to sensitive endpoints.
- Keep audit logs free of passwords, tokens, and unnecessary medical details.
- Plan backups, restoration tests, and data-retention procedures.

## 9. Development principles

1. Keep a modular monolith until there is a demonstrated need to split services.
2. Make the backend the authority for access control.
3. Enforce data integrity in PostgreSQL as well as application code.
4. Use Alembic migrations for schema changes.
5. Add automated tests alongside features.
6. Introduce infrastructure only when it solves a current requirement.
7. Keep this document aligned with implemented decisions.

## 10. Future enhancements

Potential later features include OCR, document search, medical-history summaries, reminders, appointment management, expanded sharing permissions, portals, and a mobile application. They are outside the initial implementation scope.
