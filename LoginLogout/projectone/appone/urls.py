from django.urls import path
from .views import UserListView, AdminUserCreateView, create_product, edit_product, delete_product, product_list

urlpatterns = [
    path('users/', UserListView.as_view(), name='user_list'),  # List of all users
    path('create_admin/', AdminUserCreateView.as_view(), name='create_admin'),  # Create new admin user
    path('create/', create_product, name='create_product'),
    path('edit/<int:product_id>/', edit_product, name='edit_product'),
    path('delete/<int:product_id>/', delete_product, name='delete_product'),
    path('product_list/', product_list, name='product_list'),  # Product list URL
]

