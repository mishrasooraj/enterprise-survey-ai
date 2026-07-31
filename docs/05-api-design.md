# Enterprise Survey AI

# API Design

---

# API Principles

The platform follows REST API design principles.

All APIs are

- Stateless
- Versioned
- JSON Based
- Resource Oriented
- OpenAPI Compatible

---

# Base URL

/api/v1

---

# Authentication

Authorization Header

Bearer JWT_TOKEN

---

# Response Format

Success

{
    "success": true,
    "message": "...",
    "data": {}
}

Failure

{
    "success": false,
    "message": "...",
    "errors": []
}

---

# Authentication APIs

POST /api/v1/auth/register

POST /api/v1/auth/login

POST /api/v1/auth/logout

POST /api/v1/auth/refresh

GET /api/v1/users/me

---

# Organization APIs

POST /api/v1/organizations

GET /api/v1/organizations

GET /api/v1/organizations/{id}

PUT /api/v1/organizations/{id}

DELETE /api/v1/organizations/{id}

---

# Project APIs

POST /api/v1/projects

GET /api/v1/projects

GET /api/v1/projects/{id}

PUT /api/v1/projects/{id}

DELETE /api/v1/projects/{id}

---

# Survey APIs

POST /api/v1/surveys

GET /api/v1/surveys

GET /api/v1/surveys/{id}

PUT /api/v1/surveys/{id}

DELETE /api/v1/surveys/{id}

POST /api/v1/surveys/{id}/publish

POST /api/v1/surveys/{id}/duplicate

---

# Question APIs

POST /api/v1/questions

PUT /api/v1/questions/{id}

DELETE /api/v1/questions/{id}

---

# Assignment APIs

POST /api/v1/assignments

GET /api/v1/assignments

---

# Response APIs

POST /api/v1/responses

GET /api/v1/responses

GET /api/v1/responses/{id}

---

# AI APIs

POST /api/v1/ai/generate

POST /api/v1/ai/validate

POST /api/v1/ai/improve

POST /api/v1/ai/analyze

POST /api/v1/ai/recommend

---

# Analytics APIs

GET /api/v1/analytics/dashboard

GET /api/v1/analytics/nps

GET /api/v1/analytics/csat

GET /api/v1/analytics/completion

---

# Report APIs

GET /api/v1/reports/{survey_id}

POST /api/v1/reports/generate

---

# Pagination

?page=1

&size=20

---

# Filtering

?status=published

?organization_id=uuid

?project_id=uuid

---

# Sorting

?sort=created_at

?order=desc

---

# Search

?search=employee

---

# Standard Headers

Authorization

Content-Type

Accept

X-Request-ID

---

# Error Codes

400 Bad Request

401 Unauthorized

403 Forbidden

404 Not Found

409 Conflict

422 Validation Error

500 Internal Server Error