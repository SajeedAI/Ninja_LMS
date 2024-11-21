# Create your views here.
from django.shortcuts import get_object_or_404
from .models import Module, SubModule, UserAssignment
from django.contrib.auth.decorators import login_required
from .forms import ModuleForm, SubModuleForm, UserRegistrationForm
from django.contrib.auth.decorators import user_passes_test
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, 
    CreateView, 
    UpdateView, 
    DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Module
from .forms import ModuleForm


# List View for Modules
# url: http://127.0.0.1:8000/modules/
# path: path('modules/', ModuleListView.as_view(), name='module_list'),
class ModuleListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Module
    template_name = 'appone/module_list.html'
    context_object_name = 'modules'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        print("ModuleListView: http://127.0.0.1:8000/modules/")

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff or self.request.user.is_authenticated

    def get_queryset(self):
        search_query = self.request.GET.get('search', '')
        sort_order = self.request.GET.get('sort', 'desc')
        queryset = Module.objects.filter(title__icontains=search_query)

        if not self.request.user.is_superuser:
            queryset = queryset.filter(userassignment__user=self.request.user)
        
        if sort_order == 'asc':
            queryset = queryset.order_by('date_created')
        else:
            queryset = queryset.order_by('-date_created')

        return queryset

    def get_context_data(self, **kwargs):
        from django.db.models import Count
        from django.contrib.auth.models import User

        context = super().get_context_data(**kwargs)
        context['total_users'] = User.objects.count()
        context['search_query'] = self.request.GET.get('search', '')
        context['sort_order'] = self.request.GET.get('sort', 'desc')
        return context

# url: http://127.0.0.1:8000/modules/create/
# path: path('modules/create/', ModuleCreateView.as_view(), name='module_create'),
# Create View for Modules
class ModuleCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """
    A class-based view that allows users to create new Module objects.
    It requires users to be logged in and pass a custom test (e.g., being superuser or staff).
    """
    model = Module
    form_class = ModuleForm
    template_name = 'appone/module_form.html'
    success_url = reverse_lazy('module_list')  # Redirect to the module list after success

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        print("ModuleCreateView: http://127.0.0.1:8000/modules/create/")

    def test_func(self):
        """
        Ensures the user is either a superuser or staff member.
        """
        return self.request.user.is_superuser or self.request.user.is_staff


# url: http://127.0.0.1:8000/modules/update/11/
# path: path('modules/update/<int:pk>/', ModuleUpdateView.as_view(), name='module_update'),
# Update View for Modules
class ModuleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Module
    form_class = ModuleForm
    template_name = 'appone/module_form.html'
    success_url = reverse_lazy('module_list')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        print("ModuleUpdateView: http://127.0.0.1:8000/modules/update/11/")

    def test_func(self):
        # Replace this with your logic to verify if the user has permission
        return self.request.user.is_superuser or self.request.user.is_staff

# url: http://127.0.0.1:8000/modules/delete/11/
# path: path('modules/delete/<int:pk>/', ModuleDeleteView.as_view(), name='module_delete'),
# Delete View for Modules
class ModuleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Module
    template_name = 'appone/module_confirm_delete.html'
    success_url = reverse_lazy('module_list')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        print("ModuleDeleteView: http://127.0.0.1:8000/modules/delete/11/")

    def test_func(self):
        # Replace this with your logic to verify if the user has permission
        return self.request.user.is_superuser or self.request.user.is_staff

# submodule
# url: http://127.0.0.1:8000/submodule/create/11/
# path: path('submodule/create/<int:module_id>/', SubModuleCreateView.as_view(), name='submodule_create'),
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import SubModule
from .forms import SubModuleForm

class SubModuleCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = SubModule
    form_class = SubModuleForm
    template_name = 'appone/submodule_create.html'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        print("SubModuleCreateView: http://127.0.0.1:8000/submodule/create/11/")


    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff

    def form_valid(self, form):
        # Retrieve the module object based on the 'module_id' passed in the URL
        module = get_object_or_404(Module, id=self.kwargs['module_id'])
        form.instance.main_module = module  # Assign the module to the new submodule
        return super().form_valid(form)

    def get_success_url(self):
        # Redirect to the list view after successful creation
        return reverse_lazy('submodule_list', kwargs={'module_id': self.kwargs['module_id']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Retrieve the module object to pass to the template
        module_id = self.kwargs['module_id']
        module = get_object_or_404(Module, id=module_id)
        context['module'] = module  # Pass the module to the template
        return context
    
from django.views.generic import DetailView, ListView
# DetailView for the Module
class ModuleDetailView(DetailView, LoginRequiredMixin, UserPassesTestMixin):
    model = Module
    template_name = 'appone/module_detail.html'  # A template for displaying module details
    context_object_name = 'module'

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff

    # Get the context data, adding the related submodules
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        module_id = self.kwargs['pk']
        # Add submodules related to this module to the context
        context['submodules'] = SubModule.objects.filter(main_module_id=module_id)
        return context

# ListView for SubModules
# url: http://127.0.0.1:8000/module/11/submodules/
# path: path('submodule/create/<int:module_id>/', SubModuleCreateView.as_view(), name='submodule_create'),
class SubmoduleListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = SubModule
    template_name = 'appone/submodule_list.html'
    context_object_name = 'submodules'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        print("SubmoduleListView: http://127.0.0.1:8000/module/11/submodules/")

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff or self.request.user.is_authenticated

    def get_queryset(self):
        module_id = self.kwargs['module_id']
        return SubModule.objects.filter(main_module_id=module_id)

    def get_context_data(self, **kwargs):
        # Get the context from the parent class
        context = super().get_context_data(**kwargs)
        
        # Get the module object based on the module_id
        module_id = self.kwargs['module_id']
        module = get_object_or_404(Module, id=module_id)
        
        # Pass the module to the template context
        context['module'] = module
        return context

    
from django.views.generic.edit import UpdateView

# url: http://127.0.0.1:8000/submodule/update/6/
# path: path('submodule/update/<int:pk>/', SubModuleUpdateView.as_view(), name='submodule_update'),
class SubModuleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = SubModule
    form_class = SubModuleForm
    template_name = 'appone/submodule_form.html'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        print("SubModuleUpdateView: http://127.0.0.1:8000/submodule/update/6/")

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff

    def get_success_url(self):
        if self.object.main_module:
            return reverse_lazy('submodule_list', kwargs={'module_id': self.object.main_module.id})
        else:
            raise ValueError("Main module is not set for this submodule.")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module'] = self.object.main_module
        return context

from django.views.generic.edit import DeleteView

# url: http://127.0.0.1:8000/submodule/delete/6/
# path: path('submodule/delete/<int:pk>/', SubModuleDeleteView.as_view(), name='submodule_delete'),
class SubModuleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = SubModule
    template_name = 'appone/submodule_confirm_delete.html'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        print("SubModuleDeleteView: http://127.0.0.1:8000/submodule/delete/6/")

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff

    def get_success_url(self):
        if self.object.main_module and self.object.main_module.id:
            return reverse_lazy('submodule_list', kwargs={'module_id': self.object.main_module.id})
        else:
            raise ValueError("SubModule's main_module is not set or does not have an ID.")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module'] = self.object.main_module  # Pass the related module for the template
        return context

# url: http://127.0.0.1:8000/user-assignment/list/
# path: path('user-assignment/list/', UserAssignmentListView.as_view(), name='user_assignment_list'),
from django.views.generic.list import ListView
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView
from .models import UserAssignment, Module, SubModule

class UserAssignmentListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = UserAssignment
    template_name = 'appone/user_assignment_list.html'
    context_object_name = 'assignments' 
    paginate_by = 5  # Paginate 10 items per page for UserAssignments

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        print("UserAssignmentListView: http://127.0.0.1:8000/user-assignment/list/")

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Pagination for UserAssignments (Already handled by paginate_by)
        assignments_page = self.request.GET.get('assignments_page', 1)
        assignments_paginator = Paginator(UserAssignment.objects.all(), self.paginate_by)
        assignments = assignments_paginator.get_page(assignments_page)
        context['assignments'] = assignments

        # Pagination for Modules
        modules_page = self.request.GET.get('modules_page', 1)
        modules_paginator = Paginator(Module.objects.all(), self.paginate_by)
        modules = modules_paginator.get_page(modules_page)
        context['modules'] = modules

        # Pagination for SubModules
        submodules_page = self.request.GET.get('submodules_page', 1)
        submodules_paginator = Paginator(SubModule.objects.all(), self.paginate_by)
        submodules = submodules_paginator.get_page(submodules_page)
        context['submodules'] = submodules

        return context

# url: http://127.0.0.1:8000/user-assignment/set/
# path : path('user-assignment/set/', UserAssignmentSetView.as_view(), name='user_assignment_set'),
from .models import UserAssignment
from .forms import UserAssignmentForm

class UserAssignmentSetView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = UserAssignment
    form_class = UserAssignmentForm
    template_name = 'appone/user_assignment_set.html'
    success_url = '/user-assignment/list/'  # Redirect after a successful operation

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        print("UserAssignmentSetView: http://127.0.0.1:8000/user-assignment/set/")

    # Only superusers or staff can access this view
    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff
    
class UserAssignmentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = UserAssignment
    template_name = 'appone/user_assignment_confirm_delete.html'

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff

    def get_success_url(self):
        return reverse_lazy('user_assignment_list')

from django.views.generic.edit import FormView
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Count

class RegisterUserView(LoginRequiredMixin, UserPassesTestMixin, FormView):
    template_name = 'appone/register.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('register')

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])

        role = form.cleaned_data.get('role')
        user.is_superuser = user.is_staff = role in ['superuser', 'staff']
        user.save()

        modules = form.cleaned_data['modules']
        for module in modules:
            UserAssignment.objects.create(user=user, module=module)

        messages.success(self.request, 'User registered successfully!')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_user_counts'] = UserAssignment.objects.values('module').annotate(user_count=Count('user')).order_by('-user_count')
        context['all_modules'] = Module.objects.all()
        return context
    
