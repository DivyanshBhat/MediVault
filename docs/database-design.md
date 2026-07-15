# MediVault Database Design

## Overview

MediVault is a secure family medical records management platform designed to help users organize, manage, and access their family's medical history from a single application.

The database is designed using relational database principles to ensure data integrity, scalability, and maintainability. Before writing any SQL, the complete database schema was planned to establish clear relationships between entities and avoid data duplication.


# Why PostgreSQL?

MediVault uses **PostgreSQL** as its primary database because healthcare data is highly structured and contains many relationships between entities.

Reasons for choosing PostgreSQL:

* Supports relational data through tables and foreign keys.
* Ensures data consistency using ACID transactions.
* Excellent support for constraints and data validation.
* Highly scalable and widely used in production applications.
* Strong community support and extensive documentation.


# Database Design Philosophy

The database was designed following these principles:

* One table represents one real-world entity.
* Every table has a primary key.
* Relationships are created using foreign keys.
* Duplicate data should be avoided whenever possible.
* Store references (IDs) instead of repeating information.
* Design the schema before writing SQL.
* Keep the schema simple while allowing future expansion.



# Database Entities

## Users

Stores account information for every registered user.

### Main Attributes

* id
* name
* email
* password_hash
* phone_number
* profile_picture_url
* subscription_plan
* created_at
* updated_at

### Notes

* Email must be unique.
* Passwords are never stored in plain text.
* Profile pictures will be stored in AWS S3, while the database stores only the file reference.
* Every new account starts with the **FREE** subscription plan by default.



## Patients

Stores family members managed by a user.

### Main Attributes

* id
* user_id
* name
* relationship
* date_of_birth
* gender
* blood_group
* height
* weight
* allergies
* created_at
* updated_at

### Notes

* One user can manage multiple patients.
* Age is not stored because it changes over time. Date of birth is stored instead.



## MedicalRecords

Stores metadata for uploaded medical documents.

### Main Attributes

* id
* patient_id
* doctor_id
* hospital_id
* title
* report_type
* record_date
* file_name
* file_size
* mime_type
* s3_key
* uploaded_at
* created_at
* updated_at

### Notes

* Medical files are stored in AWS S3.
* PostgreSQL stores only the metadata required to locate and manage those files.



## Doctors

Stores doctor information referenced by medical records.

### Main Attributes

* id
* hospital_id
* name
* specialization
* qualification
* phone_number
* created_at
* updated_at



## Hospitals

Stores hospital information.

### Main Attributes

* id
* name
* address
* city
* state
* country
* phone_number
* created_at
* updated_at



# Relationships

### Users → Patients

One user can have multiple patients.

Relationship:

**One-to-Many**



### Patients → MedicalRecords

One patient can have multiple medical records.

Relationship:

**One-to-Many**



### Hospitals → Doctors

One hospital can have multiple doctors.

Relationship:

**One-to-Many**



### Doctors → MedicalRecords

A doctor can be associated with multiple medical records.

Relationship:

**One-to-Many**



### Hospitals → MedicalRecords

A hospital can be associated with multiple medical records.

Relationship:

**One-to-Many**



# Business Rules

* Every user starts with the **FREE** plan.
* FREE accounts can manage up to **3 patients**.
* PREMIUM accounts can manage unlimited patients.
* Profile pictures are stored in AWS S3.
* Medical reports are stored in AWS S3.
* PostgreSQL stores only file metadata.
* Passwords are stored as secure hashes, never in plain text.



# Database Design Decisions

Several design decisions were made before implementation:

* Integer primary keys are used for Version 1 to simplify development and learning.
* Foreign keys maintain relationships between tables.
* Data duplication is minimized through normalization.
* Soft deletes are planned to improve user data safety and recovery.
* Constraints such as PRIMARY KEY, FOREIGN KEY, UNIQUE, NOT NULL, CHECK, and DEFAULT will be applied during SQL implementation.



# Future Improvements

Potential improvements for future versions include:

* UUID-based primary keys.
* Shared patients between multiple user accounts.
* Doctor and hospital login portals.
* AI-assisted prescription OCR.
* Appointment management.
* Medication reminders.
* Audit logs.
* Role-based access control.



# Conclusion

The MediVault database has been designed using relational database principles before implementation. This approach ensures that the system remains scalable, maintainable, and suitable for future feature expansion while keeping the Version 1 architecture simple and easy to understand.
