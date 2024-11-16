from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from .forms import ModuleForm, UserAssignmentForm, UserRegistrationForm
from .models import Module, UserAssignment

# http://127.0.0.1:8000/modules/register/
# path('register/', views.register_user, name='register'),
def register_user(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            # Assign selected modules to the user
            modules = form.cleaned_data['modules']
            for module in modules:
                UserAssignment.objects.create(user=user, module=module)

            login(request, user)  # Log the user in
            return redirect('register')  # Redirect to the module list page
    else:
        form = UserRegistrationForm()

    # Fetch all users and pass them to the template
    users = User.objects.all()

    return render(request, 'register.html', {'form': form, 'users': users})

def home(request):
    return render(request, 'base.html')

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Module, UserAssignment
from .forms import ModuleForm, UserAssignmentForm

# List all modules
# http://127.0.0.1:8000/modules/modules/
# id, title (edit, delete)
# def module_list(request):
#     print("module_list: id, title (edit, delete)")
#     modules = Module.objects.all()
#     return render(request, 'module_list.html', {'modules': modules})

from django.contrib.auth.decorators import user_passes_test
@user_passes_test(lambda u: u.is_superuser)
def module_list(request):
    print("module_list: id, title (edit, delete)")
    modules = Module.objects.all()
    return render(request, 'module_list.html', {'modules': modules})

# Detail view of a single module
# http://127.0.0.1:8000/modules/modules/add/
# path('user_assignments/', views.user_assignment_list, name='user_assignment_list'),
# id, user, title (edit)
def module_detail(request, pk):
    print("module_detail: reverse")
    module = get_object_or_404(Module, pk=pk)
    return render(request, 'module_detail.html', {'module': module})

# http://127.0.0.1:8000/modules/modules/add/
# path('user_assignments/add/', views.user_assignment_add, name='user_assignment_add'),
# title, description
# Add a new module
def module_add(request):
    print("module_add: title, description")
    if request.method == 'POST':
        form = ModuleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('module_list')
    else:
        form = ModuleForm()
    return render(request, 'module_form.html', {'form': form})

# Edit a module
# http://127.0.0.1:8000/modules/modules/4/edit/
# path('modules/<int:pk>/edit/', views.module_edit, name='module_edit'),
def module_edit(request, pk):
    print("module_edit: title, description")
    module = get_object_or_404(Module, pk=pk)
    if request.method == 'POST':
        form = ModuleForm(request.POST, instance=module)
        if form.is_valid():
            form.save()
            return redirect('module_list')
    else:
        form = ModuleForm(instance=module)
    return render(request, 'module_form.html', {'form': form})

# Delete a module
# http://127.0.0.1:8000/modules/modules/4/delete/
# path('modules/<int:pk>/delete/', views.module_delete, name='module_delete'),
def module_delete(request, pk):
    module = get_object_or_404(Module, pk=pk)
    if request.method == 'POST':
        module.delete()
        return redirect('module_list')
    return render(request, 'module_confirm_delete.html', {'module': module})

# List all user assignments
# http://127.0.0.1:8000/modules/user_assignments/
# path('user_assignments/', views.user_assignment_list, name='user_assignment_list'),
# id, username, title (edit, delete)
# def user_assignment_list(request):
#     print("user_assignment_list: id, username, title (edit, delete)")
#     user_assignments = UserAssignment.objects.all()
#     return render(request, 'user_assignment_list.html', {'user_assignments': user_assignments})

def user_assignment_list(request):
    # Print debugging info (optional)
    print("user_assignment_list: id, username, title (edit, delete)")

    # Check if the user is an admin
    if request.user.is_staff:
        # Admins see all assignments
        user_assignments = UserAssignment.objects.all()
    else:
        # Regular users see only their own assignments
        user_assignments = UserAssignment.objects.filter(user=request.user)

    # Render the template with the filtered assignments
    return render(request, 'user_assignment_list.html', {'user_assignments': user_assignments})

# Assign a module to a user
# http://127.0.0.1:8000/modules/user_assignments/add/

def user_assignment_add(request):
    print("user_assignment_add: User(dropdown), Module(Dropdown)")
    if request.method == 'POST':
        form = UserAssignmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_assignment_list')
    else:
        form = UserAssignmentForm()
    return render(request, 'user_assignment_form.html', {'form': form})

# Delete a user assignment
# http://127.0.0.1:8000/modules/user_assignments/2/delete/
# path('user_assignment/delete/<int:pk>/', views.user_assignment_delete, name='user_assignment_delete'),
def user_assignment_delete(request, pk):
    print("user_assignment_delete: delete id")
    user_assignment = get_object_or_404(UserAssignment, pk=pk)
    if request.method == 'POST':
        user_assignment.delete()
        return redirect('user_assignment_list')
    return render(request, 'user_assignment_confirm_delete.html', {'user_assignment': user_assignment})

# http://127.0.0.1:8000/modules/user_assignment/edit/1/
def user_assignment_edit(request, pk):
    print("user_assignment_edit: UserName, ModuleName")
    assignment = get_object_or_404(UserAssignment, pk=pk)
    
    if request.method == 'POST':
        form = UserAssignmentForm(request.POST, instance=assignment)
        if form.is_valid():
            form.save()
            return redirect('user_assignment_list')  # Redirect to the assignment list page
    else:
        form = UserAssignmentForm(instance=assignment)
    
    return render(request, 'user_assignment_edit.html', {'form': form})