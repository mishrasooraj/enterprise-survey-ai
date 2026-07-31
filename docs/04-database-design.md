# Enterprise Survey AI

# Database Design

---

# Database Overview

The application uses PostgreSQL as the primary relational database.

The database is designed using normalization principles while keeping future scalability in mind.

---

# Database Principles

- UUID Primary Keys
- Soft Delete
- Audit Columns
- Foreign Key Constraints
- Indexed Foreign Keys
- Multi-Tenant Design
- Survey Versioning

---

# Core Entities

## User

Represents a platform user.

Fields

- id
- email
- password_hash
- first_name
- last_name
- status
- created_at
- updated_at

---

## Role

Represents user roles.

Examples

- Admin
- HR Manager
- Manager
- Respondent

---

## Permission

Represents application permissions.

Examples

- survey:create
- survey:update
- survey:delete

---

## UserRole

Many-to-many relationship between users and roles.

---

## Organization

Represents a company.

Fields

- id
- name
- industry
- logo
- created_at

---

## Project

Each organization can have multiple projects.

Example

Employee Engagement

Customer Satisfaction

Product Feedback

---

## Survey

Represents a survey.

Fields

- id
- project_id
- title
- description
- status
- version
- created_at

Status

- Draft
- Published
- Closed

---

## Section

Each survey contains multiple sections.

Example

General Questions

Leadership

Culture

Work Environment

---

## Question

Belongs to one section.

Question Types

- Text
- Rating
- NPS
- CSAT
- Multiple Choice
- Checkbox
- Date

---

## Survey Assignment

Represents which respondent receives which survey.

---

## Response

Represents submitted answers.

---

## Attachment

Stores uploaded files.

Actual files are stored in MinIO.

Database stores only metadata.

---

# Relationships

Organization

↓

Projects

↓

Surveys

↓

Sections

↓

Questions

↓

Responses

---

Users

↓

Roles

↓

Permissions

---

Survey

↓

Assignments

↓

Respondents

↓

Responses

---

# Indexes

Unique

email

Composite

organization_id + status

survey_id + version

response_id + question_id

---

# Constraints

Email must be unique.

Survey version must be unique inside a project.

Response must belong to an existing survey.

Question must belong to a valid section.

---

# Audit Columns

Every table contains

created_at

updated_at

created_by

updated_by

deleted_at

---

# Future Tables

- Audit Logs
- Notification History
- AI Prompt History
- AI Feedback
- Search History
- API Keys
- Webhooks