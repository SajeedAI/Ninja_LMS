# from django.urls import path
# from django.contrib.auth import views as auth_views
# from . import views

# urlpatterns = [
#     path('register/', views.register_user, name='register'),
#     path('home/', views.home, name='home'),
#     path('login/', auth_views.LoginView.as_view(), name='login'),  # Django's built-in login view
#     path('modules/', views.module_list, name='module_list'),
#     path('modules/add/', views.module_add, name='module_add'),
#     path('modules/<int:pk>/edit/', views.module_edit, name='module_edit'),
#     path('modules/<int:pk>/delete/', views.module_delete, name='module_delete'),
#     path('modules/<int:pk>/', views.module_detail, name='module_detail'),
#     path('user_assignments/', views.user_assignment_list, name='user_assignment_list'),
#     path('user_assignments/add/', views.user_assignment_add, name='user_assignment_add'),
#     path('user_assignment/edit/<int:pk>/', views.user_assignment_edit, name='user_assignment_edit'),  # Correct URL pattern
#     path('user_assignment/delete/<int:pk>/', views.user_assignment_delete, name='user_assignment_delete'),
#     path('user_assignments/<int:pk>/delete/', views.user_assignment_delete, name='user_assignment_delete'),
#     path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
#     path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
# ]

# CBV
from django.urls import path
from .views import (
    UserRegisterView,
    ModuleListView, ModuleDetailView, ModuleCreateView, ModuleUpdateView, ModuleDeleteView,
    UserAssignmentListView, UserAssignmentCreateView, UserAssignmentUpdateView, UserAssignmentDeleteView, home
)

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('modules/', ModuleListView.as_view(), name='module_list'),
    path('modules/<int:pk>/', ModuleDetailView.as_view(), name='module_detail'),
    path('modules/add/', ModuleCreateView.as_view(), name='module_add'),
    path('modules/<int:pk>/edit/', ModuleUpdateView.as_view(), name='module_edit'),
    path('modules/<int:pk>/delete/', ModuleDeleteView.as_view(), name='module_delete'),
    path('user_assignments/', UserAssignmentListView.as_view(), name='user_assignment_list'),
    path('user_assignments/add/', UserAssignmentCreateView.as_view(), name='user_assignment_add'),
    path('user_assignments/<int:pk>/edit/', UserAssignmentUpdateView.as_view(), name='user_assignment_edit'),
    path('user_assignments/<int:pk>/delete/', UserAssignmentDeleteView.as_view(), name='user_assignment_delete'),
    path('home/', home, name='home'),
]
