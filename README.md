# AI Model Governance & Compliance Hub

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![CI/CD](https://github.com/TamTunnel/AI-Governance-Hub/actions/workflows/ci.yml/badge.svg)](https://github.com/TamTunnel/AI-Governance-Hub/actions)

## What Is This?

A **centralized platform** for managing your organization's AI models—a registry that tracks every AI system, its versions, performance metrics, and a complete audit trail. It helps answer:

- *"What AI models are we running in production?"*
- *"Who owns this model? When was it last updated?"*
- *"Can we prove compliance for regulatory audits (EU AI Act)?"*

---

## Key Features

| Feature | Description |
|---------|-------------|
| **Model Registry** | Register and catalog AI models with name, owner, and description |
| **Version Tracking** | Track model versions (v1.0, v2.1) and artifact storage locations (S3) |
| **Evaluation Metrics** | Store accuracy, F1 score, bias metrics per version |
| **Audit Logging** | Automatic immutable compliance trail for all create/update actions |
| **API Schemas (DTOs)** | Pydantic validation schemas separate from database models |
| **OAuth2 Authentication** | JWT-based auth with user registration and login |
| **PDF Compliance Reports** | Generate EU AI Act style compliance reports for any model |
| **Health Monitoring** | `/health` endpoint for load balancers and Kubernetes probes |
| **Secrets Management** | Environment-based configuration, no hardcoded credentials |
| **CI/CD Pipeline** | GitHub Actions for linting, testing, building, and deployment |

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      FRONTEND (React)                       │
│   • Model List Dashboard    • Register New Model Form       │
│   • Version & Metrics View  • Mantine UI Components         │
└─────────────────────────────────────────────────────────────┘
                              │ REST API
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      BACKEND (FastAPI)                      │
│   /api/v1/models         → Model registry CRUD              │
│   /api/v1/versions       → Version management               │
│   /api/v1/metrics        → Evaluation data storage          │
│   /api/v1/audit-logs     → Compliance audit history         │
│   /api/v1/auth/register  → User registration                │
│   /api/v1/auth/token     → JWT login                        │
│   /api/v1/reports/{id}/compliance-report → PDF download     │
│   /api/v1/health         → System health check              │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    DATABASE (PostgreSQL)                    │
│   Tables: modelregistry, modelversion, evaluationmetric,    │
│           compliancelog, user                               │
└─────────────────────────────────────────────────────────────┘
```

---

## Quick Start

### Prerequisites
- Docker & Docker Compose
- Node.js 18+ (for frontend development)

### Run with Docker
```bash
# Clone the repo
git clone https://github.com/TamTunnel/AI-Governance-Hub.git
cd AI-Governance-Hub

# Copy environment template
cp .env.example .env

# Start all services
docker compose up --build
```

**URLs:**
| Service | URL |
|---------|-----|
| Frontend | http://localhost:3000 |
| API Docs (Swagger) | http://localhost:8000/docs |
| Health Check | http://localhost:8000/api/v1/health |

### Development Mode
```bash
# Backend
cd backend && poetry install && poetry run uvicorn app.main:app --reload

# Frontend (separate terminal)
cd frontend && npm install && npm run dev
```

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/v1/auth/register` | Create user account |
| `POST` | `/api/v1/auth/token` | Login, get JWT token |
| `POST` | `/api/v1/models/` | Register new AI model |
| `GET` | `/api/v1/models/` | List all models |
| `GET` | `/api/v1/models/{id}` | Get model details |
| `POST` | `/api/v1/versions/` | Add model version |
| `POST` | `/api/v1/metrics/` | Add evaluation metric |
| `GET` | `/api/v1/audit-logs/` | View compliance audit trail |
| `GET` | `/api/v1/reports/models/{id}/compliance-report` | Download PDF report |
| `GET` | `/api/v1/health` | System health status |

---

## Technology Stack

| Layer | Technology |
|-------|------------|
| Frontend | React, TypeScript, Vite, Mantine UI |
| Backend | Python 3.11, FastAPI, SQLModel, Pydantic |
| Database | PostgreSQL 15 |
| Auth | OAuth2, JWT (python-jose), bcrypt |
| Reports | ReportLab (PDF generation) |
| Infrastructure | Docker, Docker Compose, Nginx |
| CI/CD | GitHub Actions |

---

## Configuration

Copy `.env.example` to `.env` and configure:

```bash
# Database
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_secure_password
DATABASE_URL=postgresql://postgres:password@db:5432/ai_governance

# Authentication
SECRET_KEY=your-secret-key-minimum-32-characters

# Frontend
VITE_API_URL=http://localhost:8000/api/v1
```

---

## CI/CD Pipeline

The GitHub Actions workflow (`.github/workflows/ci.yml`) includes:

1. **Backend Tests** - Runs pytest with PostgreSQL service
2. **Frontend Build** - Lints and builds the React app
3. **Docker Build** - Builds production images
4. **Deploy** - Placeholder for staging/production deployment

---

## License

This project is licensed under the **Apache License 2.0** — an enterprise-friendly open-source license that permits commercial use, modification, and distribution.

See [LICENSE](LICENSE) for full details.
