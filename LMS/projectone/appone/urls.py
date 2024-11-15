from django.urls import path
from .views import MainModuleListView, SubModuleListView, MainModuleCreateView, SubModuleCreateView, \
    MainModuleUpdateView, SubModuleUpdateView, MainModuleDeleteView, SubModuleDeleteView
from . import views
urlpatterns = [
     # modules
    path('', MainModuleListView.as_view(), name='main_module_list'),
    path('create/', MainModuleCreateView.as_view(), name='main_module_create'),
    path('<int:pk>/update/', MainModuleUpdateView.as_view(), name='main_module_update'),
    path('<int:pk>/delete/', MainModuleDeleteView.as_view(), name='main_module_delete'),
    # sub modules
    path('<int:main_module_id>/submodules/', views.SubModuleListView.as_view(), name='submodule_list'),
    path('<int:main_module_id>/submodule/create/', views.SubModuleCreateView.as_view(), name='sub_module_create'),
    path('<int:main_module_id>/submodule/<int:pk>/update/', views.SubModuleUpdateView.as_view(), name='sub_module_update'),

    path('submodule/<int:pk>/update/', SubModuleUpdateView.as_view(), name='sub_module_update'),
    path('submodule/<int:pk>/delete/', SubModuleDeleteView.as_view(), name='sub_module_delete'),
    path('submodules/', SubModuleListView.as_view(), name='submodule_list'),

]
