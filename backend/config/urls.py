"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from django.views.generic import TemplateView
from prompts.schema import get_openapi_schema
import yaml


def openapi_schema(request):
    """Return OpenAPI schema in JSON or YAML format"""
    schema = get_openapi_schema()
    if request.GET.get('format') == 'yaml':
        return JsonResponse(schema, content_type='application/x-yaml')
    return JsonResponse(schema)


def swagger_ui(request):
    """Serve Swagger UI"""
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>AI Prompt Library API - Swagger UI</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css">
        <style>
            body { margin: 0; }
        </style>
    </head>
    <body>
        <div id="swagger-ui"></div>
        <script src="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-standalone-preset.js"></script>
        <script>
            window.onload = function() {
                window.ui = SwaggerUIBundle({
                    url: '/api/schema/',
                    dom_id: '#swagger-ui',
                    deepLinking: true,
                    presets: [
                        SwaggerUIBundle.presets.apis,
                        SwaggerUIStandalonePreset
                    ],
                    plugins: [
                        SwaggerUIBundle.plugins.DownloadUrl
                    ],
                    layout: "StandaloneLayout"
                });
            };
        </script>
    </body>
    </html>
    """
    from django.http import HttpResponse
    return HttpResponse(html)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('prompts/', include('prompts.urls')),
    # OpenAPI schema
    path('api/schema/', openapi_schema, name='openapi-schema'),
    # Swagger UI
    path('docs/', swagger_ui, name='swagger-ui'),
]
