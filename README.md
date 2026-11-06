# MediVault

### Your family's complete medical history. One tap away.

MediVault is a secure family medical-record management platform designed to help individuals and families store, organize, manage, and access their medical records from one centralized location.
From prescriptions and diagnostic reports to medical histories, MediVault aims to make healthcare information accessible, organized, and secure.

> **Project Status:** Under Development — MediVault 2.0 (Architecture Rebuild)

---

## Project Overview

Managing medical records across multiple family members can become difficult. Documents get misplaced, medical histories become fragmented, and accessing older reports can be inconvenient.
MediVault aims to solve this problem by providing a centralized platform where families can securely manage their medical information.

### Core Objectives

- Centralized medical-record management.
- Individual patient profiles for family members.
- Secure document uploads and storage.
- Organized medical history.
- Family-based access and permissions.
- Scalable architecture for future enhancements.

---

## Planned Features

- **User Authentication:** Secure registration, login, and account management.
- **Family Management:** Create and manage family accounts.
- **Patient Profiles:** Maintain individual medical profiles for family members.
- **Medical Records:** Upload, organize, view, and manage medical documents.
- **Document Storage:** Secure cloud-based storage for prescriptions, reports, and other files.
- **Access Control:** Ensure users can only access records they are authorized to view.
- **Subscription Management:** Free and premium plans with different patient limits.
- **Audit Logs:** Track important actions performed within the platform.

---

## Technology Stack

MediVault follows a modern full-stack architecture, using different technologies where they provide the most value.
| Layer | Technology |
|---|---|
| Frontend | React + TypeScript |
| Build Tool | Vite |
| Styling | Tailwind CSS |
| UI Components | shadcn/ui |
| Routing | React Router |
| API State Management | TanStack Query |
| Form Validation | React Hook Form + Zod |
| Backend | Python + FastAPI |
| Backend Validation | Pydantic |
| ORM | SQLAlchemy |
| Database | PostgreSQL |
| Database Migrations | Alembic |
| Authentication | JWT + secure refresh-token flow |
| Password Hashing | Argon2 |
| File Storage | AWS S3 |
| Caching | Redis (planned) |
| Background Processing | Celery (planned) |
| Containerization | Docker |
| Testing | Pytest + frontend testing tools |
| Version Control | Git + GitHub |

---

## Architecture

MediVault uses a frontend-backend separation architecture.
MEDIVAULT
|
React + TypeScript
|
HTTP / API
|
Python + FastAPI
|
-----------------------
| | |
PostgreSQL AWS S3 Redis
| | (Planned)
User Data Documents
Family Reports
Patients Prescriptions
Records

### Frontend

Responsible for the user interface, dashboards, patient profiles, forms, and document management.

### Backend

FastAPI handles application logic, authentication, authorization, data validation, and communication with external services.

### Database

PostgreSQL stores structured application data, including users, families, patients, medical records, and subscriptions.

### Cloud Storage

## AWS S3 stores medical documents separately from the relational database.

## Project Structure

MediVault/
│
├── docs/
│ ├── architecture.md
│ ├── database-design.md
│ ├── er-diagram.png
│ └── roadmap.md
│
├── medivault-frontend/
│
├── medivault-backend/
│
├── .gitignore
├── LICENSE
├── README.md
└── MediVault.code-workspace
The frontend and backend will be developed and maintained independently within the same repository.

---

## Security Considerations

Because MediVault handles sensitive medical information, security is a core architectural requirement.
Planned security measures include:

- Secure password hashing.
- Short-lived access tokens and protected refresh tokens.
- Family-level authorization and data isolation.
- Private cloud storage.
- Time-limited document access links.
- Input and file validation.
- Audit logging.
- Secure HTTPS communication.
- Database backups and recovery procedures.

---

## Development Roadmap

| Phase | Description                                | Status      |
| ----- | ------------------------------------------ | ----------- |
| 1     | Architecture and technology selection      | Completed   |
| 2     | Repository restructuring and documentation | In Progress |
| 3     | Backend foundation and database setup      | Planned     |
| 4     | Authentication and authorization           | Planned     |
| 5     | Family and patient management              | Planned     |
| 6     | Medical-record management                  | Planned     |
| 7     | Cloud storage integration                  | Planned     |
| 8     | Security and testing                       | Planned     |
| 9     | Subscription management                    | Planned     |
| 10    | Deployment and production readiness        | Planned     |

---

## Future Possibilities

Potential future enhancements include:

- Medical document categorization.
- OCR-based document text extraction.
- Search across medical records.
- Automated medical-record summaries.
- Family health timelines.
- Appointment and medication reminders.
  These are future possibilities, not currently implemented features.

---

## Development

MediVault is being rebuilt using a modern full-stack architecture.
The development process emphasizes:

- Modular and maintainable code.
- Clear separation of frontend and backend responsibilities.
- Secure data handling.
- Database consistency.
- Automated testing.
- Version control and documentation.

---

## Project Information

**Project:** MediVault  
**Version:** 2.0 (Architecture Rebuild)  
**Category:** Full-Stack Web Application  
**Repository:** [GitHub - MediVault](https://github.com/DivyanshBhat/MediVault)

---

_Building a simpler, more organized way to manage family healthcare information._
