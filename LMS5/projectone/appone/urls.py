from django.urls import path, include
from .views import (
    ModuleListView, 
    ModuleCreateView, 
    ModuleUpdateView, 
    ModuleDeleteView,
    SubModuleCreateView, SubModuleUpdateView, SubModuleDeleteView, SubmoduleListView,
    UserAssignmentListView, UserAssignmentDeleteView, UserAssignmentSetView,
    RegisterUserView, ManageUsersView, EditUserView, DeleteUserView, HomeView, ModuleDetailView
)
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('modules/', ModuleListView.as_view(), name='module_list'),
    path('modules/create/', ModuleCreateView.as_view(), name='module_create'),
    path('modules/update/<int:pk>/', ModuleUpdateView.as_view(), name='module_update'),
    path('modules/delete/<int:pk>/', ModuleDeleteView.as_view(), name='module_delete'),
    path('module/<int:pk>/', ModuleDetailView.as_view(), name='module_detail'),

    path('module/<int:module_id>/submodules/', SubmoduleListView.as_view(), name='submodule_list'),
    path('submodule/create/<int:module_id>/', SubModuleCreateView.as_view(), name='submodule_create'),
    path('submodule/update/<int:pk>/', SubModuleUpdateView.as_view(), name='submodule_update'),
    path('submodule/delete/<int:pk>/', SubModuleDeleteView.as_view(), name='submodule_delete'),

    path('user-assignment/list/', UserAssignmentListView.as_view(), name='user_assignment_list'),
    path('user-assignment/set/', UserAssignmentSetView.as_view(), name='user_assignment_set'),
    path('user_assignment/delete/<int:pk>/', UserAssignmentDeleteView.as_view(), name='user_assignment_delete'),
   
    path('register/', RegisterUserView.as_view(), name='register'),
    path('manage_users/', ManageUsersView.as_view(), name='manage_users'),
    path('manage_users/edit/<int:pk>/', EditUserView.as_view(), name='edit_user'),
    path('manage_users/delete/<int:pk>/', DeleteUserView.as_view(), name='delete_user'),
    
    path('home/', HomeView.as_view(), name='home'),
    
    path('accounts/', include('django.contrib.auth.urls')),  # Includes login, logout, etc.
    path('', LoginView.as_view(), name='login'),  # Custom login path
    
]