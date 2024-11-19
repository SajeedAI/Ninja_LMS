from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Module, SubModule, UserAssignment
from django.contrib.auth.decorators import login_required
from .forms import ModuleForm, SubModuleForm, UserRegistrationForm
from django.contrib.auth.decorators import user_passes_test

# Module
# This method is used to fetch all the modules
# This method is used to fetch the User count
# This method is used to fetch the SubModule count
@login_required(login_url='/accounts/login/')
@user_passes_test(lambda user: user.is_superuser or user.is_staff)
def module_list(request):
    print("module_list: this method is used to fetch all the modules")

    # Get search query
    search_query = request.GET.get('search', '')

    # Get sort order: default is 'desc' (descending), 'asc' for ascending
    sort_order = request.GET.get('sort', 'desc')

    # Filter modules based on search query (title contains search term)
    if request.user.is_superuser:
        modules = Module.objects.all().filter(title__icontains=search_query)
    else:
        modules = Module.objects.filter(userassignment__user=request.user, title__icontains=search_query)

    # Sort the modules by date based on the sort order
    if sort_order == 'asc':
        modules = modules.order_by('date_created')
    else:
        modules = modules.order_by('-date_created')

    # Annotate with submodule count
    modules = modules.annotate(submodule_count=Count('submodules'))

    # Get total user count
    total_users = User.objects.count()

    return render(request, 'appone/module_list.html', {
        'modules': modules,
        'total_users': total_users,
        'search_query': search_query,
        'sort_order': sort_order,
    })

# Module
# This method is used to create the module
@user_passes_test(lambda user: user.is_superuser or user.is_staff)
@login_required
def module_create(request):
    print("module_create: this method is used to create the module")

    if request.method == 'POST':
        form = ModuleForm(request.POST, request.FILES)  # Include request.FILES
        if form.is_valid():
            form.save()
            return redirect('module_list')
    else:
        form = ModuleForm()
    return render(request, 'appone/module_form.html', {'form': form})

# Module
# This method is used to update the module
@user_passes_test(lambda user: user.is_superuser or user.is_staff)
@login_required
def module_update(request, pk):
    print("module_update: this method is used to update the module")

    module = get_object_or_404(Module, pk=pk)
    if request.method == 'POST':
        form = ModuleForm(request.POST, request.FILES, instance=module)  # Ensure request.FILES is passed here
        if form.is_valid():
            form.save()
            return redirect('module_list')
    else:
        form = ModuleForm(instance=module)
    return render(request, 'appone/module_form.html', {'form': form})

# Module
# This method is used to delete the module
@user_passes_test(lambda user: user.is_superuser or user.is_staff)
@login_required
def module_delete(request, pk):

    print("module_delete: this method is used to delete the module")

    module = get_object_or_404(Module, pk=pk)
    if request.method == 'POST':
        module.delete()
        return redirect('module_list')
    return render(request, 'appone/module_confirm_delete.html', {'module': module})

# submodule
# This method is used to fetch all the submodules from main module
@user_passes_test(lambda user: user.is_superuser or user.is_staff)
@login_required
def submodule_list(request, module_id):
    print("submodule_list: this method is used to fetch all the submodules from main module")

    # Retrieve the module based on the provided module_id
    module = get_object_or_404(Module, id=module_id)

    # Get the sorting option from the query string
    sort_option = request.GET.get('sort', 'date_desc')  # Default to sorting by newest

    # Retrieve the submodules associated with the module and apply sorting
    if sort_option == 'date_asc':
        submodules = SubModule.objects.filter(main_module=module).order_by('date_created')
    else:  # Default to 'date_desc'
        submodules = SubModule.objects.filter(main_module=module).order_by('-date_created')

    # Render the submodules in the template
    return render(request, 'appone/submodule_list.html', {'module': module, 'submodules': submodules})

