from pathlib import Path

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.http import JsonResponse, FileResponse, Http404
from django.urls import path, include, re_path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

FRONTEND_DIR = Path(settings.BASE_DIR) / 'frontend'


def health(request):
    """Liveness probe for the load balancer and `docker compose ps`.

    Deliberately does not touch the database or Redis: this answers "is
    gunicorn serving requests", and a check that fails on a slow query
    gets the whole site restarted for no reason.
    """
    return JsonResponse({'status': 'ok'})


def serve_frontend(request, path='index.html'):
    """Serve frontend HTML/CSS/JS files directly from the frontend/ directory."""
    if not path:
        path = 'index.html'
    file_path = FRONTEND_DIR / path
    if file_path.exists() and file_path.is_file():
        return FileResponse(open(file_path, 'rb'))
    # Fallback to index.html
    index = FRONTEND_DIR / 'index.html'
    if index.exists():
        return FileResponse(open(index, 'rb'))
    raise Http404


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/health/', health, name='health'),
    path('api/v1/', include('accounts.urls')),
    path('api/v1/', include('movies.urls')),
    path('api/v1/', include('halls.urls')),
    path('api/v1/', include('showtimes.urls')),
    path('api/v1/', include('reservations.urls')),
    path('api/v1/', include('payments.urls')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
]

if settings.DEBUG or settings.EXPOSE_API_DOCS:
    urlpatterns += [
        path('api-auth/', include('rest_framework.urls')),
        path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # Serve frontend assets (css, js, img) on the same origin as the API
    urlpatterns += static('/css/', document_root=FRONTEND_DIR / 'css')
    urlpatterns += static('/js/', document_root=FRONTEND_DIR / 'js')
    urlpatterns += static('/img/', document_root=FRONTEND_DIR / 'img')
    urlpatterns += [
        # Named HTML pages e.g. /movies.html, /signin.html
        re_path(r'^(?P<path>[a-zA-Z0-9_\-]+\.html)$', serve_frontend),
        # Root / → index.html
        path('', serve_frontend),
    ]
