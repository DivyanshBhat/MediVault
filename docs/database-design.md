# MediVault — Database Design

## 1. Overview

MediVault uses PostgreSQL as its primary relational database.
The database is designed around a family-based multi-tenant architecture. A user can create multiple families or belong to multiple families through invitations. Each family has its own patient profiles, medical records, subscription, and activity history.
The database uses UUID primary keys, foreign-key relationships, appropriate indexes, and timestamps.

### Design principles

- Family-based data isolation.
- Support multiple families per user.
- Role-based family membership.
- UUID primary keys.
- Referential integrity through foreign keys.
- Soft deletion for recoverable user data.
- Immutable audit history.
- Private medical file storage through AWS S3.
- Subscription management at the family level.

---

## 2. Entity Relationship Overview

The initial database contains the following entities:

1. Users
2. Families
3. Family Memberships
4. Family Invitations
5. Patients
6. Medical Records
7. Subscriptions
8. Audit Logs

### Relationships

- A user can belong to multiple families.
- A family can have multiple users.
- A family can contain multiple patient profiles.
- A patient can have multiple medical records.
- A family has one subscription.
- A family can have multiple audit log entries.
- A family can have multiple pending invitations.
  The many-to-many relationship between users and families is handled through the `family_memberships` table.

---

## 3. Table Definitions

### 3.1 Users

Stores registered MediVault accounts.
| Column | Type | Constraints |
|---|---|---|
| id | UUID | Primary Key |
| full_name | VARCHAR(100) | NOT NULL |
| email | VARCHAR(255) | UNIQUE, NOT NULL |
| password_hash | VARCHAR(255) | NOT NULL |
| is_active | BOOLEAN | DEFAULT TRUE |
| email_verified_at | TIMESTAMPTZ | NULL |
| created_at | TIMESTAMPTZ | NOT NULL |
| updated_at | TIMESTAMPTZ | NOT NULL |
| deleted_at | TIMESTAMPTZ | NULL |
**Purpose:**

- Stores account information.
- Supports authentication.
- Allows account deactivation.
- Connects users to families through memberships.
  Passwords must always be stored as secure password hashes, never as plain text.

### 3.2 Families

Represents a family workspace.
| Column | Type | Constraints |
|---|---|---|
| id | UUID | Primary Key |
| name | VARCHAR(100) | NOT NULL |
| created_by | UUID | FK → users.id |
| created_at | TIMESTAMPTZ | NOT NULL |
| updated_at | TIMESTAMPTZ | NOT NULL |
| deleted_at | TIMESTAMPTZ | NULL |
**Purpose:**

- Represents an independent family workspace.
- Owns patient profiles and medical records.
- Has its own subscription.
- Provides the boundary for family-level data access.

### 3.3 Family Memberships

Connects users with families.
| Column | Type | Constraints |
|---|---|---|
| id | UUID | Primary Key |
| family_id | UUID | FK → families.id |
| user_id | UUID | FK → users.id |
| role | VARCHAR(20) | NOT NULL |
| joined_at | TIMESTAMPTZ | NOT NULL |
| created_at | TIMESTAMPTZ | NOT NULL |
**Allowed roles:**

- `OWNER`
- `ADMIN`
- `MEMBER`
  **Constraints:**
- A user can have only one membership in a particular family.
- A user can belong to multiple different families.
- Each family must have an owner.
- Only authorized roles can invite or remove members and manage family settings.
  The combination of `family_id` and `user_id` must be unique.

### 3.4 Family Invitations

Stores invitations sent to people who are not yet members of a family.
| Column | Type | Constraints |
|---|---|---|
| id | UUID | Primary Key |
| family_id | UUID | FK → families.id |
| invited_by | UUID | FK → users.id |
| email | VARCHAR(255) | NOT NULL |
| role | VARCHAR(20) | NOT NULL |
| token_hash | VARCHAR(255) | NOT NULL |
| status | VARCHAR(20) | NOT NULL |
| expires_at | TIMESTAMPTZ | NOT NULL |
| accepted_at | TIMESTAMPTZ | NULL |
| created_at | TIMESTAMPTZ | NOT NULL |
**Purpose:**