# submodule
@user_passes_test(lambda user: user.is_superuser or user.is_staff)
@login_required
# @user_passes_test(lambda user: user.is_superuser)
def submodule_create(request, module_id):
    # Get the module object based on the module_id from the URL
    module = get_object_or_404(Module, id=module_id)

    # Handle the form submission
    if request.method == 'POST':
        form = SubModuleForm(request.POST)
        if form.is_valid():
            # Create the submodule instance but don't save it yet
            submodule = form.save(commit=False)
            # Associate the submodule with the module
            submodule.main_module = module
            submodule.save()
            # Redirect to the submodule list page for this module
            return redirect('submodule_list', module_id=module.id)
    else:
        form = SubModuleForm()

    return render(request, 'appone/submodule_create.html', {'form': form, 'module': module})

# submodule
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import user_passes_test
from .models import SubModule
from .forms import SubModuleForm

@user_passes_test(lambda user: user.is_superuser or user.is_staff)
@login_required
def submodule_update(request, pk):
    """
    This method is used to update a submodule.
    Only accessible by superusers.
    """
    print("submodule_update: this method is used to update a submodule")

    # Retrieve the SubModule object
    submodule = get_object_or_404(SubModule, pk=pk)

    if request.method == 'POST':
        # Process the form data
        form = SubModuleForm(request.POST, instance=submodule)
        if form.is_valid():
            form.save()
            # Redirect to the submodule list of the associated module
            return redirect('submodule_list', module_id=submodule.main_module.id)
    else:
        # Pre-fill the form with the current SubModule data
        form = SubModuleForm(instance=submodule)

    # Render the update form with context
    return render(request, 'appone/submodule_form.html', {
        'form': form,
        'module': submodule.main_module,  # Pass the associated module for URL context
    })

# submodule
@user_passes_test(lambda user: user.is_superuser or user.is_staff)
@login_required
def submodule_delete(request, pk):
    """
    This method is used to delete a submodule.
    Only accessible by superusers.
    """
    submodule = get_object_or_404(SubModule, pk=pk)
    module = submodule.main_module  # Retrieve the associated module

    if request.method == 'POST':
        submodule.delete()
        # Redirect to the submodule list for the associated module
        return redirect('submodule_list', module_id=module.id)

    # Render the confirmation page
    return render(request, 'appone/submodule_confirm_delete.html', {
        'submodule': submodule,
        'module': module,  # Pass the associated module to the template
    })

# user assignment
# This Method is used to add Module to Specific User Manually
from .forms import UserAssignmentForm  
@user_passes_test(lambda user: user.is_superuser or user.is_staff)
@login_required  
def user_assignment_set(request):

    print("user_assignment_set: this Method is used to add Module to Specific User Manually")
    
    if request.method == 'POST':
        form = UserAssignmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_assignment_list')  # Redirect after successful save
    else:
        form = UserAssignmentForm()

    return render(request, 'appone/user_assignment_set.html', {'form': form})

# This method user_assignment_list: this is for admin 
@user_passes_test(lambda user: user.is_superuser or user.is_staff)
@login_required
def user_assignment_list(request):
    print("user_assignment_list: this is for admin")
    
    # Fetch all user assignments
    assignments = UserAssignment.objects.all()
    modules = Module.objects.all()
    submodules = SubModule.objects.all()

    # Paginate assignments
    assignments_paginator = Paginator(assignments, 10)  # Show 10 assignments per page
    assignments_page_number = request.GET.get('assignments_page')
    assignments_page_obj = assignments_paginator.get_page(assignments_page_number)

    # Paginate modules
    modules_paginator = Paginator(modules, 10)  # Show 10 modules per page
    modules_page_number = request.GET.get('modules_page')
    modules_page_obj = modules_paginator.get_page(modules_page_number)

    # Paginate submodules
    submodules_paginator = Paginator(submodules, 10)  # Show 10 submodules per page
    submodules_page_number = request.GET.get('submodules_page')
    submodules_page_obj = submodules_paginator.get_page(submodules_page_number)

    # Render the template with paginated objects
    return render(request, 'appone/user_assignment_list.html', {
        'assignments': assignments_page_obj,
        'modules': modules_page_obj,
        'submodules': submodules_page_obj,
    })

