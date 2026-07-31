# Enterprise Survey AI

# AI Agent Design

---

# Overview

The platform uses LangGraph to orchestrate multiple AI agents.

Each agent has a single responsibility and collaborates with other agents to automate the complete survey lifecycle.

---

# AI Architecture

User

↓

Requirement Agent

↓

Survey Designer Agent

↓

Validation Agent

↓

Survey Service

↓

Analytics Agent

↓

Recommendation Agent

↓

Report Agent

---

# Agent 1

## Requirement Agent

Purpose

Understand the business requirement.

Responsibilities

- Extract survey objective
- Identify audience
- Detect survey type
- Estimate question count
- Identify required sections

Input

Natural language prompt

Output

Structured survey requirements

---

# Agent 2

## Survey Designer Agent

Purpose

Generate survey structure.

Responsibilities

- Create sections
- Create questions
- Select question types
- Arrange ordering

Tools

LLM

RAG

Organization Templates

Output

Survey Draft

---

# Agent 3

## Validation Agent

Purpose

Validate generated survey.

Checks

- Duplicate questions
- Leading questions
- Bias detection
- Sensitive content
- Grammar
- Survey length
- Required question coverage

Output

Validation Report

---

# Agent 4

## Analytics Agent

Purpose

Analyze submitted responses.

Responsibilities

- Sentiment Analysis
- Completion Rate
- NPS
- CSAT
- Department Trends

Output

Analytics Summary

---

# Agent 5

## Recommendation Agent

Purpose

Generate business recommendations.

Examples

Improve leadership communication

Increase employee recognition

Improve onboarding

Output

Actionable Recommendations

---

# Agent 6

## Report Agent

Purpose

Generate executive reports.

Responsibilities

- Executive Summary
- Charts
- KPIs
- AI Summary
- Recommendations

Output

PDF Report

---

# LangGraph State

The workflow maintains shared state.

State includes

- User Request
- Survey Draft
- Validation Result
- Analytics Result
- Recommendations
- Report Metadata

---

# AI Tools

The agents use tools instead of directly solving every problem.

Tools include

- PostgreSQL Search
- Qdrant Vector Search
- Survey Template Search
- Organization Policy Lookup
- Sentiment Analysis
- PDF Generator

---

# RAG Workflow

Organization Documents

↓

Embedding Model

↓

Qdrant

↓

Semantic Search

↓

Relevant Context

↓

LLM

---

# Prompt Strategy

Every agent has its own prompt.

Prompts are version controlled.

Prompt changes do not require code changes.

---

# Human Approval

Users can review generated surveys before publication.

AI suggestions are never published automatically.

---

# Error Handling

If one agent fails

↓

Retry

↓

Fallback Prompt

↓

Manual Review

---

# Future Enhancements

- Translation Agent
- Compliance Agent
- Risk Assessment Agent
- Voice Survey Agent
- Image Analysis Agent
- Meeting Summary Agent