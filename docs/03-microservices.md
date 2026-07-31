# Enterprise Survey AI

# Microservice Design

---

# Overview

The platform follows a microservice architecture.

Each service:

- Owns its business logic
- Owns its APIs
- Owns its database objects
- Can be deployed independently
- Communicates using REST APIs and Kafka events

---

# Phase 1 Services

## 1. Authentication Service

### Purpose

Responsible for authentication and authorization.

### Responsibilities

- User Registration
- Login
- Logout
- JWT Token Generation
- Refresh Token
- Role Based Access Control (RBAC)
- Organization Membership

### REST APIs

POST /auth/login

POST /auth/register

POST /auth/logout

POST /auth/refresh

GET /users/me

GET /roles

### Database

Tables

- users
- roles
- permissions
- organizations
- organization_users

### Dependencies

PostgreSQL

Redis

Keycloak (optional future)

---

## 2. Survey Service

### Purpose

Responsible for complete survey lifecycle.

### Responsibilities

- Projects
- Surveys
- Questions
- Sections
- Assignments
- Respondents
- Responses
- Survey Versioning

### REST APIs

POST /surveys

GET /surveys

GET /surveys/{id}

PUT /surveys/{id}

DELETE /surveys/{id}

POST /surveys/{id}/publish

POST /responses

GET /responses

### Database

Tables

- projects
- surveys
- sections
- questions
- respondents
- survey_assignments
- responses

### Publishes Kafka Events

SurveyCreated

SurveyPublished

SurveyAssigned

SurveySubmitted

---

## 3. AI Service

### Purpose

Handles all AI workflows.

### Responsibilities

- AI Survey Generation
- Question Optimization
- Validation
- Bias Detection
- Recommendation Generation
- RAG
- LangGraph Workflow

### REST APIs

POST /ai/generate

POST /ai/validate

POST /ai/improve

POST /ai/analyze

POST /ai/recommend

### Dependencies

Ollama

Qdrant

LangGraph

Sentence Transformers

### Consumes Kafka Events

SurveySubmitted

### Publishes Kafka Events

AnalysisCompleted

RecommendationsGenerated

---

# Phase 2 Services

## Analytics Service

Responsibilities

- NPS
- CSAT
- Dashboard
- Trends
- Department Comparison

Consumes

SurveySubmitted

AnalysisCompleted

Publishes

AnalyticsGenerated

---

## Notification Service

Responsibilities

- Email
- Reminder
- Survey Invitation
- Completion Notification

Consumes

SurveyPublished

SurveyAssigned

---

## Report Service

Responsibilities

- PDF
- Charts
- Executive Summary
- AI Insights

Consumes

AnalyticsGenerated

RecommendationsGenerated

---

# Service Communication

Synchronous

Frontend

↓

Authentication

↓

Survey

↓

AI

---

Asynchronous

Survey Published

↓

Kafka

↓

Notification

Survey Submitted

↓

Kafka

↓

Analytics

↓

Report

---

# Design Principles

- Database per Service (logical ownership)
- Stateless Services
- Independent Deployment
- Event Driven
- API First
- High Cohesion
- Loose Coupling
- Health Checks for Every Service

---

# Health Endpoints

Every service exposes:

GET /health

GET /ready

GET /live

---

# Future Services

- File Service
- Audit Service
- Search Service
- Workflow Service
- Billing Service