- Allows family owners and authorized administrators to invite users.
- Supports invitation acceptance and expiration.
- Prevents storing raw invitation tokens.
  **Possible statuses:**
- `PENDING`
- `ACCEPTED`
- `EXPIRED`
- `REVOKED`

### 3.5 Patients

Stores patient profiles belonging to a family.
A patient profile does not require the patient to have a MediVault login account.
| Column | Type | Constraints |
|---|---|---|
| id | UUID | Primary Key |
| family_id | UUID | FK → families.id |
| full_name | VARCHAR(100) | NOT NULL |
| date_of_birth | DATE | NULL |
| gender | VARCHAR(30) | NULL |
| blood_group | VARCHAR(5) | NULL |
| relationship | VARCHAR(50) | NULL |
| notes | VARCHAR(1000) | NULL |
| created_at | TIMESTAMPTZ | NOT NULL |
| updated_at | TIMESTAMPTZ | NOT NULL |
| deleted_at | TIMESTAMPTZ | NULL |
**Purpose:**

- Stores family members' patient profiles.
- Connects medical records to individual patients.
- Allows a family to manage multiple patient profiles.
  **Subscription rule:**
- Free plan: Maximum 3 active patient profiles per family.
- Premium plan: Unlimited active patient profiles.
  The patient limit will be checked by the backend within a database transaction to prevent concurrent requests from exceeding the limit.

### 3.6 Medical Records

Stores medical document metadata and references to files in AWS S3.
The actual documents are never stored directly in PostgreSQL.
| Column | Type | Constraints |
|---|---|---|
| id | UUID | Primary Key |
| patient_id | UUID | FK → patients.id |
| family_id | UUID | FK → families.id |
| uploaded_by | UUID | FK → users.id |
| title | VARCHAR(200) | NOT NULL |
| description | VARCHAR(1000) | NULL |
| record_type | VARCHAR(50) | NOT NULL |
| document_date | DATE | NULL |
| storage_key | VARCHAR(500) | NOT NULL |
| original_filename | VARCHAR(255) | NOT NULL |
| mime_type | VARCHAR(100) | NOT NULL |
| file_size_bytes | BIGINT | NOT NULL |
| checksum_sha256 | VARCHAR(64) | NULL |
| created_at | TIMESTAMPTZ | NOT NULL |
| updated_at | TIMESTAMPTZ | NOT NULL |
| deleted_at | TIMESTAMPTZ | NULL |
**Possible record types:**

- `PRESCRIPTION`
- `LAB_REPORT`
- `SCAN`
- `DISCHARGE_SUMMARY`
- `VACCINATION`
- `OTHER`
  **Purpose:**
- Stores information about medical documents.
- Connects each document to a patient and family.
- Tracks who uploaded each document.
- References the private S3 object using `storage_key`.
  **Important security rule:**
  The backend must verify that the requesting user belongs to the family associated with the patient and record before allowing access.
  S3 objects must remain private. Access should be provided through short-lived pre-signed URLs after backend authorization.

### 3.7 Subscriptions

Stores family-level subscription information.
| Column | Type | Constraints |
|---|---|---|
| id | UUID | Primary Key |
| family_id | UUID | FK → families.id, UNIQUE |
| plan | VARCHAR(20) | NOT NULL |
| status | VARCHAR(20) | NOT NULL |
| provider | VARCHAR(30) | NULL |
| provider_customer_id | VARCHAR(255) | NULL |
| provider_subscription_id | VARCHAR(255) | NULL |
| current_period_start | TIMESTAMPTZ | NULL |
| current_period_end | TIMESTAMPTZ | NULL |
| created_at | TIMESTAMPTZ | NOT NULL |
| updated_at | TIMESTAMPTZ | NOT NULL |
**Possible plans:**

- `FREE`
- `PREMIUM`
  **Possible statuses:**
- `ACTIVE`
- `TRIALING`
- `PAST_DUE`
- `CANCELLED`
- `EXPIRED`
  **Purpose:**
- Manages the subscription for an entire family.
- Controls the number of patient profiles permitted.
- Stores payment-provider references when premium billing is introduced.
  A family should have one current subscription record. The free plan is the default.

