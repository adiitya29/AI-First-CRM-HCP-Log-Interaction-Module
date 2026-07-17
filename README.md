# AI-First CRM – HCP Module

> An AI-first Customer Relationship Management system focused on the **Healthcare Professional (HCP)** module, built for life-science field representatives.

---

## 🧠 Overview

This project provides a **Log Interaction Screen** that lets field reps log interactions with HCPs via:
- **Structured Form** – traditional field-by-field data entry
- **Conversational Chat** – AI-powered natural language interface using LangGraph & Groq (`gemma2-9b-it`)

Currently, the **Backend** is fully functional with robust CRUD operations, Pytest test suites, database configurations, and a working AI LangGraph agent to extract structured fields from natural language notes.
---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React 18 + Redux Toolkit + Vite |
| Backend | Django 5 + Django REST Framework |
| AI Agent | LangGraph + Groq (`gemma2-9b-it`) |
| Database | PostgreSQL via Supabase |
| Font | Google Inter |

---

## 📁 Project Structure

```
.
├── backend/          # Django REST API
│   ├── core/         # Project settings (base / dev / prod)
│   ├── apps/
│   │   └── hcp/      # HCP module app
│   ├── manage.py
│   └── requirements.txt
├── frontend/         # React + Redux SPA
│   ├── src/
│   │   ├── store/         # Redux store
│   │   ├── features/hcp/  # HCP slice & thunks
│   │   └── components/    # Shared UI components
│   └── package.json
└── README.md
```

---

## 🚀 Getting Started

### Backend

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env          # fill in your secrets
python manage.py migrate
python manage.py runserver
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

---

## 🔑 Environment Variables

Copy `backend/.env.example` to `backend/.env` and fill in:

| Variable | Description |
|----------|-------------|
| `SECRET_KEY` | Django secret key |
| `DATABASE_URL` | Supabase PostgreSQL connection string |
| `GROQ_API_KEY` | Groq API key (for LLM calls) |
| `DEBUG` | `True` / `False` |
| `ALLOWED_HOSTS` | Comma-separated list |

---

## 📋 Development Workflow (Progress)

### ✅ Completed So Far (Backend)
- **Module 1: Scaffold & Serialization**
  - Django models for `HealthcareProfessional` and `Interaction`.
  - DRF Serializers, API views, and URL routing.
- **Module 2: Database & Migrations**
  - PostgreSQL via Supabase connection.
  - Safe local testing using an in-memory SQLite override via `conftest.py`.
  - Custom `verify_db` management command.
- **Module 3: Full API CRUD Integration**
  - Advanced filtering and querying.
  - 39 integration tests verifying every endpoint, creation rule, and partial update.
- **Module 4: LangGraph AI Agent**
  - Integration with Groq API (`gemma2-9b-it`).
  - Structured data extraction using Pydantic schemas (converting natural language logs to structured JSON).
  - Fully mocked unit tests to test the API without burning Groq credits.
  - Total of **40/40 passing Pytest tests**.

### 🚧 Up Next (Frontend)
- Setting up the Redux Thunks to consume these Django endpoints.
- Building the UI (Forms and AI Chatbox) using React and the predefined Inter typography and CSS Design Tokens.

---

## 📜 License

MIT
