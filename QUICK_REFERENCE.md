# Quick Reference Card

## 🌐 Access URLs

| Service | URL | Purpose |
|---------|-----|---------|
| **Frontend** | http://localhost:4200 | Angular app |
| **Backend API** | http://localhost:8000 | Django REST API |
| **Admin Panel** | http://localhost:8000/admin | Django admin |

## 📚 Documentation Files

1. **COMPLETE_PROJECT_GUIDE.md** - Start here! Complete overview
2. **FRONTEND_WALKTHROUGH.md** - Angular step-by-step guide
3. **BACKEND_API_DOCS.md** - API endpoints & examples
4. **DATABASE_PGADMIN_GUIDE.md** - Database access guide
5. **README.md** - Quick start instructions

## 🚀 Common Commands

```bash
# Start all services
docker compose up

# Start in background
docker compose up -d

# Stop all services
docker compose down

# View logs
docker compose logs -f

# Restart a service
docker compose restart backend

# Rebuild and start
docker compose up --build

# Create superuser
docker compose exec backend python manage.py createsuperuser

# Access PostgreSQL
docker compose exec db psql -U promptuser -d promptdb

# Access Redis
docker compose exec redis redis-cli

# Run Django shell
docker compose exec backend python manage.py shell
```

## 🔌 API Endpoints

```bash
# List all prompts
GET http://localhost:8000/prompts/

# Create prompt
POST http://localhost:8000/prompts/
Body: {"title": "...", "content": "...", "complexity": 5}

# Get prompt detail (increments view count)
GET http://localhost:8000/prompts/1/
```

## 🗄️ Database Info

```
Host: localhost (or 'db' from Docker)
Port: 5432
Database: promptdb
Username: promptuser
Password: promptpass
```

## 📊 Redis Commands

```bash
# Connect
docker compose exec redis redis-cli

# View all keys
KEYS *

# Get view count
GET prompt:1:views

# Set view count
SET prompt:1:views 100

# Increment
INCR prompt:1:views
```

## 🎨 Frontend Routes

```
/                  → Redirects to /prompts
/prompts           → List all prompts
/prompts/:id       → View prompt detail
/add-prompt        → Create new prompt
```

## 🧪 Test Data

```sql
-- Insert test prompts
INSERT INTO prompts_prompt (title, content, complexity, created_at)
VALUES 
  ('Write marketing email', 'Create compelling email for product launch', 4, NOW()),
  ('Generate SQL query', 'Convert natural language to SQL', 7, NOW()),
  ('Write a poem', 'Create haiku about technology', 2, NOW());
```

## 🐛 Troubleshooting

```bash
# Check service status
docker compose ps

# View logs
docker compose logs backend
docker compose logs frontend
docker compose logs db

# Restart everything
docker compose down
docker compose up --build

# Check database connection
docker compose exec backend python manage.py dbshell
```

## 📁 Key Files

```
frontend/src/app/
├── components/
│   ├── prompt-list/          # Browse prompts
│   ├── prompt-detail/        # View single prompt
│   └── add-prompt/           # Create prompt
└── services/
    └── prompt.service.ts     # API calls

backend/prompts/
├── models.py                 # Prompt model
├── views.py                  # API endpoints
└── urls.py                   # URL routing

docker-compose.yml            # Container config
.env                          # Environment variables
```

## ✅ Health Check

```bash
# All services running?
docker compose ps

# Frontend accessible?
curl http://localhost:4200

# Backend accessible?
curl http://localhost:8000/prompts/

# Database accessible?
docker compose exec db pg_isready -U promptuser

# Redis accessible?
docker compose exec redis redis-cli ping
```

## 🎯 Next Steps

1. ✅ Read **COMPLETE_PROJECT_GUIDE.md**
2. ✅ Open http://localhost:4200 in browser
3. ✅ Browse prompts
4. ✅ Create a new prompt
5. ✅ View prompt detail (watch view count!)
6. ✅ Read **FRONTEND_WALKTHROUGH.md**
7. ✅ Read **BACKEND_API_DOCS.md**
8. ✅ Connect to database with pgAdmin

## 💡 Pro Tips

- Use Chrome DevTools Network tab to see API calls
- Install Angular DevTools extension for debugging
- Use `docker compose logs -f` to follow logs in real-time
- Check Redis view counts: `docker compose exec redis redis-cli KEYS prompt:*:views`
- Use Django admin for quick data management
