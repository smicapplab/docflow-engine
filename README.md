# docflow-engine

Local-first Intelligent Document Processing (IDP) Proof of Concept focused on extracting structured data from financial and compliance documents.

This project is designed as a clean, production-oriented architecture while remaining lightweight for local development and experimentation.

---

## 📦 Architecture Overview

The system is composed of two primary services:

```
NextJS (fe-idp)
        ↓
NestJS API (be-idp)
        ↓
Python Extraction Engine (idp-engine)
        ↓
NestJS API (be-idp)
        ↓
PostgreSQL
```

### Services

- **fe-idp** → NextJS frontend
- **be-idp** → NestJS API (orchestrator & persistence)
- **idp-engine** → Python extraction engine (document parsing & structured output)
- **PostgreSQL** → Persistence layer

> The Python engine is stateless and has **no direct database connection**.
> It returns structured JSON back to NestJS, which is fully responsible for persistence,
> orchestration, and API exposure.

---

## 🎯 Project Scope (POC)

Current scope is intentionally limited but designed for expansion:

- Digital-native PDF bank statements
- Image-based / scanned bank statements (automatic OCR detection and processing)
- Transaction table reconstruction
- Ledger normalization (JSON output)
- Balance reconciliation validation
- Fully local processing (Tesseract OCR for scanned documents, no external document AI services such as Textract)
- Automatic detection of text-based vs image-based PDFs (text-layer check → OCR fallback)
- Rule-based document classification (offline-safe)

Future document types (planned):
- Homeowners Insurance (HOI)
- Government ID documents
- Paystubs
- Mortgage statements

Future analytical extensions:
- Mortgage underwriting analysis
- Fraud detection
- Cash flow forecasting

---

## 🗂 Project Structure

```
docflow-engine/
├── be-idp/           # NestJS API (orchestrator)
├── fe-idp/           # NextJS frontend
├── idp-engine/       # Python extraction engine
│   ├── app/
│   │   ├── core/     # Extraction, classification, routing
│   │   ├── documents/# Document-specific parsers
│   │   ├── models/   # Pydantic output contracts
│   │   └── main.py   # Engine entrypoint
├── docker-compose.yml
├── .env
└── README.md
```

---

## 🧠 Engine Processing Flow

```
PDF
   ↓
Raw Text Extraction (PDF or OCR)
   ↓
Document Classification
   ↓
Document-Specific Parser
   ↓
Normalization
   ↓
Validation / Reconciliation
   ↓
Confidence Scoring
   ↓
Structured JSON Output
```

The engine is document-type aware and layout-aware.

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

- PostgreSQL
- NestJS API
- Python extraction engine

Frontend can be run separately:

```
cd fe-idp
npm install
npm run dev
```

---

## 🧠 Development Workflow

### Backend (NestJS)
```
cd be-idp
npm install
npm run start:dev
```

### Python Engine (Local)
```
cd idp-engine
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m app.main /path/to/document.pdf
```

The engine will output structured JSON.

---

## 🔒 Design Principles

- Clear separation between orchestration and extraction
- Stateless Python engine
- No direct database access from extraction engine
- Strict data contracts (Pydantic models)
- Offline-safe classification (rule-based)
- Automatic OCR fallback
- Layout-aware parsing for semi-structured documents
- Incremental expansion path for additional document types
- Privacy-conscious architecture (sensitive financial data processed locally)
- External LLM usage is optional and strictly limited to post-processing enrichment
- Cost-aware engineering decisions during POC phase

---

## 📖 Status

Infrastructure and engine scaffolding complete.

Next steps:
- Harden bank statement layout parser
- Implement structured normalization validation
- Add HOI parser module
- Integrate engine invocation from NestJS API