### 3.8 Audit Logs

Tracks important actions performed within MediVault.
| Column | Type | Constraints |
|---|---|---|
| id | UUID | Primary Key |
| family_id | UUID | FK → families.id |
| actor_user_id | UUID | FK → users.id, NULL |
| action | VARCHAR(100) | NOT NULL |
| entity_type | VARCHAR(50) | NOT NULL |
| entity_id | UUID | NULL |
| metadata | JSONB | NULL |
| created_at | TIMESTAMPTZ | NOT NULL |
**Example actions:**

- `FAMILY_CREATED`
- `MEMBER_INVITED`
- `MEMBER_REMOVED`
- `PATIENT_CREATED`
- `PATIENT_UPDATED`
- `RECORD_UPLOADED`
- `RECORD_DELETED`
  **Purpose:**
- Maintains an activity history.
- Helps investigate unauthorized or unexpected actions.
- Provides accountability for sensitive medical-record operations.
  Audit logs should be append-only. Avoid storing passwords, access tokens, medical document contents, or unnecessary sensitive personal information in log metadata.

---

## 4. Database Relationships

| Relationship                  | Type        |
| ----------------------------- | ----------- |
| Users → Family Memberships    | One-to-Many |
| Families → Family Memberships | One-to-Many |
| Families → Patients           | One-to-Many |
| Patients → Medical Records    | One-to-Many |
| Families → Subscriptions      | One-to-One  |
| Families → Family Invitations | One-to-Many |
| Families → Audit Logs         | One-to-Many |
| Users → Medical Records       | One-to-Many |
| Users → Audit Logs            | One-to-Many |

## Users and families have a many-to-many relationship through `family_memberships`.

## 5. Important Indexes and Constraints

The initial database should include:

- Unique index on `users.email`.
- Unique constraint on `(family_id, user_id)` in `family_memberships`.
- Unique constraint on `subscriptions.family_id`.
- Index on `patients.family_id`.
- Index on `medical_records.patient_id`.
- Index on `medical_records.family_id`.
- Index on `medical_records.uploaded_by`.
- Index on `family_invitations.family_id` and invitation status.
- Index on `audit_logs.family_id` and `created_at`.
  Additional constraints:
- `file_size_bytes` must be greater than zero.
- Roles, subscription plans, statuses, and record types must use validated allowed values.
- Foreign keys must prevent orphaned records.
- Family and patient relationships must be validated to ensure a medical record cannot connect a patient from one family to another family's records.
  Use transactions for operations that update related data or enforce subscription limits.

---

## 6. Data Types and Conventions

| Purpose           | PostgreSQL Type |
| ----------------- | --------------- |
| Primary keys      | UUID            |
| Names             | VARCHAR(100)    |
| Email             | VARCHAR(255)    |
| Password hashes   | VARCHAR(255)    |
| Descriptions      | VARCHAR(1000)   |
| Dates             | DATE            |
| Timestamps        | TIMESTAMPTZ     |
| Boolean values    | BOOLEAN         |
| File sizes        | BIGINT          |
| Flexible metadata | JSONB           |

### General conventions

- Use `snake_case` for table and column names.
- Use UUID primary keys.
- Use `TIMESTAMPTZ` for timestamps.
- Store timestamps in UTC.
- Use `VARCHAR` with explicit limits for ordinary string fields.
- Use JSONB only for genuinely flexible metadata.
- Use foreign keys wherever relationships exist.

---

## 7. Soft Deletion and Data Retention

Soft deletion will initially be supported for:

- User accounts.
- Families.
- Patient profiles.
- Medical records.
  Soft-deleted records should not appear in ordinary application queries.
  Audit logs should not be soft-deleted or silently modified.
  Permanent deletion and retention policies must be designed carefully, particularly for medical documents and account-related personal information.

---

## 8. Family Data Isolation and Security

Family isolation is one of the most important parts of the MediVault database design.
Every request involving a family-owned resource must verify the user's membership and permissions.
For example, when retrieving a medical record:

