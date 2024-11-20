from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Module CRUD
    path('modules/', views.module_list, name='module_list'),
    path('modules/<int:module_id>/submodules/', views.submodule_list, name='submodule_list'),
    path('modules/module_form/', views.module_create, name='module_create'),
    path('module/update/<int:pk>/', views.module_update, name='module_update'),
    path('module/delete/<int:pk>/', views.module_delete, name='module_delete'),
    
    # SubModule CRUD
    path('submodules/<int:module_id>/', views.submodule_list, name='submodule_list'),
    path('submodules/create/<int:module_id>/', views.submodule_create, name='submodule_create'),
    path('modules/<int:module_id>/submodules/', views.submodule_list, name='submodule_list'),
    path('submodules/<int:pk>/edit/', views.submodule_update, name='submodule_update'),
    path('submodules/<int:pk>/delete/', views.submodule_delete, name='submodule_delete'),
   
    # UserAssignment CRUD
    path('assignments/user_assignment_list/', views.user_assignment_list, name='user_assignment_list'),
    path('assignments/user_assignment_set/', views.user_assignment_set, name='user_assignment_set'),
    path('assignments/<int:pk>/delete/', views.user_assignment_delete, name='user_assignment_delete'),
    path('register/', views.register_user, name='register'),
    # path('user-assignments/', views.user_assignments, name='user_assignments'),

    # registration
    path('register/', views.register_user, name='register'),
    path('manage-users/', views.manage_users, name='manage_users'),
    path('edit-user/<int:user_id>/', views.edit_user, name='edit_user'),
    path('delete-user/<int:user_id>/', views.delete_user, name='delete_user'),

    path('home/', views.home, name='home'),

    path('', auth_views.LoginView.as_view(), name='login'),
    
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),

]