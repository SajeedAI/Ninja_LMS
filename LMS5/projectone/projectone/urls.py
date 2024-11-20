# my_django_project/urls.py

from django.contrib import admin
from django.urls import path, include  # Include allows us to reference app-level URLs
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),  # Admin panel URL
    path('', include('appone.urls')),  # Includes URLs from the 'users' app
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
