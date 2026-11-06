# MediVault — System Architecture

## 1. Overview

MediVault is a secure family medical-record management platform designed to help individuals and families store, organize, manage, and access medical information from a centralized application.
The system allows users to maintain individual patient profiles, upload medical documents, organize medical histories, and securely share access with authorized family members.
MediVault follows a **client-server architecture** with a separate frontend, backend, relational database, and cloud-based file storage.
The application will initially follow a **modular monolith architecture**, keeping the backend as one deployable application with clearly separated modules.

### Architectural Goals

- Security and privacy of medical information.
- Separation of frontend and backend responsibilities.
- Maintainable and modular code.
- Reliable relational data management.
- Scalable document storage.
- Family-based access control.
- Extensibility for future features.

---

# 2. Technology Stack

## 2.1 Frontend

**Primary technologies: React + TypeScript + Vite**
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
| Zod | Frontend data validation |
The frontend is responsible for:

- Rendering application pages and components.
- User interactions and navigation.
- Form handling and client-side validation.
- Communicating with backend APIs.
- Displaying patient profiles and medical records.
- Managing loading, error, and success states.
  The frontend must not be treated as a trusted security boundary. All important authorization and validation checks must also be performed by the backend.

## 2.2 Backend

**Primary technologies: Python + FastAPI**
| Technology | Responsibility |
|---|---|
| Python | Backend programming language |
| FastAPI | REST API framework |
| Pydantic | Request and response validation |
| SQLAlchemy 2 | Database ORM |
| Alembic | Database migrations |
| PyJWT | JWT handling |
| pwdlib | Password hashing integration |
| Pytest | Backend testing |
The backend acts as the central application layer.
Responsibilities include:

- Authentication and authorization.
- Business logic.
- Request processing.
- Input validation.
- Database operations.
- Medical-record management.
- Family and patient management.
- Secure file-upload authorization.
- Subscription and plan enforcement.
- Audit logging.
  The backend will be organized into independent application modules while remaining part of a single deployable service.

## 2.3 Database

**Database: PostgreSQL**
PostgreSQL stores structured application information.
Primary data includes:

- User accounts.
- Families.
- Family memberships.
- Patient profiles.
- Medical records.
- Subscription information.
- Audit logs.
  SQLAlchemy will handle database interactions, while Alembic will manage schema migrations.
  Relational integrity will be maintained using:
- Primary keys.
- Foreign keys.
- Unique constraints.
- Check constraints.
- Database indexes.
  UUID identifiers will be used for application entities from the initial implementation.

## 2.4 File Storage

**Storage: Amazon Web Services S3**
AWS S3 will store uploaded medical documents separately from the relational database.
Supported document types may include:

- PDF medical reports.
- Prescriptions.
- Laboratory reports.
- Medical images.
- Other permitted healthcare documents.
  PostgreSQL will store document metadata rather than the actual file contents.
  Metadata includes:
- Document ID.
- Patient ID.
- Original file name.
- S3 object key.
- MIME type.
- File size.
- Document category.
- Upload timestamp.
  Medical documents will be stored in private S3 buckets.
  Access will be provided through short-lived, authorized pre-signed URLs.

## 2.5 Authentication and Security

Authentication will use a token-based approach.
Planned technologies:

- JWT access tokens.
- Refresh-token rotation.
- Argon2 password hashing.
- Secure HttpOnly cookies for refresh tokens.
- Backend-enforced authorization policies.
  The backend will verify the identity of the user and their permissions before allowing access to protected resources.
  Family-level data isolation is a core security requirement.

## 2.6 Infrastructure and Supporting Technologies

| Technology     | Responsibility                 | Priority         |
| -------------- | ------------------------------ | ---------------- |
| Docker         | Containerization               | Initial setup    |
| Redis          | Caching and task queue support | Later            |
| Celery         | Background processing          | Later            |
| Git            | Version control                | Initial setup    |
| GitHub         | Repository hosting             | Initial setup    |
| GitHub Actions | CI/CD automation               | Later            |
| AWS            | Cloud infrastructure           | Deployment stage |

Redis and Celery will be introduced when background processing or caching becomes necessary.
They are not required for the initial application foundation.

---

# 3. High-Level System Architecture

                  USER
                    |
                    |
            React + TypeScript
                    |
                    |
                HTTP / HTTPS
                    |
                    |
             Python + FastAPI
                    |
          -----------------------
          |          |          |
          |          |          |
      PostgreSQL   AWS S3    Redis
          |          |       (Later)
          |          |
      User Data   Medical Files
      Families    Prescriptions
      Patients    Reports
      Records
          |
          |
      Audit Logs

The frontend communicates with the backend through REST APIs.
The backend handles application logic and communicates with PostgreSQL and AWS S3.

---

# 4. Request Lifecycle

A typical authenticated request follows this sequence:
User
|
v
React Frontend
|
v
HTTP Request
|
v
FastAPI Backend
|
v
Authentication
|
v
Authorization
|
v
Request Validation
|
v
Business Logic
|
v
SQLAlchemy ORM
|
v
PostgreSQL
|
v
Response
|
v
React Frontend
Every protected backend operation must verify that the authenticated user is authorized to perform the requested action.

