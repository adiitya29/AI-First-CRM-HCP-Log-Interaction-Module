# AI-First CRM – HCP Module

> An AI-first Customer Relationship Management system focused on the **Healthcare Professional (HCP)** module, built for life-science field representatives.

---

## 🧠 Overview

This project provides a **Log Interaction Screen** that lets field reps log interactions with HCPs via:
- **Structured Form** – traditional field-by-field data entry
- **Conversational Chat** – AI-powered natural language interface (LangGraph + Groq)

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

## 📋 Development Workflow

1. Work module-by-module (backend first, then frontend)
2. Test after every major change
3. Push to GitHub after each passing milestone
4. Move to the next module

---

## 📜 License

MIT
