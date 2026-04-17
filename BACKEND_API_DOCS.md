# Backend API Documentation - AI Prompt Library

## 🎯 Overview
Django 4.2 REST API with plain views (no Django REST Framework), PostgreSQL database, and Redis caching for view counts.

## 📁 Project Structure

```
backend/
├── config/
│   ├── settings.py          # Django settings
│   ├── urls.py              # Root URL config
│   ├── wsgi.py              # WSGI application
│   └── asgi.py              # ASGI application
├── prompts/
│   ├── models.py            # Prompt model
│   ├── views.py             # API endpoints
│   ├── urls.py              # App URL config
│   ├── admin.py             # Django admin config
│   └── apps.py              # App configuration
├── manage.py                # Django CLI
└── requirements.txt         # Python dependencies
```

---

## 🗄️ Database Model

### Prompt Model

**File**: `backend/prompts/models.py`

```python
from django.db import models

class Prompt(models.Model):
    id = models.AutoField(primary_key=True)           # Auto-increment PK
    title = models.CharField(max_length=255)          # Prompt title
    content = models.TextField()                      # Prompt content
    complexity = models.IntegerField()                # 1-10 rating
    created_at = models.DateTimeField(auto_now_add=True)  # Auto timestamp

    class Meta:
        ordering = ['-created_at']  # Newest first

    def __str__(self):
        return self.title
```

**Database Table**: `prompts_prompt`

**Columns**:
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTO INCREMENT | Unique identifier |
| title | VARCHAR(255) | NOT NULL | Prompt title |
| content | TEXT | NOT NULL | Full prompt content |
| complexity | INTEGER | NOT NULL | Difficulty rating (1-10) |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Creation timestamp |

---

## 🔌 API Endpoints

### Base URL
```
http://localhost:8000
```

---

### 1. List All Prompts

**Endpoint**: `GET /prompts/`

**Description**: Retrieve all prompts (without content, for list view)

**Request**:
```http
GET /prompts/ HTTP/1.1
Host: localhost:8000
```

**Response**: `200 OK`
```json
[
  {
    "id": 1,
    "title": "Write a product description",
    "complexity": 3,
    "created_at": "2026-04-17T00:43:38.123456Z"
  },
  {
    "id": 2,
    "title": "Generate SQL query from natural language",
    "complexity": 7,
    "created_at": "2026-04-17T00:45:12.789012Z"
  }
]
```

**Response Fields**:
- `id` (integer): Prompt ID
- `title` (string): Prompt title
- `complexity` (integer): Difficulty rating (1-10)
- `created_at` (string): ISO 8601 timestamp

**Code Implementation**:
```python
@csrf_exempt
def prompt_list(request):
    if request.method == 'GET':
        prompts = Prompt.objects.all()  # Ordered by -created_at
        data = [
            {
                'id': p.id,
                'title': p.title,
                'complexity': p.complexity,
                'created_at': p.created_at.isoformat()
            }
            for p in prompts
        ]
        return JsonResponse(data, safe=False)
```

---

### 2. Create New Prompt

**Endpoint**: `POST /prompts/`

**Description**: Create a new prompt with validation

**Request**:
```http
POST /prompts/ HTTP/1.1
Host: localhost:8000
Content-Type: application/json

{
  "title": "Write a blog post about AI",
  "content": "Create a comprehensive blog post about the impact of AI on modern society",
  "complexity": 5
}
```

**Validation Rules**:
- `title`: Required, minimum 3 characters
- `content`: Required, minimum 20 characters
- `complexity`: Required, integer between 1-10

**Success Response**: `201 Created`
```json
{
  "id": 3,
  "title": "Write a blog post about AI",
  "content": "Create a comprehensive blog post about the impact of AI on modern society",
  "complexity": 5,
  "created_at": "2026-04-17T01:23:45.678901Z"
}
```

**Error Response**: `400 Bad Request`
```json
{
  "errors": {
    "title": "Title must be at least 3 characters",
    "content": "Content must be at least 20 characters",
    "complexity": "Complexity must be between 1 and 10"
  }
}
```

