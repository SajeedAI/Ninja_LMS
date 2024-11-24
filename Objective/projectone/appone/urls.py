from django.urls import path
from .views import quiz_view

urlpatterns = [
    path('quiz/<int:question_id>/', quiz_view, name='quiz_view'),
]
