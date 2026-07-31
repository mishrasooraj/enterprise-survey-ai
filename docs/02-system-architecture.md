# Enterprise Survey AI
# System Architecture

---

# 1. Architecture Overview

Enterprise Survey AI follows a Microservice Architecture combined with an Event-Driven Architecture.

Each service owns its own business logic and communicates using REST APIs and Kafka Events.

The system is fully containerized using Docker Compose.

---

# 2. High Level Architecture

                        React Frontend

                              │

                        Traefik Gateway

                              │

       -----------------------------------------------------

       │            │             │

 Authentication   Survey      AI Service

    Service       Service      (LangGraph)

       │            │             │

       │            │             │

 PostgreSQL     PostgreSQL     Qdrant

       │            │             │

       └────────────┼─────────────┘

                    │

                  Kafka

                    │

    ---------------------------------------

    │            │            │

Analytics   Notification   Report Service

 Service      Service

                    │

                  Redis

                    │

                 MinIO

---

# 3. Architecture Style

The project follows

- Microservices
- Event Driven Architecture
- Clean Architecture
- Domain Driven Design (lightweight)
- API First Development

---

# 4. Communication

Synchronous Communication

REST APIs

Examples

Frontend

↓

Survey Service

Survey Service

↓

Authentication Service

Survey Service

↓

AI Service

---

Asynchronous Communication

Kafka

Examples

Survey Published

↓

Notification Service

Survey Submitted

↓

Analytics Service

↓

Report Service

---

# 5. Service Responsibilities

Authentication Service

Responsible for

- Login
- JWT
- RBAC
- User Management

---

Survey Service

Responsible for

- Organizations
- Projects
- Surveys
- Questions
- Responses
- Assignments

---

AI Service

Responsible for

- LangGraph
- AI Agents
- RAG
- Survey Generation
- Validation
- Recommendations

---

Analytics Service

Responsible for

- NPS
- CSAT
- Completion Rate
- Trends
- Dashboard Metrics

---

Notification Service

Responsible for

- Email
- Survey Invitations
- Reminder Emails

---

Report Service

Responsible for

- Executive Reports
- PDF Generation
- Charts
- AI Summary

---

# 6. Database Ownership

Authentication Service

↓

Auth Database

Survey Service

↓

Survey Database

Analytics Service

↓

Analytics Database

Report Service

↓

No Dedicated Database

AI Service

↓

Qdrant

---

# 7. External Components

PostgreSQL

Persistent Storage

Redis

Cache

Kafka

Messaging

Qdrant

Vector Database

MinIO

Object Storage

Keycloak

Authentication

Ollama

LLM

---

# 8. Design Principles

Single Responsibility

Loose Coupling

High Cohesion

Scalable

Stateless Services

Async Processing

Containerized

Observable

---

# 9. Deployment

Docker Compose

↓

Traefik

↓

Microservices

↓

Infrastructure Containers

---

# 10. Future Migration

Docker Compose

↓

Docker Swarm

↓

Kubernetes

↓

AWS ECS