**Code Implementation**:
```python
@csrf_exempt
def prompt_list(request):
    elif request.method == 'POST':
        try:
            body = json.loads(request.body)
            title = body.get('title', '').strip()
            content = body.get('content', '').strip()
            complexity = body.get('complexity')
            
            # Validation
            errors = {}
            if len(title) < 3:
                errors['title'] = 'Title must be at least 3 characters'
            if len(content) < 20:
                errors['content'] = 'Content must be at least 20 characters'
            if not isinstance(complexity, int) or complexity < 1 or complexity > 10:
                errors['complexity'] = 'Complexity must be between 1 and 10'
            
            if errors:
                return JsonResponse({'errors': errors}, status=400)
            
            # Create prompt
            prompt = Prompt.objects.create(
                title=title,
                content=content,
                complexity=complexity
            )
            
            return JsonResponse({
                'id': prompt.id,
                'title': prompt.title,
                'content': prompt.content,
                'complexity': prompt.complexity,
                'created_at': prompt.created_at.isoformat()
            }, status=201)
            
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
```

---

### 3. Get Prompt Detail

**Endpoint**: `GET /prompts/<id>/`

**Description**: Retrieve single prompt with full content and increment view count

**Request**:
```http
GET /prompts/1/ HTTP/1.1
Host: localhost:8000
```

**Response**: `200 OK`
```json
{
  "id": 1,
  "title": "Write a product description",
  "content": "Create a compelling product description for a new smartphone that highlights its key features and benefits",
  "complexity": 3,
  "created_at": "2026-04-17T00:43:38.123456Z",
  "view_count": 5
}
```

**Response Fields**:
- `id` (integer): Prompt ID
- `title` (string): Prompt title
- `content` (string): Full prompt content
- `complexity` (integer): Difficulty rating (1-10)
- `created_at` (string): ISO 8601 timestamp
- `view_count` (integer): Number of times viewed (from Redis)

**Error Response**: `404 Not Found`
```json
{
  "error": "Prompt not found"
}
```

**Code Implementation**:
```python
@csrf_exempt
def prompt_detail(request, pk):
    if request.method == 'GET':
        try:
            prompt = Prompt.objects.get(pk=pk)
            
            # Increment view count in Redis
            view_key = f'prompt:{pk}:views'
            view_count = redis_client.incr(view_key)
            
            return JsonResponse({
                'id': prompt.id,
                'title': prompt.title,
                'content': prompt.content,
                'complexity': prompt.complexity,
                'created_at': prompt.created_at.isoformat(),
                'view_count': view_count
            })
        except Prompt.DoesNotExist:
            return JsonResponse({'error': 'Prompt not found'}, status=404)
```

**Redis View Counting**:
- Key format: `prompt:{id}:views`
- Example: `prompt:1:views` → `5`
- `INCR` command atomically increments counter
- Persists across server restarts
- Fast O(1) operation

---

## 🔧 Configuration

### Database Configuration

**File**: `backend/config/settings.py`

```python
import os
import dj_database_url

# Support both local Docker and Render deployment
if os.environ.get('DATABASE_URL'):
    # Production (Render, Heroku, etc.)
    DATABASES = {
        'default': dj_database_url.parse(os.environ['DATABASE_URL'])
    }
else:
    # Local Docker development
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ.get('POSTGRES_DB', 'promptdb'),
            'USER': os.environ.get('POSTGRES_USER', 'promptuser'),
            'PASSWORD': os.environ.get('POSTGRES_PASSWORD', 'promptpass'),
            'HOST': os.environ.get('POSTGRES_HOST', 'localhost'),
            'PORT': os.environ.get('POSTGRES_PORT', '5432'),
        }
    }
```

