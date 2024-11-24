from django.urls import path
from . import views

urlpatterns = [
    path('', views.quiz_view, name='quiz'),
    path('submit/', views.submit_quiz, name='submit_quiz'),
]
