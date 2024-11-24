from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('test_overview/', views.test_overview, name='test_overview'),
    path('available-tests/', views.available_tests, name='available_tests'),
    path('profile/', views.profile_view, name='profile'),  # Define the profile URL
    path('week/<int:week_id>/', views.take_test, name='take_test'),
    path('week/<int:week_id>/results/', views.test_results, name='test_results'),
    path('', views.custom_login, name='login'),
    path('accounts/logout/', views.custom_logout, name='logout'),
   
]
