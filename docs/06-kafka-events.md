# Enterprise Survey AI

# Kafka Event Design

---

# Overview

The platform uses Apache Kafka for asynchronous communication between microservices.

Kafka helps decouple services and enables scalable event-driven processing.

---

# Design Principles

- Event Driven Architecture
- Loose Coupling
- Immutable Events
- Idempotent Consumers
- Retry Support
- Dead Letter Queue
- Event Versioning

---

# Kafka Topics

survey.events

analytics.events

ai.events

notification.events

report.events

audit.events

---

# Survey Events

## SurveyCreated

Producer

Survey Service

Consumers

Analytics Service

Audit Service

---

## SurveyPublished

Producer

Survey Service

Consumers

Notification Service

Audit Service

---

## SurveyAssigned

Producer

Survey Service

Consumers

Notification Service

Audit Service

---

## SurveySubmitted

Producer

Survey Service

Consumers

AI Service

Analytics Service

Audit Service

---

# AI Events

## AnalysisCompleted

Producer

AI Service

Consumers

Analytics Service

Report Service

---

## RecommendationGenerated

Producer

AI Service

Consumers

Report Service

---

# Analytics Events

## AnalyticsGenerated

Producer

Analytics Service

Consumers

Report Service

---

# Notification Events

## InvitationSent

Producer

Notification Service

Consumers

Audit Service

---

## ReminderSent

Producer

Notification Service

Consumers

Audit Service

---

# Event Structure

Every Kafka event follows the same structure.

{
    "event_id": "UUID",
    "event_name": "SurveyPublished",
    "event_version": "1.0",
    "occurred_at": "ISO Timestamp",
    "producer": "survey-service",
    "correlation_id": "UUID",
    "payload": {}
}

---

# Retry Strategy

Retry Count

3

Retry Delay

Exponential Backoff

---

# Dead Letter Queue

Failed messages move to

dead-letter.events

after all retries fail.

---

# Event Versioning

Each event contains

event_version

to support backward compatibility.

---

# Delivery Guarantee

At Least Once Delivery

Consumers must be idempotent.

---

# Message Ordering

Ordering is guaranteed within the same partition.

Survey ID should be used as the partition key.

---

# Monitoring

Kafka UI

Prometheus Metrics

Grafana Dashboard

Consumer Lag Monitoring