import json
import redis
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes
from .models import Prompt

# Initialize Redis connection (optional — graceful fallback if unavailable)
try:
    redis_client = redis.Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        decode_responses=True
    )
    redis_client.ping()
except Exception:
    redis_client = None


@extend_schema(
    summary="List all prompts or create a new prompt",
    description="GET: Returns a list of all prompts ordered by creation date (newest first). POST: Creates a new prompt with validation.",
    responses={
        200: {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "title": {"type": "string"},
                    "complexity": {"type": "integer"},
                    "created_at": {"type": "string", "format": "date-time"}
                }
            }
        },
        201: {
            "type": "object",
            "properties": {
                "id": {"type": "integer"},
                "title": {"type": "string"},
                "content": {"type": "string"},
                "complexity": {"type": "integer"},
                "created_at": {"type": "string", "format": "date-time"}
            }
        },
        400: {
            "type": "object",
            "properties": {
                "errors": {"type": "object"}
            }
        }
    },
    examples=[
        OpenApiExample(
            'Create Prompt Example',
            value={
                "title": "Write a Blog Post",
                "content": "Create an engaging blog post about artificial intelligence",
                "complexity": 5
            },
            request_only=True,
        ),
    ],
)
@csrf_exempt
def prompt_list(request):
    if request.method == 'GET':
        prompts = Prompt.objects.all()
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
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


@extend_schema(
    summary="Get prompt details",
    description="Returns detailed information about a specific prompt and increments its view count in Redis.",
    parameters=[
        OpenApiParameter(
            name='pk',
            type=OpenApiTypes.INT,
            location=OpenApiParameter.PATH,
            description='Prompt ID'
        ),
    ],
    responses={
        200: {
            "type": "object",
            "properties": {
                "id": {"type": "integer"},
                "title": {"type": "string"},
                "content": {"type": "string"},
                "complexity": {"type": "integer"},
                "created_at": {"type": "string", "format": "date-time"},
                "view_count": {"type": "integer", "description": "Number of times this prompt has been viewed"}
            }
        },
        404: {
            "type": "object",
            "properties": {
                "error": {"type": "string"}
            }
        }
    },
)
@csrf_exempt
def prompt_detail(request, pk):
    if request.method == 'GET':
        try:
            prompt = Prompt.objects.get(pk=pk)
            
            # Increment view count using Redis (primary) with PostgreSQL fallback
            # Redis provides fast, atomic counters for high-traffic scenarios
            if redis_client:
                try:
                    view_key = f'prompt:{pk}:views'
                    view_count = redis_client.incr(view_key)
                    # Sync to database periodically for persistence
                    prompt.view_count = view_count
                    prompt.save(update_fields=['view_count'])
                except Exception:
                    # Redis failed mid-request — fall back to database
                    from django.db.models import F
                    Prompt.objects.filter(pk=pk).update(view_count=F('view_count') + 1)
                    prompt.refresh_from_db()
                    view_count = prompt.view_count
            else:
                # No Redis available — use database directly
                from django.db.models import F
                Prompt.objects.filter(pk=pk).update(view_count=F('view_count') + 1)
                prompt.refresh_from_db()
                view_count = prompt.view_count
            
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
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