1. Authenticate the user.
2. Identify the requested medical record.
3. Determine the family associated with the record.
4. Verify the user's membership in that family.
5. Verify the user's permissions.
6. Return the authorized record or a private, short-lived file URL.
   Knowing a UUID must never be sufficient to access a medical record.
   The backend must also validate that the `family_id` stored on a medical record matches the family that owns its referenced patient.

---

## 9. Future Database Enhancements

The following tables and features can be introduced when the application requires them:

- Refresh Tokens / Sessions.
- Notifications.
- Payment Transactions.
- Medical Record Categories.
- Record Sharing and Access Permissions.
- User Activity History.
- Family Settings.
- Data Export Requests.
- Account Deletion Requests.
  These are intentionally excluded from the initial schema to keep the first version manageable.

---

## 10. Database Technology

**Database:** PostgreSQL
**ORM:** SQLAlchemy 2
**Migrations:** Alembic
**Validation:** Pydantic
Database schema changes will be managed through Alembic migrations rather than manual production database modifications.
The initial database name will be `medivault`.

---

## 11. Summary

The MediVault database is designed around family workspaces, with users connected to families through memberships.
This structure supports:

- Multiple families per user.
- Multiple users per family.
- Multiple patient profiles per family.
- Medical records linked to individual patients.
- Family-level subscription management.
- Auditable access and activity.
- Secure private document storage.
  The design provides a foundation for MediVault 2.0 while leaving room for future features.


---

## 12. Cross-family integrity constraints

Application authorization is essential, but the database should also prevent a medical record from referencing a patient owned by a different family.

To enforce this relationship:

1. Keep `patients.id` as the primary key.
2. Add a composite unique constraint on `patients(family_id, id)`.
3. In `medical_records`, use a composite foreign key from `(family_id, patient_id)` to `patients(family_id, id)`.

Conceptually, the relevant constraints are:

```sql
ALTER TABLE patients
ADD CONSTRAINT uq_patients_family_id_id
UNIQUE (family_id, id);

ALTER TABLE medical_records
ADD CONSTRAINT fk_medical_records_family_patient
FOREIGN KEY (family_id, patient_id)
REFERENCES patients (family_id, id);
```

The composite foreign key makes it impossible to attach a patient from Family A to a medical record that claims to belong to Family B. The ORM relationships and Alembic migration must reflect this constraint. Do not rely only on a service-layer check.

The backend must still verify the requesting user's family membership and role. Database integrity does not replace authorization.

## 13. Authentication session persistence

Refresh-token rotation requires server-side session state. Before implementing refresh-token authentication, add a dedicated session or refresh-token table through an Alembic migration.

A possible initial design is:

| Column | Type | Constraints |
|---|---|---|
| id | UUID | Primary Key |
| user_id | UUID | FK → users.id, NOT NULL |
| token_hash | VARCHAR(255) | UNIQUE, NOT NULL |
| expires_at | TIMESTAMPTZ | NOT NULL |
| created_at | TIMESTAMPTZ | NOT NULL |
| revoked_at | TIMESTAMPTZ | NULL |
| replaced_by_token_id | UUID | NULL, FK → refresh_tokens.id |

Store only a hash of the refresh-token secret, never the raw token. The backend should rotate tokens, revoke the previous token, detect reuse, and revoke the affected token family/session according to the chosen security policy.

This table is an implementation prerequisite for refresh-token rotation, even though it is introduced in the authentication phase rather than required for the first database-learning exercises. Its final name and columns can be refined before the authentication migration is created.

## 14. Constraint implementation notes

- Add database CHECK constraints for finite role, invitation-status, subscription-plan, subscription-status, and medical-record-type values, or use PostgreSQL enum types after considering migration implications.
- Add a unique constraint on `family_invitations.token_hash`.
- Use a transaction when creating a family and its initial OWNER membership so the application cannot leave a newly created family without its owner.
- Enforce that a family retains at least one active owner through transactional application logic or a carefully designed database mechanism; a simple row-level CHECK constraint cannot enforce this across membership rows.
- Ensure queries that list active patients and enforce the free-plan limit consistently exclude soft-deleted patients.
- Confirm delete behavior for each foreign key before creating migrations. Avoid cascading deletion of audit history or medical documents without an explicit retention policy.
