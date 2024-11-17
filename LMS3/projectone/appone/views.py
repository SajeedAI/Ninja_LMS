from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Module, SubModule, UserAssignment
from django.contrib.auth.decorators import login_required
from .forms import ModuleForm, SubModuleForm, UserRegistrationForm

# MODULE CRUD
from django.contrib.auth.decorators import user_passes_test

@login_required(login_url='/accounts/login/')
# @user_passes_test(lambda u: u.has_perm('appone.can_view_module'))
# @user_passes_test(lambda u: u.is_superuser or u.is_authenticated)
# @user_passes_test(lambda u: u.is_superuser or u.is_staff)
# def module_list(request):
#     modules = Module.objects.all()
#     return render(request, 'appone/module_list.html', {'modules': modules})

def module_list(request):
    # Check if the user is a superuser or has some specific access
    if request.user.is_superuser:
        # Admins can see all modules
        modules = Module.objects.all()
    else:
        # Regular users can see modules based on their assignments or access
        # Assuming userassignment is a related field to track module access
        modules = Module.objects.filter(userassignment__user=request.user)

    return render(request, 'appone/module_list.html', {'modules': modules})

def module_create(request):
    if request.method == 'POST':
        form = ModuleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('module_list')
    else:
        form = ModuleForm()
    return render(request, 'appone/module_form.html', {'form': form})

def module_update(request, pk):
    module = get_object_or_404(Module, pk=pk)
    if request.method == 'POST':
        form = ModuleForm(request.POST, instance=module)
        if form.is_valid():
            form.save()
            return redirect('module_list')
    else:
        form = ModuleForm(instance=module)
    return render(request, 'appone/module_form.html', {'form': form})

def module_delete(request, pk):
    module = get_object_or_404(Module, pk=pk)
    if request.method == 'POST':
        module.delete()
        return redirect('module_list')
    return render(request, 'appone/module_confirm_delete.html', {'module': module})

# SUBMODULE CRUD
def submodule_list(request, module_id):
    # Retrieve the module based on the provided module_id
    module = get_object_or_404(Module, id=module_id)

    # Retrieve the submodules associated with the module
    submodules = SubModule.objects.filter(main_module=module)

    # Render the submodules in the template
    return render(request, 'appone/submodule_list.html', {'module': module, 'submodules': submodules})

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

    return render(request, 'appone/submodule_form.html', {'form': form, 'module': module})

def submodule_update(request, pk):
    submodule = get_object_or_404(SubModule, pk=pk)
    if request.method == 'POST':
        form = SubModuleForm(request.POST, instance=submodule)
        if form.is_valid():
            form.save()
            return redirect('submodule_list')
    else:
        form = SubModuleForm(instance=submodule)
    return render(request, 'appone/submodule_form.html', {'form': form})

# views.py
def submodule_create(request, module_id):
    module = get_object_or_404(Module, id=module_id)
    form = SubModuleForm(request.POST or None)
    if form.is_valid():
        submodule = form.save(commit=False)
        submodule.module = module
        submodule.save()
        return redirect('submodule_list', module_id=module.id)
    return render(request, 'appone/submodule_form.html', {'form': form, 'module': module})


# USER ASSIGNMENT CRUD
def user_assignments(request):
     # Fetch user assignments for the logged-in user
    assignments = UserAssignment.objects.filter(user=request.user)
    print(assignments)  # Debugging to check the assignments queryset
    
    # Fetch all modules
    modules = Module.objects.all()
    print(modules)  # Debugging to check the modules queryset
    
    # Render the template with both assignments and modules
    return render(request, 'appone/user_assignments.html', {
        'assignments': assignments,
        'modules': modules,
    })

# @login_required
# def user_assignment_list(request):
#     assignments = UserAssignment.objects.filter(user=request.user)
#     return render(request, 'appone/user_assignments.html', {'assignments': assignments})

@login_required
def user_assignment_list(request):
    # Fetch user assignments for the logged-in user
    assignments = UserAssignment.objects.all()
    print(f"Assignments: {assignments}")  # Debugging: Check if assignments are being fetched

    # Fetch all modules
    modules = Module.objects.all()
    print(f"Modules: {modules}")  # Debugging: Check if modules are being fetched

    # Render the template with both assignments and modules
    return render(request, 'appone/user_assignments.html', {
        'assignments': assignments,
        'modules': modules,
    })

from .forms import UserAssignmentForm  # Make sure this form exists
@login_required  # Ensure that only authenticated users can access this
def user_assignment_create(request):
    print("user_assignment_create")
    if request.method == 'POST':
        form = UserAssignmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_assignment_list')  # Redirect after successful save
    else:
        form = UserAssignmentForm()

    return render(request, 'appone/create.html', {'form': form})

@login_required
def user_assignment_delete(request, pk):
    assignment = get_object_or_404(UserAssignment, pk=pk, user=request.user)
    if request.method == 'POST':
        assignment.delete()
        return redirect('user_assignment_list')
    return render(request, 'appone/user_assignment_confirm_delete.html', {'assignment': assignment})

@login_required
def assign_module(request, module_id):
    module = get_object_or_404(Module, id=module_id)
    UserAssignment.objects.get_or_create(user=request.user, module=module)
    return redirect('user_assignments')

@login_required  # Ensure the user is logged in before they can see the assignments
def assignment_list(request):
    # Retrieve assignments for the logged-in user
    assignments = UserAssignment.objects.filter(user=request.user)

    # Render the assignments in the template
    return render(request, 'appone/user_assignments.html', {'assignments': assignments})

def submodule_delete(request, pk):
    submodule = get_object_or_404(SubModule, pk=pk)
    if request.method == 'POST':
        submodule.delete()
        return redirect('submodule_list', module_id=submodule.main_module.id)
    return render(request, 'appone/submodule_confirm_delete.html', {'submodule': submodule})

from django.contrib.auth.models import User
from django.contrib.auth import login
def register_user(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # Save the user object
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            # Assign selected modules to the user
            modules = form.cleaned_data['modules']
            for module in modules:
                UserAssignment.objects.create(user=user, module=module)

            # Log the user in
            login(request, user)

            # Redirect to a new page after successful registration, e.g., the module list
            return redirect('module_list')  # Change to appropriate redirect target
    else:
        form = UserRegistrationForm()

    # Render the registration form template
    return render(request, 'appone/register.html', {'form': form})

def home(request):
    return render(request, 'appone/base.html')