**Environment Variables**:
```bash
# Local Docker
POSTGRES_DB=promptdb
POSTGRES_USER=promptuser
POSTGRES_PASSWORD=promptpass
POSTGRES_HOST=db
POSTGRES_PORT=5432

# Production (Render)
DATABASE_URL=postgresql://user:pass@host:5432/dbname
```

---

### Redis Configuration

```python
import redis
from django.conf import settings

redis_client = redis.Redis(
    host=settings.REDIS_HOST,      # 'redis' in Docker
    port=settings.REDIS_PORT,      # 6379
    decode_responses=True          # Return strings, not bytes
)
```

**Environment Variables**:
```bash
REDIS_HOST=redis
REDIS_PORT=6379
```

---

### CORS Configuration

```python
INSTALLED_APPS = [
    ...
    'corsheaders',
]

MIDDLEWARE = [
    ...
    'corsheaders.middleware.CorsMiddleware',
    ...
]

# Allow all origins (development only!)
CORS_ALLOW_ALL_ORIGINS = True
```

**Production**: Restrict to specific origins
```python
CORS_ALLOWED_ORIGINS = [
    "https://your-frontend-domain.com",
]
```

---

## 🧪 Testing the API

### Using cURL

#### 1. List All Prompts
```bash
curl http://localhost:8000/prompts/
```

#### 2. Create New Prompt
```bash
curl -X POST http://localhost:8000/prompts/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Test Prompt",
    "content": "This is a test prompt with enough content to pass validation",
    "complexity": 5
  }'
```

#### 3. Get Prompt Detail
```bash
curl http://localhost:8000/prompts/1/
```

#### 4. Test Validation Errors
```bash
# Title too short
curl -X POST http://localhost:8000/prompts/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "ab",
    "content": "This is a test prompt with enough content",
    "complexity": 5
  }'

# Content too short
curl -X POST http://localhost:8000/prompts/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Test Prompt",
    "content": "short",
    "complexity": 5
  }'

# Invalid complexity
curl -X POST http://localhost:8000/prompts/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Test Prompt",
    "content": "This is a test prompt with enough content",
    "complexity": 15
  }'
```

---

### Using Python Requests

```python
import requests

BASE_URL = "http://localhost:8000"

# List all prompts
response = requests.get(f"{BASE_URL}/prompts/")
prompts = response.json()
print(f"Found {len(prompts)} prompts")

# Create new prompt
new_prompt = {
    "title": "Python API Test",
    "content": "This prompt was created via Python requests library",
    "complexity": 6
}
response = requests.post(f"{BASE_URL}/prompts/", json=new_prompt)
created = response.json()
print(f"Created prompt ID: {created['id']}")

# Get prompt detail (increments view count)
prompt_id = created['id']
response = requests.get(f"{BASE_URL}/prompts/{prompt_id}/")
detail = response.json()
print(f"View count: {detail['view_count']}")

# Get again (view count should increment)
response = requests.get(f"{BASE_URL}/prompts/{prompt_id}/")
detail = response.json()
print(f"View count after second request: {detail['view_count']}")
```

---

## 🗄️ Database Migrations

### Initial Migration
```bash
# Create migration files
python manage.py makemigrations

# Apply migrations
python manage.py migrate
```

### Migration Files
```
backend/prompts/migrations/
├── __init__.py
└── 0001_initial.py  # Creates prompts_prompt table
```

### SQL Generated
```sql
CREATE TABLE "prompts_prompt" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "title" varchar(255) NOT NULL,
    "content" text NOT NULL,
    "complexity" integer NOT NULL,
    "created_at" datetime NOT NULL
);

CREATE INDEX "prompts_prompt_created_at_idx" 
ON "prompts_prompt" ("created_at" DESC);
```

---

## 🔐 Admin Interface

### Configuration

**File**: `backend/prompts/admin.py`

```python
from django.contrib import admin
from .models import Prompt

@admin.register(Prompt)
class PromptAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'complexity', 'created_at')
    list_filter = ('complexity', 'created_at')
    search_fields = ('title', 'content')
```

### Access Admin
```
URL: http://localhost:8000/admin
```