from django.db.models import Q

# url: http://127.0.0.1:8000/manage_users/
# path: path('manage_users/', ManageUsersView.as_view(), name='manage_users'),
class ManageUsersView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = User
    template_name = 'appone/manage_users.html'
    paginate_by = 10

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        print("ManageUsersView: http://127.0.0.1:8000/manage_users/")

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return User.objects.filter(Q(username__icontains=query) | Q(email__icontains=query), is_superuser=False)
        return User.objects.filter(is_superuser=False)

# url: http://127.0.0.1:8000/manage_users/edit/2/
# path: path('manage_users/edit/<int:pk>/', EditUserView.as_view(), name='edit_user'),
from django.views.generic.edit import UpdateView
from .forms import EditUserForm

class EditUserView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = User
    form_class = EditUserForm
    template_name = 'appone/edit_user.html'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        print("EditUserView: http://127.0.0.1:8000/manage_users/edit/2/")

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff

    def get_success_url(self):
        return reverse_lazy('manage_users')

# url: http://127.0.0.1:8000/manage_users/delete/2/
# path: path('manage_users/delete/<int:pk>/', DeleteUserView.as_view(), name='delete_user'),
class DeleteUserView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = User
    template_name = 'appone/confirm_delete.html'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        print("DeleteUserView: http://127.0.0.1:8000/manage_users/delete/2/")

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff

    def get_success_url(self):
        return reverse_lazy('manage_users')

from django.views.generic.base import TemplateView

# url: http://127.0.0.1:8000/home/
# path: path('home/', HomeView.as_view(), name='home'),
class HomeView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'appone/home.html'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        print("HomeView: http://127.0.0.1:8000/home/")

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff or self.request.user.is_authenticated


