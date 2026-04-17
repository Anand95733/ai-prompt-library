<p align="center">
  <h1 align="center">✨ AI Prompt Library</h1>
  <p align="center">
    A production-grade full-stack application for managing and sharing AI prompts
    <br />
    Built with Angular 19 · Django 4.2 · PostgreSQL · Redis · Docker
  </p>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/build-passing-brightgreen?style=flat-square" alt="Build Status" />
  <img src="https://img.shields.io/badge/Angular-19-dd0031?style=flat-square&logo=angular" alt="Angular" />
  <img src="https://img.shields.io/badge/Django-4.2-092E20?style=flat-square&logo=django" alt="Django" />
  <img src="https://img.shields.io/badge/PostgreSQL-14-336791?style=flat-square&logo=postgresql&logoColor=white" alt="PostgreSQL" />
  <img src="https://img.shields.io/badge/Redis-7-DC382D?style=flat-square&logo=redis&logoColor=white" alt="Redis" />
  <img src="https://img.shields.io/badge/Docker-Compose-2496ED?style=flat-square&logo=docker&logoColor=white" alt="Docker" />
  <img src="https://img.shields.io/badge/license-MIT-blue?style=flat-square" alt="License" />
</p>

---

## 📸 Screenshots

| Prompt Library | Prompt Detail | Create Prompt |
|:-:|:-:|:-:|
| ![List View](docs/screenshots/list-view.png) | ![Detail View](docs/screenshots/detail-view.png) | ![Create Form](docs/screenshots/create-form.png) |

