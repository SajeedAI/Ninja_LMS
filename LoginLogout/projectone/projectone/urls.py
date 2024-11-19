# my_django_project/urls.py

from django.contrib import admin
from django.urls import path, include  # Include allows us to reference app-level URLs

urlpatterns = [
    path('admin/', admin.site.urls),  # Admin panel URL
    path('users/', include('appone.urls')),  # Includes URLs from the 'users' app
    # Any other app URL paths would be included here as well
]
