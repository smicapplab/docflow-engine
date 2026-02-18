# IDP-LOC

Local-first Intelligent Document Processing (IDP) Proof of Concept focused on extracting structured data from Bank Statement PDFs.

This project is designed as a clean, production-oriented microservice architecture while remaining lightweight enough for local development and experimentation.

---

## 📦 Architecture Overview

The system is composed of three services:

```
NextJS (fe-idp)
        ↓
NestJS API (be-idp)
        ↓
Redis Queue
        ↓
Python Worker (idp-engine)
        ↓
NestJS Result Endpoint
        ↓
PostgreSQL
```

### Services

- **fe-idp** → NextJS frontend
- **be-idp** → NestJS API (orchestrator)
- **idp-engine** → Python worker (PDF parsing & ledger extraction)
- **Redis** → Message broker
- **PostgreSQL** → Persistence layer

---

## 🎯 Project Scope (POC)

Current scope is intentionally limited:

- Digital-native PDF bank statements
- Transaction table reconstruction
- Ledger normalization (JSON output)
- Balance reconciliation validation
- Redis-based job queue
- Fully local processing (no Textract or external OCR services)

Future extensions may include:
- OCR fallback
- Mortgage underwriting analysis
- Fraud detection
- Cash flow forecasting

---

## 🗂 Project Structure

```
IDP-LOC/
├── be-idp/        # NestJS API
├── fe-idp/        # NextJS frontend
├── idp-engine/    # Python worker
├── docker-compose.yml
├── .env
└── README.md
```

---

## ⚙️ Environment Configuration

Create a root `.env` file:

```
POSTGRES_USER=idp
POSTGRES_PASSWORD=super_secure_password
POSTGRES_DB=idp_db
```

Do not commit `.env`.  
Commit a `.env.example` instead if needed.

---

## 🐳 Running with Docker (Recommended)

From project root:

```
docker compose up --build
```

This starts:

- Redis
- PostgreSQL
- NestJS API
- Python Worker

Frontend can be run separately:

```
cd fe-idp
npm install
npm run dev
```

---

## 🧠 Development Workflow

### Backend
```
cd be-idp
npm install
npm run start:dev
```

### Worker (local without Docker)
```
cd idp-engine
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app/worker.py
```

---

## 🔒 Production Considerations

- Containers use restart policies
- Postgres and Redis use persistent volumes
- Only API port (3000) is exposed
- Services communicate over isolated Docker network
- Environment variables injected via Docker Compose

---

## 🚀 Deployment

On Linux server:

```
git clone <repo>
cd IDP-LOC
docker compose up -d --build
```

Optional improvements:
- Add Nginx reverse proxy
- Add HTTPS (Let's Encrypt)
- Use managed DB/Redis for high availability

---

## 📌 Design Principles

- Clear service boundaries
- Stateless worker
- Queue-based processing
- No direct DB access from worker
- Strict data contracts between services
- Incremental expansion path

---

## 📖 Status

Initial infrastructure scaffolding complete.  
Next step: implement Redis job publishing and worker extraction pipeline.