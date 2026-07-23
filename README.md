# AI-First CRM – HCP Module: Log Interaction Screen

> An AI-first Customer Relationship Management system focused on the **Healthcare Professional (HCP)** module, built for life-science field representatives.

---

## 🧠 Overview

This project provides a **Log Interaction Screen** that lets field reps log interactions with HCPs in two ways:

- **Structured Form** – traditional field-by-field data entry with full control
- **Conversational AI Chat** – natural language interface powered by LangGraph & Groq (`llama-3.3-70b-versatile`)

The AI assistant intelligently parses free-form text and **selectively populates** the corresponding form fields — only updating fields that were explicitly mentioned, leaving all other fields untouched.

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | React 18 + Redux Toolkit + Vite |
| **Styling** | Vanilla CSS (Custom Design System, Glassmorphism, Inter Font) |
| **Backend** | Django 5 + Django REST Framework |
| **AI Agent** | LangGraph + LangChain + Groq (`llama-3.3-70b-versatile`) |
| **Database** | PostgreSQL via Supabase |
| **Testing** | Pytest + Factory Boy (SQLite in-memory for tests) |

---

## 📁 Project Structure

```
.
├── backend/
│   ├── core/
│   │   └── settings/          # base / development / testing configs
│   ├── apps/
│   │   └── hcp/
│   │       ├── ai/
│   │       │   ├── agent.py   # LangGraph state graph + LLM chain
│   │       │   └── schemas.py # Pydantic schemas for structured extraction
│   │       ├── tests/         # Pytest integration & unit tests (40/40 pass)
│   │       ├── models.py      # HealthcareProfessional & Interaction models
│   │       ├── serializers.py # DRF serializers
│   │       ├── views.py       # API views (CRUD + AI chat endpoint)
│   │       └── urls.py
│   ├── conftest.py            # SQLite override for safe pytest runs
│   ├── pytest.ini
│   ├── manage.py
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── store/
│   │   │   └── store.js            # Redux store
│   │   ├── features/hcp/
│   │   │   ├── hcpSlice.js         # Redux slice + async thunks
│   │   │   ├── LogInteractionPage.jsx
│   │   │   └── components/
│   │   │       ├── InteractionForm.jsx   # Controlled form with AI sync
│   │   │       └── AiAssistantChat.jsx   # AI chat input panel
│   │   ├── components/ui/
│   │   │   ├── index.jsx   # Reusable UI primitives (Card, Input, Button…)
│   │   │   └── ui.css
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── index.css       # Design system tokens (HSL colors, typography, glassmorphism)
│   └── package.json
└── README.md
```

---

## 📋 Development Modules (Completed)

### ✅ Backend

#### Module 1 – Scaffold & Serialization
- Django models: `HealthcareProfessional` and `Interaction`
- DRF Serializers, API views, and URL routing
- 11/11 initial tests passing

#### Module 2 – Database & Migrations
- PostgreSQL (Supabase) connection with SSL
- In-memory SQLite override via `core/settings/testing.py` for fast, isolated tests
- Custom `verify_db` management command

#### Module 3 – Full API CRUD Integration
- HCP list, create, retrieve, update, delete endpoints
- Interaction logging with filtering by HCP, date, type
- 39/39 integration tests passing (Factory Boy for test data)

#### Module 4 – LangGraph AI Agent
- LangGraph `StateGraph` with a single parsing node
- Pydantic schema `InteractionExtraction` for structured output via LangChain's `with_structured_output`
- Groq `llama-3.3-70b-versatile` for reliable JSON extraction
- **Selective field extraction**: all schema fields default to `None`; the AI only populates fields that are explicitly mentioned in the user's message
- Fully mocked unit tests to verify parsing without burning API credits
- **40/40 Pytest tests passing**

---

### ✅ Frontend

#### Module 5 – Log Interaction Screen UI

**Design System (`index.css`)**
- HSL-based color tokens, glassmorphism utilities, Inter font via Google Fonts
- Custom scrollbars, micro-animations, and smooth transitions
- Strict Vanilla CSS — no Tailwind

**UI Components (`src/components/ui/`)**
- `Card`, `CardHeader`, `CardTitle`, `CardContent`
- `Input`, `Textarea`, `Select`, `Label`, `Button` (with `primary`, `secondary`, `outline` variants)

**Redux State (`hcpSlice.js`)**
- `fetchHcps` — loads HCP list from `/api/v1/hcp/professionals/`
- `createInteraction` — posts a new interaction log
- `chatWithAI` — sends user message to `/api/v1/hcp/chat/` and stores `parsedAiData` in Redux

**Interaction Form (`InteractionForm.jsx`)**
Fully controlled React component with fields for:
- HCP Name (dropdown populated from API)
- Interaction Type, Date, Time
- Attendees, Topics Discussed (Notes), Outcomes
- Materials Shared / Samples Distributed (rendered as a dynamic list)
- HCP Sentiment (radio buttons)
- Follow-up Actions

**Selective AI Merge Logic**
When the AI returns data, only fields with non-null values are updated in the form.
Saying "set the date to tomorrow" only updates the Date — HCP name, sentiment, notes etc. remain unchanged.

**AI Assistant Chat (`AiAssistantChat.jsx`)**
- Chat input that dispatches the `chatWithAI` thunk
- Shows loading state and errors inline
- On success, Redux `parsedAiData` triggers the selective form merge

---

## 🌐 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/v1/hcp/professionals/` | List all HCPs |
| `POST` | `/api/v1/hcp/professionals/` | Create HCP |
| `GET` | `/api/v1/hcp/professionals/{id}/` | Get HCP details |
| `PUT/PATCH` | `/api/v1/hcp/professionals/{id}/` | Update HCP |
| `DELETE` | `/api/v1/hcp/professionals/{id}/` | Delete HCP |
| `GET` | `/api/v1/hcp/interactions/` | List interactions |
| `POST` | `/api/v1/hcp/interactions/` | Log new interaction |
| `POST` | `/api/v1/hcp/chat/` | AI chat → structured extraction |
| `GET` | `/api/v1/hcp/health/` | Health check |

---