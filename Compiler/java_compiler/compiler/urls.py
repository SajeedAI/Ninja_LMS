from django.urls import path
from . import views

urlpatterns = [
    path('run_code/', views.run_java_code, name='run_java_code'),
]
