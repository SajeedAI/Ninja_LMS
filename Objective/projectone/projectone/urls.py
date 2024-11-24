from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),           # Admin panel
    path('', include('appone.urls')),   # Include URLs from the quiz_app
]
