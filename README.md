# MediVault

### Your family's complete medical history. One tap away.

MediVault is a secure family medical-record management platform designed to help individuals and families store, organize, manage, and access medical information from one centralized application.

> **Project status:** Under development — MediVault 2.0 (architecture rebuild)

---

## Project overview

Medical documents are often scattered across emails, messaging apps, folders, and physical files. MediVault aims to make it easier for families to maintain organized medical histories for every family member in one secure place.

### Core objectives

- Centralized medical-record management.
- Individual patient profiles for family members.
- Secure document uploads and storage.
- Organized medical histories.
- Family-based access control and permissions.
- A maintainable architecture that can grow over time.

## Planned features

- **Authentication:** Registration, login, account management, and secure sessions.
- **Family management:** Create family workspaces and manage memberships.
- **Patient profiles:** Maintain profiles for family members, including people who do not have MediVault accounts.
- **Medical records:** Upload, organize, view, and manage medical documents.
- **Private document storage:** Store reports, prescriptions, and other permitted files securely.
- **Authorization:** Restrict access to family and patient information based on membership and permissions.
- **Subscriptions:** Free and premium plans with different patient limits.
- **Audit logs:** Record important security-sensitive actions.

These are planned capabilities; they should not be interpreted as features that are already implemented.

---

## Technology stack

MediVault uses separate frontend and backend technologies, choosing tools suited to each responsibility.

| Layer | Technology |
|---|---|
| Frontend | React + TypeScript |
| Build tool | Vite |
| Styling | Tailwind CSS |
| UI components | shadcn/ui |
| Routing | React Router |
| API state management | TanStack Query |
| Forms | React Hook Form |
| Frontend validation | Zod |
| Backend language | Python |
| Backend framework | FastAPI |
| Backend validation | Pydantic |
| ORM | SQLAlchemy 2 |
| Database | PostgreSQL |
| Database migrations | Alembic |
| JWT handling | PyJWT |
| Password hashing | pwdlib with Argon2 |
| File storage | Private AWS S3 bucket |
| Caching / task queue | Redis (later, when needed) |
| Background processing | Celery (later, when needed) |
| Containerization | Docker |
| Backend testing | Pytest |
| Version control | Git + GitHub |

---

## System architecture

The application follows a client-server architecture with a modular monolith backend.

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
             /      |       \
            v       v        v
       PostgreSQL  AWS S3   Redis
                    private  (later)
                    storage
```

- **Frontend:** Handles pages, forms, navigation, and user interactions.
- **Backend:** Handles authentication, authorization, validation, business logic, and integrations.
- **PostgreSQL:** Stores structured application data such as users, families, patients, and medical-record metadata.
- **AWS S3:** Stores medical documents separately from the relational database. The bucket will remain private.

The backend is the security boundary. Frontend checks improve usability but never replace backend authorization.

For more detail, see [System Architecture](docs/architecture.md) and [Database Design](docs/database-design.md).

---

## Repository structure

```text
MediVault/
├── docs/
│   ├── architecture.md
│   ├── database-design.md
│   ├── er-diagram.png
│   └── roadmap.md
├── medivault-backend/
├── medivault-frontend/
├── .gitignore
├── LICENSE
├── MediVault.code-workspace
└── README.md
```

The frontend and backend directories are separate applications within the same repository. Their internal structures will be created during their respective setup phases.

---

## Security principles

MediVault is intended to handle sensitive personal and medical information. Security must be considered from the beginning of implementation.

Planned controls include:

- Argon2 password hashing; never store plaintext passwords.
- Short-lived access tokens and protected refresh-token handling.
- Backend-enforced family and patient authorization.
- Private S3 buckets and short-lived pre-signed URLs.
- File type, size, and upload validation.
- Restricted database credentials and parameterized database access.
- Audit logging without storing passwords, tokens, or unnecessary medical details.
- HTTPS, secure secret management, backups, and recovery procedures.

A UUID is an identifier, not an authorization mechanism. Every protected request must verify the user's permissions.

---

## Development roadmap

| Phase | Description | Status |
|---|---|---|
| 0 | Repository and development environment setup | In progress |
| 1 | Architecture and database design documentation | Completed |
| 2 | SQL and PostgreSQL fundamentals | Next |
| 3 | Python and FastAPI backend foundation | Planned |
| 4 | Authentication and authorization | Planned |
| 5 | Family and patient management | Planned |
| 6 | Medical-record management and S3 integration | Planned |
| 7 | Frontend implementation and API integration | Planned |
| 8 | Security, testing, and hardening | Planned |
| 9 | Deployment and production readiness | Planned |
| 10 | Future enhancements | Later |

The detailed task checklist lives in [docs/roadmap.md](docs/roadmap.md).

---

## Future possibilities

Potential enhancements after the core platform is working include:

- OCR-based document text extraction.
- Search across medical records.
- Medical-history summaries.
- Appointment and medication reminders.
- Additional family-sharing permissions.
- Doctor or hospital portals.
- A mobile application.

These are future possibilities, not part of the initial implementation scope.

---

## Development approach

The project will be developed incrementally:

1. Understand the concepts before implementing them.
2. Finalize the design before writing application code.
3. Keep frontend and backend responsibilities separate.
4. Enforce security and data integrity in the backend and database.
5. Write tests as features are introduced.
6. Use Git commits to keep changes small and understandable.
7. Keep documentation aligned with the implementation.

---

## Project information

- **Project:** MediVault
- **Version:** 2.0 (architecture rebuild)
- **Category:** Full-stack web application
- **Repository:** [GitHub — MediVault](https://github.com/DivyanshBhat/MediVault)

---

_Building a simpler, more organized way to manage family healthcare information._
