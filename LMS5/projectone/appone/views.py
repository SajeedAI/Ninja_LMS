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
class ModuleListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Module
    template_name = 'appone/module_list.html'
    context_object_name = 'modules'

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

    def test_func(self):
        """
        Ensures the user is either a superuser or staff member.
        """
        return self.request.user.is_superuser or self.request.user.is_staff
    
# Update View for Modules
class ModuleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Module
    form_class = ModuleForm
    template_name = 'appone/module_form.html'
    success_url = reverse_lazy('module_list')

# Delete View for Modules
class ModuleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Module
    template_name = 'appone/module_confirm_delete.html'
    success_url = reverse_lazy('module_list')

# submodule
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import SubModule
from .forms import SubModuleForm

class SubModuleCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = SubModule
    form_class = SubModuleForm
    template_name = 'appone/submodule_create.html'

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
class ModuleDetailView(DetailView):
    model = Module
    template_name = 'appone/module_detail.html'  # A template for displaying module details
    context_object_name = 'module'

    # Get the context data, adding the related submodules
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        module_id = self.kwargs['pk']
        # Add submodules related to this module to the context
        context['submodules'] = SubModule.objects.filter(main_module_id=module_id)
        return context

# ListView for SubModules
class SubmoduleListView(ListView):
    model = SubModule
    template_name = 'appone/submodule_list.html'
    context_object_name = 'submodules'

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

class SubModuleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = SubModule
    form_class = SubModuleForm
    template_name = 'appone/submodule_form.html'

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff

    def get_success_url(self):
        return reverse_lazy('submodule_list', kwargs={'module_id': self.object.main_module.id})

from django.views.generic.edit import DeleteView

class SubModuleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = SubModule
    template_name = 'appone/submodule_confirm_delete.html'

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff

    def get_success_url(self):
        return reverse_lazy('submodule_list', kwargs={'module_id': self.object.main_module.id})

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

from .models import UserAssignment
from .forms import UserAssignmentForm

class UserAssignmentSetView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = UserAssignment
    form_class = UserAssignmentForm
    template_name = 'appone/user_assignment_set.html'
    success_url = '/user-assignment/list/'  # Redirect after a successful operation

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

class ManageUsersView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = User
    template_name = 'appone/manage_users.html'
    paginate_by = 10

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return User.objects.filter(Q(username__icontains=query) | Q(email__icontains=query), is_superuser=False)
        return User.objects.filter(is_superuser=False)

from django.views.generic.edit import UpdateView
from .forms import EditUserForm

class EditUserView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = User
    form_class = EditUserForm
    template_name = 'appone/edit_user.html'

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff

    def get_success_url(self):
        return reverse_lazy('manage_users')


class DeleteUserView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = User
    template_name = 'appone/confirm_delete.html'

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff

    def get_success_url(self):
        return reverse_lazy('manage_users')

from django.views.generic.base import TemplateView

class HomeView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'appone/home.html'

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff

