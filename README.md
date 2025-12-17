# AI Model Governance & Compliance Hub

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![CI/CD](https://github.com/TamTunnel/AI-Governance-Hub/actions/workflows/ci.yml/badge.svg)](https://github.com/TamTunnel/AI-Governance-Hub/actions)

## What Is This?

A **centralized platform** for managing your organization's AI models—supporting both **EU AI Act** and **US AI governance** (NIST AI RMF) requirements.

**v0.4** adds: **Data Classification**, **Lineage Tracking**, **Human-in-the-Loop Approvals**, and **NIST AI RMF alignment**.

---

## Key Features

| Feature | Description |
|---------|-------------|
| **Model Registry** | Central catalog of AI models |
| **Risk Profiles** | EU AI Act & NIST AI RMF classification |
| **Data Classification** | Sensitivity (PII/PHI/PCI) and classification levels |
| **Lineage Tracking** | Datasets and model dependencies |
| **Human Approval** | Capture approver, approval notes, timestamps |
| **Policy Engine** | Define and enforce governance rules |
| **Multi-Tenancy** | Organization + environment scoping |
| **SSO Ready** | Designed for IdP integration |

---

## US AI Governance & NIST AI RMF Alignment

This platform supports alignment with the **NIST AI Risk Management Framework (AI RMF)**.

### NIST AI RMF Function Mapping

| NIST Function | Platform Capability |
|---------------|---------------------|
| **GOVERN** | RBAC, policies, organization scoping, audit logs |
| **MAP** | Model registry, risk profiles, data classification, lineage |
| **MEASURE** | Evaluation metrics, version tracking, performance history |
| **MANAGE** | Compliance lifecycle, policy enforcement, human approvals |

### Sectoral Applicability

| Regulation | Relevant Features |
|------------|-------------------|
| **HIPAA** | `data_sensitivity: phi`, audit logging |
| **GLBA/FFIEC** | Risk profiles, data classification, approval workflows |
| **CCPA/CPRA** | PII tracking, data sources documentation |
| **FedRAMP** | Organization scoping, audit trails, security controls |

---

## Data Classification & Sensitivity

### Sensitivity Levels

| Level | Description | Example Use Case |
|-------|-------------|------------------|
| `public` | Non-sensitive data | Public datasets |
| `internal` | Internal business data | Operational metrics |
| `pii` | Personally Identifiable Information | Customer names, emails |
| `phi` | Protected Health Information (HIPAA) | Medical records |
| `pci` | Payment Card Industry data | Credit card numbers |

### Classification Levels

| Level | Description |
|-------|-------------|
| `public` | Open to external parties |
| `internal` | Internal use only |
| `confidential` | Restricted access |
| `restricted` | Highly restricted (need-to-know) |

### Jurisdiction

Track data residency requirements with the `jurisdiction` field (e.g., "US", "EU", "Global").

---

## Lineage & Traceability

### Why Lineage Matters

- **Audit compliance**: Know exactly what data trained your models
- **Incident response**: Quickly identify affected models when data issues arise
- **Reproducibility**: Track model dependencies for retraining

### Data Model

```
Dataset (training data, validation data, etc.)
    ↓ linked via ModelDatasetLink
ModelRegistry (your AI model)
    ↓ linked via ModelDependency
ModelRegistry (parent models, fine-tuning sources)
```

### Example: Link a Dataset

```bash
# Create a dataset
curl -X POST "http://localhost:8000/api/v1/datasets/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Customer Transactions Q4",
    "source_system": "Snowflake",
    "data_sensitivity": "pii",
    "data_classification": "confidential"
  }'

# Link to a model
curl -X POST "http://localhost:8000/api/v1/models/1/datasets/" \
  -H "Content-Type: application/json" \
  -d '{"dataset_id": 1, "dataset_type": "training"}'
```

---

## Human-in-the-Loop Approvals

When a model is approved, the system captures:

| Field | Description |
|-------|-------------|
| `approved_by_user_id` | Who approved the model |
| `approved_at` | Timestamp of approval |
| `approval_notes` | Required justification |

**Approval notes are mandatory** when changing status to `approved`.

---

## SSO / Identity Provider Integration (Planned)

### Recommended Patterns

1. **Reverse proxy + headers**: Deploy behind Nginx/Envoy with IdP, pass user info via headers
2. **App-native OIDC**: Integrate directly with Okta, Azure AD, or Keycloak

### IdP Role Mapping

| IdP Group | Maps to Role |
|-----------|--------------|
| `ai-admins` | `admin` |
| `ml-engineers` | `model_owner` |
| `compliance-team` | `auditor` |

---

## Security & Deployment

### Network Placement

> [!IMPORTANT]
> Deploy behind a reverse proxy with TLS termination.

### Secrets Management

| Secret | Source |
|--------|--------|
| `DATABASE_URL` | Environment variable |
| `SECRET_KEY` | Environment variable (min 32 chars) |

### Observability

- Prometheus metrics: `GET /api/v1/metrics`
- Structured audit logs in `ComplianceLog` table

---

## Quick Start

```bash
git clone https://github.com/TamTunnel/AI-Governance-Hub.git
cd AI-Governance-Hub
cp .env.example .env
docker compose up --build
```

| Service | URL |
|---------|-----|
| Frontend | http://localhost:3000 |
| API Docs | http://localhost:8000/docs |
| Metrics | http://localhost:8000/api/v1/metrics |

---

## Roadmap

| Status | Feature |
|--------|---------|
| ✅ Done | Policy Engine |
| ✅ Done | Multi-tenancy |
| ✅ Done | Data Classification (v0.4) |
| ✅ Done | Lineage Tracking (v0.4) |
| ✅ Done | Human Approvals (v0.4) |
| 🔜 | SSO/OIDC integration |
| 🔜 | MLflow integration |
| 🔜 | Advanced policy DSL |
| 🔜 | Model lineage visualization |

---

## Technology Stack

| Layer | Technology |
|-------|------------|
| Frontend | React, TypeScript, Mantine |
| Backend | Python 3.11, FastAPI, SQLModel |
| Database | PostgreSQL 15 |
| Auth | OAuth2, JWT, RBAC |
| Infrastructure | Docker, Nginx |

---

## License

Apache License 2.0 — See [LICENSE](LICENSE).
