# Enterprise Survey AI

# Deployment Architecture

---

# Deployment Strategy

The platform is containerized using Docker.

Development and production use the same Docker images.

Deployment follows a CI/CD workflow using GitHub Actions.

---

# Development Environment

Developer

↓

Git

↓

GitHub Repository

↓

Clone Repository

↓

Docker Compose

↓

Local Development

---

# Local Deployment

Command

docker compose up

Starts

- PostgreSQL
- Redis
- Kafka
- Kafka UI
- Ollama
- Qdrant
- MinIO
- Authentication Service
- Survey Service
- AI Service
- React Frontend

---

# Container Architecture

Frontend

↓

Traefik

↓

Authentication Service

Survey Service

AI Service

↓

PostgreSQL

Redis

Kafka

Qdrant

Ollama

MinIO

---

# Docker Networks

frontend-network

backend-network

monitoring-network

---

# Persistent Volumes

postgres-data

redis-data

kafka-data

qdrant-data

minio-data

grafana-data

---

# Environment Variables

Configuration is stored in

.env

The repository contains

.env.example

Developers copy

cp .env.example .env

before running the project.

---

# Health Checks

Every service exposes

GET /health

GET /ready

GET /live

Docker waits until dependencies become healthy.

---

# Startup Order

PostgreSQL

↓

Redis

↓

Kafka

↓

Qdrant

↓

Ollama

↓

Authentication Service

↓

Survey Service

↓

AI Service

↓

Frontend

---

# CI Pipeline

Developer Push

↓

GitHub

↓

GitHub Actions

↓

Lint

↓

Unit Tests

↓

Docker Build

↓

Integration Tests

↓

Ready for Deployment

---

# CD Strategy

GitHub Actions

↓

SSH

↓

Linux Server

↓

Pull Latest Images

↓

Docker Compose Up

---

# Logging

All containers write structured JSON logs.

Logs are collected by Loki.

---

# Monitoring

Prometheus

↓

Grafana Dashboard

---

# Tracing

OpenTelemetry

↓

Jaeger

---

# Security

JWT Authentication

Secrets stored in .env

Docker Secrets (Future)

HTTPS (Production)

---

# Production Deployment

Ubuntu Server

↓

Docker

↓

Docker Compose

↓

Traefik

↓

Microservices

↓

Infrastructure

---

# Future Migration

Docker Compose

↓

Docker Swarm

↓

Kubernetes

↓

AWS ECS