> **Note:** Add screenshots to `docs/screenshots/` after first deployment.

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                          Browser                                │
│                     http://localhost:4200                        │
└───────────────────────────┬─────────────────────────────────────┘
                            │ HTTP (Angular SPA)
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Angular 19 Frontend                           │
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│  │  List View   │  │ Detail View  │  │   Create Form        │  │
│  │  /prompts    │  │ /prompts/:id │  │   /add-prompt        │  │
│  └──────────────┘  └──────────────┘  └──────────────────────┘  │
│                            │                                    │
│                    PromptService (HttpClient)                    │
│                            │                                    │
│                   Proxy /api/* → backend:8000                   │
└───────────────────────────┬─────────────────────────────────────┘
                            │ REST API
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Django 4.2 Backend                            │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                    API Endpoints                          │  │
│  │  GET  /prompts/       → List all prompts                 │  │
│  │  POST /prompts/       → Create new prompt                │  │
│  │  GET  /prompts/:id/   → Detail + increment views         │  │
│  └──────────────────────────────────────────────────────────┘  │
│                    │                      │                      │
│                    ▼                      ▼                      │
│        ┌───────────────────┐   ┌───────────────────┐           │
│        │   PostgreSQL 14   │   │    Redis 7         │           │
│        │   (prompt data)   │   │  (view counters)   │           │
│        └───────────────────┘   └───────────────────┘           │
└─────────────────────────────────────────────────────────────────┘
```

---

## ✨ Features

- **Browse Prompts** — Responsive grid with glassmorphism cards, complexity badges (green/orange/red), hover animations
- **Prompt Details** — Full content view with live Redis-backed view counter
- **Create Prompts** — Reactive form with real-time client + server validation
- **Premium UI** — Dark theme, glass morphism effects, gradient text, smooth transitions
- **Loading Skeletons** — Pulse-animated placeholders during data fetch
- **Swagger Docs** — Interactive API documentation at `/docs/`
- **Dockerized** — One-command setup with Docker Compose

---

## 🛠️ Tech Stack

| Layer | Technology | Version |
|-------|-----------|---------|
| **Frontend** | Angular (Standalone Components) | 19.0 |
| **Backend** | Django (Plain Views, no DRF serializers) | 4.2 |
| **Database** | PostgreSQL | 14 |
| **Cache** | Redis | 7 |
| **Docs** | Swagger UI + OpenAPI 3.0 | — |
| **Container** | Docker Compose | 2.x |
| **Deploy (BE)** | Render.com (Free Tier) | — |
| **Deploy (FE)** | Vercel | — |

---

## 🚀 Quick Start

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/) & Docker Compose
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR-USERNAME/ai-prompt-library.git
cd ai-prompt-library
```

### 2. Start All Services

```bash
docker compose up --build
```

### 3. Access the Application

| Service | URL |
|---------|-----|
| **Frontend** | [http://localhost:4200](http://localhost:4200) |
| **Backend API** | [http://localhost:8000](http://localhost:8000) |
| **Swagger Docs** | [http://localhost:8000/docs/](http://localhost:8000/docs/) |
| **Django Admin** | [http://localhost:8000/admin/](http://localhost:8000/admin/) |

### 4. Create Superuser (Optional)

```bash
docker compose exec backend python manage.py createsuperuser
```

---

## 💻 Local Development (Without Docker)

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate       # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Set environment variables
export POSTGRES_DB=promptdb
export POSTGRES_USER=promptuser
export POSTGRES_PASSWORD=promptpass
export POSTGRES_HOST=localhost
export REDIS_HOST=localhost
export DEBUG=True

python manage.py migrate
python manage.py runserver
```

### Frontend

```bash
cd frontend
npm install
npm start                      # Serves at http://localhost:4200
```

> The Angular dev server proxies `/api/*` requests to `http://backend:8000` via `proxy.conf.json`.

---

## 📡 API Documentation

### Endpoints

| Method | Endpoint | Description | Request Body | Response |
|--------|----------|-------------|-------------|----------|
| `GET` | `/prompts/` | List all prompts | — | `[{id, title, complexity, created_at}]` |
| `POST` | `/prompts/` | Create a prompt | `{title, content, complexity}` | `{id, title, content, complexity, created_at}` |
| `GET` | `/prompts/:id/` | Get prompt detail | — | `{id, title, content, complexity, created_at, view_count}` |

### Validation Rules

| Field | Rule |
|-------|------|
| `title` | Required, minimum 3 characters |
| `content` | Required, minimum 20 characters |
| `complexity` | Required, integer between 1–10 |

### Example: Create a Prompt

```bash
curl -X POST http://localhost:8000/prompts/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Write a Blog Post",
    "content": "Create an engaging blog post about artificial intelligence and its impact",
    "complexity": 5
  }'
```

### Example Response

```json
{
  "id": 1,
  "title": "Write a Blog Post",
  "content": "Create an engaging blog post about artificial intelligence and its impact",
  "complexity": 5,
  "created_at": "2026-04-17T02:00:00.000000+00:00"
}
```

---

## 🚢 Deployment

### Backend → Render.com (Free Tier)

1. Push your repo to GitHub.
2. Go to [Render Dashboard](https://dashboard.render.com/) → **New** → **Blueprint**.
3. Connect your GitHub repo.
4. Render reads `backend/render.yaml` and provisions:
   - **Web Service** (Python 3.11, Gunicorn)
   - **PostgreSQL** (Free tier)
5. Copy your backend URL: `https://YOUR-APP.onrender.com`

### Frontend → Vercel

1. Go to [Vercel Dashboard](https://vercel.com/new) → Import your repo.
2. Set **Root Directory** to `frontend`.
3. Update `frontend/src/environments/environment.prod.ts`:
   ```typescript
   export const environment = {
     production: true,
     apiUrl: 'https://YOUR-APP.onrender.com/prompts'
   };
   ```
4. Update the proxy URL in `frontend/vercel.json`:
   ```json
   { "source": "/api/(.*)", "destination": "https://YOUR-APP.onrender.com/$1" }
   ```
5. Deploy. Vercel auto-detects Angular and runs `npm run build`.

---

## 📂 Project Structure

```
ai-prompt-library/
├── backend/                        # Django 4.2 REST API
│   ├── config/
│   │   ├── settings.py             # DB, Redis, CORS config
│   │   ├── urls.py                 # Root URLs + Swagger
│   │   ├── wsgi.py                 # WSGI entry point
│   │   └── asgi.py                 # ASGI entry point
│   ├── prompts/
│   │   ├── models.py               # Prompt model (title, content, complexity)
│   │   ├── views.py                # API views (list, create, detail)
│   │   ├── schema.py               # OpenAPI 3.0 schema
│   │   ├── urls.py                 # App URL routing
│   │   └── admin.py                # Django Admin config
│   ├── render.yaml                 # Render.com deployment blueprint
│   ├── requirements.txt            # Python dependencies
│   └── Dockerfile                  # Backend container
│
├── frontend/                       # Angular 19 SPA
│   ├── src/
│   │   ├── app/
│   │   │   ├── components/
│   │   │   │   ├── prompt-list/    # Grid view with cards
│   │   │   │   ├── prompt-detail/  # Detail view with view counter
│   │   │   │   └── add-prompt/     # Reactive form with validation
│   │   │   ├── services/
│   │   │   │   └── prompt.service.ts   # HTTP client + environment URL
│   │   │   ├── app.component.ts    # Root component (header, nav)
│   │   │   └── app.routes.ts       # Client-side routing
│   │   ├── environments/
│   │   │   ├── environment.ts      # Dev config (proxy)
│   │   │   └── environment.prod.ts # Prod config (direct URL)
│   │   ├── styles.css              # Global dark theme
│   │   ├── main.ts                 # Bootstrap
│   │   └── proxy.conf.json         # Dev server API proxy
│   ├── vercel.json                 # Vercel deployment config
│   ├── angular.json                # Angular CLI config
│   ├── package.json                # npm dependencies
│   └── Dockerfile                  # Frontend container
│
├── docker-compose.yml              # Multi-container orchestration
├── .env                            # Environment variables
├── .gitignore                      # Git ignore rules
└── README.md                       # This file
```

---

## 🧪 Testing

### Frontend (Browser)

```
✅ Homepage loads at /prompts with prompt grid
✅ Prompt cards show title, complexity badge, date
✅ Complexity badges colored: green (1-3), orange (4-6), red (7-10)
✅ Card hover lifts with indigo glow animation
✅ Click card → navigates to /prompts/:id detail page
✅ Detail shows full content, view count, complexity badge
✅ View count increments on each visit (Redis-backed)
✅ "← Back to prompts" navigation works on all pages
✅ Create form validates: title (≥3), content (≥20), complexity (1-10)
✅ Successful creation redirects to new prompt detail
✅ Invalid prompt ID shows "Prompt not found" error state
✅ Loading skeletons display during data fetch
```

### Backend (curl)

```bash
# List prompts
curl http://localhost:8000/prompts/

# Create prompt
curl -X POST http://localhost:8000/prompts/ \
  -H "Content-Type: application/json" \
  -d '{"title": "Test", "content": "Valid content over twenty chars", "complexity": 5}'

# Get detail (view count increments)
curl http://localhost:8000/prompts/1/
```

---

## 📄 License

This project is licensed under the MIT License.

---

<p align="center">
  Built with ❤️ using Angular 19 + Django 4.2
</p>
