# FarmHealth AI - System Architecture

## Overview

FarmHealth AI is a fully offline agricultural and livestock-health advisor designed for African farmers and extension officers.

The system combines:

1. Fine-tuned agricultural language model
2. Offline Retrieval-Augmented Generation (RAG)
3. Local knowledge base
4. Lightweight user interface

All components operate without cloud connectivity.

---

## High-Level Architecture

User
↓
FarmHealth Interface
↓
Query Processor
↓
Offline Retrieval Layer (RAG)
↓
Local Knowledge Base
↓
Fine-Tuned Language Model
↓
Response Generator
↓
User

---

## Core Components

### User Interface

Responsibilities:

- User interaction
- Prompt submission
- Response display

Owner:
UI/UX Designer

---

### Query Processor

Responsibilities:

- Input validation
- Query routing
- Context preparation

Owner:
Developer

---

### Offline Retrieval Layer

Responsibilities:

- Search local documents
- Retrieve relevant context
- Support location-aware recommendations

Owner:
Developer

---

### Local Knowledge Base

Contains:

- Agricultural manuals
- Livestock-health information
- Weather guidance
- Market references
- Extension documents

Owner:
Victor

---

### Fine-Tuned Language Model

Responsibilities:

- Agricultural reasoning
- Livestock-health guidance
- Decision support
- Question answering

Owner:
Victor

---

## Design Principles

- Fully Offline
- CPU Optimized
- Low Memory Usage
- African Context First
- English + Hausa Support
- Modular Architecture

---

## Target Hardware

- Ubuntu 22.04
- 8GB RAM
- Integrated Graphics
- No GPU Required