---

# 5. Medical Document Upload Architecture

Medical documents will be uploaded directly from the frontend to AWS S3 using short-lived pre-signed URLs.
This avoids routing large file contents through the application server.

### Upload Flow

User selects document
|
v
React Frontend
|
v
FastAPI Backend
|
v
Authenticate user
|
v
Verify patient access
|
v
Validate upload request
|
v
Generate pre-signed URL
|
v
Frontend receives upload URL
|
v
Upload directly to AWS S3
|
v
Backend verifies uploaded object
|
v
Save document metadata
|
v
PostgreSQL

### Document Access Flow

User requests document
|
v
FastAPI Backend
|
v
Authenticate user
|
v
Verify family and patient permissions
|
v
Generate short-lived access URL
|
v
Frontend accesses document
The S3 bucket must remain private. Public object access will not be permitted.

---

# 6. Database Architecture

The application will use a relational database model.
The initial core entities are:
| Entity | Responsibility |
|---|---|
| Users | User accounts and authentication |
| Families | Family-level accounts |
| FamilyMemberships | User-family relationships and roles |
| Patients | Individual medical profiles |
| MedicalRecords | Medical document metadata |
| Subscriptions | Free and premium plan information |
| AuditLogs | Security and activity history |
Additional entities may be introduced as the application evolves.
The complete schema and relationships will be documented separately in `database-design.md`.

---

# 7. Backend Module Architecture

The backend will follow a modular structure.
Initial modules:

- **Authentication:** Registration, login, refresh tokens and logout.
- **Users:** User profiles and account management.
- **Families:** Family creation and membership management.
- **Patients:** Patient profiles and associated information.
- **Medical Records:** Document metadata and record management.
- **Storage:** AWS S3 integration and upload authorization.
- **Subscriptions:** Plan management and usage limits.
- **Audit:** Logging important security-sensitive actions.
  Modules will communicate through defined service interfaces rather than relying on tightly coupled code.

---

# 8. Security Architecture

Security is a fundamental requirement because MediVault handles sensitive medical information.
Planned security measures include:

### Authentication

- Secure password hashing.
- Short-lived access tokens.
- Refresh-token rotation.
- Protected authentication endpoints.

### Authorization

- Family-level data isolation.
- Role-based access control.
- Patient-level permission checks.
- Backend-enforced resource ownership checks.

### File Security

- Private S3 buckets.
- Short-lived pre-signed URLs.
- File type and size validation.
- Randomized storage object keys.
- No public document URLs.

### Database Security

- Parameterized database operations through the ORM.
- Restricted database credentials.
- Foreign key constraints.
- Automated backups.

### Application Security

- HTTPS communication.
- Secure secret management.
- Rate limiting.
- Audit logging.
- Input validation.
  Security controls will be tested throughout development.

---

# 9. Project Structure

MediVault/
|
|-- docs/
| |-- architecture.md
| |-- database-design.md
| |-- er-diagram.png
| |-- roadmap.md
|
|-- medivault-frontend/
| |-- public/
| |-- src/
| | |-- assets/
| | |-- components/
| | |-- pages/
| | |-- layouts/
| | |-- hooks/
| | |-- services/
| | |-- context/
| | |-- types/
| | |-- utils/
| |
| |-- package.json
| |-- tsconfig.json
|
|-- medivault-backend/
| |-- app/
| | |-- api/
| | |-- core/
| | |-- models/
| | |-- schemas/
| | |-- services/
| | |-- repositories/
| | |-- middleware/
| | |-- main.py
| |
| |-- migrations/
| |-- tests/
| |-- requirements.txt
|
|-- .gitignore
|-- README.md
|-- LICENSE
|-- MediVault.code-workspace
This structure may evolve as the application grows.

---

# 10. Design Principles

MediVault follows these architectural principles:

1. Separation of concerns.
2. Modular monolith architecture.
3. Secure-by-design development.
4. Relational data integrity.
5. Least-privilege access control.
6. Maintainability and readability.
7. Incremental development.
8. Automated testing.
9. Independent frontend and backend development.
10. Scalable cloud-based document storage.

---

# 11. Planned Future Enhancements

Potential future improvements include:

- OCR-based medical document extraction.
- AI-assisted document categorization.
- Medical history summaries.
- Medication reminders.
- Appointment management.
- Doctor and hospital portals.
- Advanced family-sharing permissions.
- Mobile application.
- Advanced search across medical records.
  These features will be evaluated after the core platform is implemented.

---

# 12. Conclusion

MediVault is designed as a secure and modular family medical-record management platform.
By combining React and TypeScript for the frontend, Python and FastAPI for the backend, PostgreSQL for structured data, and AWS S3 for document storage, the architecture aims to provide a maintainable foundation for future development.
The initial implementation will prioritize authentication, family management, patient profiles, medical-record management, and security.
The architecture will evolve incrementally as new requirements are introduced.
