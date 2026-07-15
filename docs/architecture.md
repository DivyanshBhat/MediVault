# MediVault System Architecture

## Overview

MediVault is a full-stack web application that enables users to securely store, organize, and manage their family's medical records from a single platform.

The application follows a modern client-server architecture where the frontend, backend, database, and file storage are separated into independent components. This modular approach improves maintainability, scalability, and security.


# Technology Stack

## Frontend

* React
* Vite
* HTML
* CSS
* JavaScript

The frontend is responsible for rendering the user interface, collecting user input, and communicating with the backend through HTTP requests.


## Backend

* Node.js
* Express.js

The backend serves as the central layer of the application.

Responsibilities include:

* Processing API requests
* Authentication and authorization
* Business logic
* Input validation
* Database communication
* File upload handling
* Response generation


## Database

* PostgreSQL

PostgreSQL stores all structured application data including:

* User accounts
* Family members (patients)
* Medical record metadata
* Doctors
* Hospitals

Relational database principles are used to maintain data integrity through primary keys, foreign keys, and constraints.


## File Storage

* AWS S3

Medical reports and profile pictures are stored in Amazon S3 instead of the database.

The PostgreSQL database stores only the metadata required to locate each file, such as:

* S3 object key
* File name
* File size
* MIME type
* Upload timestamp

This approach keeps the database lightweight while allowing efficient storage of large files.


## Authentication

* JSON Web Tokens (JWT)

After a successful login, the backend generates a JWT.

The client stores this token and includes it with future requests to access protected resources.

Passwords are never stored in plain text. They will be securely hashed before being saved to the database.


## Validation

* Zod

All incoming request data will be validated before it reaches the database.

Validation helps:

* Prevent invalid input
* Improve security
* Return meaningful error messages
* Maintain data consistency


# High-Level Request Flow

A typical request follows this sequence:

```text
User
   ↓
React Frontend
   ↓
Express Backend
   ↓
Authentication & Validation
   ↓
PostgreSQL Database
   ↓
Response
   ↓
React Frontend
```


# File Upload Flow

When a user uploads a medical report:

```text
User
   ↓
React Frontend
   ↓
Express Backend
   ↓
AWS S3
   ↓
Store File Metadata in PostgreSQL
   ↓
Success Response
```

The actual file is stored in AWS S3, while PostgreSQL stores only its metadata.


# Database Architecture

The application is based on five core entities:

* Users
* Patients
* MedicalRecords
* Doctors
* Hospitals

Relationships between these entities are documented in the Entity Relationship Diagram (ERD).


# Project Structure

```text
MediVault/
│
├── medivault-frontend/
├── medivault-backend/
├── docs/
│   ├── architecture.md
│   ├── database-design.md
│   └── er-diagram.png
│
├── README.md
├── LICENSE
└── .gitignore
```


# Design Principles

The architecture has been designed around the following principles:

* Separation of concerns
* Modular development
* Relational database design
* Scalability
* Maintainability
* Security by design
* Incremental feature development

# Planned Future Enhancements

Future versions of MediVault may include:

* AI-powered prescription OCR
* Appointment scheduling
* Medication reminders
* Doctor portal
* Hospital portal
* Multi-user patient sharing
* Role-based access control
* Audit logging
* UUID-based identifiers
* Mobile application

# Conclusion

The MediVault architecture is designed to provide a scalable, secure, and maintainable foundation for managing family medical records. By separating responsibilities across the frontend, backend, database, and cloud storage, the application can evolve with future requirements while maintaining clean system design.