### Create Superuser
```bash
docker compose exec backend python manage.py createsuperuser

# Enter:
# Username: admin
# Email: admin@example.com
# Password: admin123
```

### Admin Features
- View all prompts in table
- Filter by complexity and date
- Search by title/content
- Add/edit/delete prompts
- Bulk actions

---

## 📊 Redis Data Structure

### View Counts

**Key Pattern**: `prompt:{id}:views`

**Examples**:
```
prompt:1:views → "5"
prompt:2:views → "12"
prompt:3:views → "3"
```

### Redis Commands

```bash
# Connect to Redis
docker compose exec redis redis-cli

# Get view count
GET prompt:1:views

# Set view count manually
SET prompt:1:views 100

# Increment view count
INCR prompt:1:views

# Get all prompt view keys
KEYS prompt:*:views

# Delete view count
DEL prompt:1:views

# Get all keys
KEYS *
```

---

## 🚀 Deployment

### Local Development
```bash
# Start all services
docker compose up

# Run migrations
docker compose exec backend python manage.py migrate

# Create superuser
docker compose exec backend python manage.py createsuperuser
```

### Production (Render)

**Environment Variables**:
```bash
DATABASE_URL=postgresql://...
REDIS_HOST=redis-hostname
REDIS_PORT=6379
DJANGO_SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=your-domain.com
```

**Build Command**:
```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
```

**Start Command**:
```bash
gunicorn config.wsgi:application --bind 0.0.0.0:$PORT
```

---

## 🔍 Debugging

### View Logs
```bash
# All services
docker compose logs

# Backend only
docker compose logs backend

# Follow logs
docker compose logs -f backend
```

### Django Shell
```bash
docker compose exec backend python manage.py shell

# In shell:
from prompts.models import Prompt

# Get all prompts
prompts = Prompt.objects.all()
for p in prompts:
    print(f"{p.id}: {p.title}")

# Create prompt
Prompt.objects.create(
    title="Shell Test",
    content="Created from Django shell",
    complexity=5
)

# Get prompt
prompt = Prompt.objects.get(id=1)
print(prompt.title)
```

### Check Redis
```bash
docker compose exec redis redis-cli

# List all keys
KEYS *

# Get view count
GET prompt:1:views

# Monitor commands
MONITOR
```

---

## 📦 Dependencies

**File**: `backend/requirements.txt`

```
django>=4.2              # Web framework
psycopg2-binary          # PostgreSQL adapter
redis                    # Redis client
django-cors-headers      # CORS middleware
gunicorn                 # WSGI server
dj-database-url          # Database URL parser
```

---

## 🎯 Key Concepts

### 1. Plain Views (No DRF)
- Use `JsonResponse` directly
- Manual JSON parsing
- Custom validation logic
- Lightweight and simple

### 2. CSRF Exemption
```python
@csrf_exempt  # Disable CSRF for API endpoints
def prompt_list(request):
    ...
```

### 3. Redis Atomic Operations
```python
# INCR is atomic - safe for concurrent requests
view_count = redis_client.incr(view_key)
```

### 4. Database URL Parsing
```python
# Automatically parse DATABASE_URL
DATABASES = {
    'default': dj_database_url.parse(os.environ['DATABASE_URL'])
}
```

---

## 🐛 Common Issues

### 1. Database Connection Error
```
django.db.utils.OperationalError: could not connect to server
```
**Solution**: Ensure PostgreSQL is running and wait-for-it logic is working

### 2. Redis Connection Error
```
redis.exceptions.ConnectionError: Error connecting to Redis
```
**Solution**: Check Redis container is running and REDIS_HOST is correct

### 3. CORS Error
```
Access to fetch at 'http://localhost:8000/prompts/' has been blocked by CORS policy
```
**Solution**: Ensure `django-cors-headers` is installed and configured

---

## 📚 Additional Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Redis Documentation](https://redis.io/documentation)
- [Gunicorn Documentation](https://docs.gunicorn.org/)