@user_passes_test(lambda user: user.is_superuser or user.is_staff)
@login_required
def user_assignment_delete(request, pk):
    assignment = get_object_or_404(UserAssignment, pk=pk, user=request.user)
    if request.method == 'POST':
        assignment.delete()
        return redirect('user_assignment_list')
    return render(request, 'appone/user_assignment_confirm_delete.html', {'assignment': assignment})

# registartion
from django.db.models import Count
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Count
from .forms import UserRegistrationForm
from .models import UserAssignment, Module

@user_passes_test(lambda user: user.is_superuser or user.is_staff)
@login_required
def register_user(request):
    # Fetch module user counts for the template
    module_user_counts = UserAssignment.objects.values('module').annotate(user_count=Count('user')).order_by('-user_count')

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # Save the user object (without committing to the database yet)
            user = form.save(commit=False)
            
            # Set the password (hashed)
            user.set_password(form.cleaned_data['password'])

            # Assign the role based on the selected value from the form
            role = form.cleaned_data.get('role')
            if role == 'superuser' or role == 'staff':  # Ensure both superuser and staff have full access
                user.is_superuser = True
                user.is_staff = True  # Superusers and staff are both staff in terms of access
            else:
                user.is_superuser = False
                user.is_staff = False  # Regular users have no admin rights

            user.save()  # Commit the user object to the database

            # Assign selected modules to the user
            modules = form.cleaned_data['modules']
            for module in modules:
                UserAssignment.objects.create(user=user, module=module)

            # Add a success message
            messages.success(request, 'User registered successfully!')

            # Redirect to a dashboard or homepage after successful registration
            return redirect('register')  # Replace 'register' with the name of the view you want to redirect to
    else:
        form = UserRegistrationForm()

    # Fetch all modules to show in the template
    all_modules = Module.objects.all()

    # Render the registration form template along with the module user count and all modules
    return render(request, 'appone/register.html', {
        'form': form,
        'module_user_counts': module_user_counts,
        'all_modules': all_modules,
    })

from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count, Q
from django import forms
from django.core.paginator import Paginator

# Filter only superusers to access these views
@user_passes_test(lambda user: user.is_superuser or user.is_staff)
@login_required
def manage_users(request):
    # Search functionality
    query = request.GET.get('q')
    if query:
        users = User.objects.filter(
            Q(username__icontains=query) | Q(email__icontains=query)
        )
    else:
        users = User.objects.all()

    # Fetch registered users (non-superusers)
    registered_users = users.filter(is_superuser=False)

    # Pagination
    paginator = Paginator(registered_users, 10)  # Show 10 users per page
    page_number = request.GET.get('page')  # Get the current page number from the URL
    page_obj = paginator.get_page(page_number)  # Get the users for the current page

    return render(request, 'appone/manage_users.html', {'page_obj': page_obj})

# Form for editing user details
@user_passes_test(lambda user: user.is_superuser or user.is_staff)
@login_required
class EditUserForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput, required=False, help_text="Leave blank to keep the current password."
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        if self.cleaned_data['password']:
            user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
    
@user_passes_test(lambda user: user.is_superuser or user.is_staff)
@login_required
def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = EditUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('manage_users')  # Redirect to user management after successful edit
    else:
        form = EditUserForm(instance=user)

    return render(request, 'appone/edit_user.html', {'form': form, 'user': user})

@user_passes_test(lambda user: user.is_superuser or user.is_staff)
@login_required
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        user.delete()  # Hard delete
        return redirect('manage_users')  # Redirect to user management page
    return render(request, 'appone/confirm_delete.html', {'user': user})

@user_passes_test(lambda user: user.is_superuser or user.is_staff)
@login_required
def home(request):
    return render(request, 'appone/home.html')

