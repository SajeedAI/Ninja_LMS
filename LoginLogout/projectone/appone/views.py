from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.views.generic import ListView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required, user_passes_test

# Create Admin User View
class AdminUserCreateView(CreateView):
    model = User
    form_class = UserCreationForm
    template_name = 'admin_user_create.html'
    success_url = reverse_lazy('user_list')  # Redirect to user list after creation

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_staff = True  # Grants admin privileges
        user.is_superuser = True  # Grants full admin rights
        user.save()
        return super().form_valid(form)


# List Users View
class UserListView(ListView):
    model = User
    template_name = 'user_list.html'
    context_object_name = 'users'  # Context variable to pass users list to template

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import user_passes_test
from .models import Product

# def is_admin(user):
#     return user.is_staff
def is_admin(user):
    return user.is_superuser

# Create product view, only accessible by admin users
@user_passes_test(is_admin)
def create_product(request):
    if request.method == "POST":
        product_name = request.POST.get('product_name')
        
        if product_name:  # Ensure that product_name is provided
            # Create a new product
            Product.objects.create(product_name=product_name)
            return redirect('product_list')  # Redirect to the product list page after creation
        else:
            # Handle the case where product_name is missing
            return render(request, 'create_product.html', {'error': 'Product name is required'})
    
    return render(request, 'create_product.html')  # For GET request, show the form)

@user_passes_test(is_admin)
def edit_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if request.method == "POST":
        product.product_name = request.POST.get('product_name')
        product.save()
        return redirect('product_list')
    return render(request, 'edit_product.html', {'product': product})

@user_passes_test(is_admin)
def delete_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    product.delete()
    return redirect('product_list')


# Use the decorator to enforce login and check for admin
@user_passes_test(is_admin)
@login_required
def product_list(request):
    products = Product.objects.all()  # Fetch all products from the database
    return render(request, 'product_list.html', {'products': products})