from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import render
from .models import MainModule, SubModule
from django.shortcuts import get_object_or_404

# List Views
# url: http://127.0.0.1:8000/appone/
# path: path('', MainModuleListView.as_view(), name='main_module_list'),
# Title, Description, Actions
class MainModuleListView(ListView):
    model = MainModule
    template_name = 'appone/main_module_list.html'
    context_object_name = 'main_modules'  #  {% for module in main_modules %}

    def __init__(self, *args, **kwargs):
        print("MainModuleListView: ListView")  
        super().__init__(*args, **kwargs)

# Create Views
# url: http://127.0.0.1:8000/appone/create/
# path('create/', MainModuleCreateView.as_view(), name='main_module_create'),
# Title, Description
class MainModuleCreateView(CreateView):
    model = MainModule
    template_name = 'appone/main_module_form.html'
    fields = ['title', 'description']
    success_url = reverse_lazy('main_module_list')

    def __init__(self, *args, **kwargs):
        print("MainModuleCreateView: CreateView")  
        super().__init__(*args, **kwargs)

# url: http://127.0.0.1:8000/appone/1/submodules/
# path: path('<int:main_module_id>/submodules/', views.SubModuleListView.as_view(), name='submodule_list'),
# Title, Topic, VideoLink, Actions
class SubModuleListView(ListView):
    model = SubModule
    template_name = 'appone/sub_module_list.html'
    context_object_name = 'submodules'
   
    def get_queryset(self):
        print("SubModuleListView get_queryset")
        main_module = get_object_or_404(MainModule, pk=self.kwargs['main_module_id'])
        return SubModule.objects.filter(main_module=main_module)

    def get_context_data(self, **kwargs):
        print("SubModuleListView: get_context_data")
        context = super().get_context_data(**kwargs)
        main_module = get_object_or_404(MainModule, pk=self.kwargs['main_module_id'])
        context['main_module'] = main_module  #  {% for module in main_modules %}
        return context

# http://127.0.0.1:8000/appone/1/submodule/create/
# path('<int:main_module_id>/submodule/create/', views.SubModuleCreateView.as_view(), name='sub_module_create'),
# Title, Topic, VideoLink, MainModule(drop down)
class SubModuleCreateView(CreateView):
    model = SubModule
    template_name = 'appone/sub_module_form.html'
    fields = ['title', 'topic', 'video_link', 'main_module']

    def get_context_data(self, **kwargs):
        print("SubModuleCreateView: get_context_data")
        context = super().get_context_data(**kwargs)
        main_module_id = self.kwargs['main_module_id']
        context['main_module'] = get_object_or_404(MainModule, id=main_module_id)
        return context

    # After submodule created, redirect to 
    # url: http://127.0.0.1:8000/appone/1/submodules/
    def get_success_url(self):
        print("SubModuleCreateView: get_success_url")
        main_module_id = self.kwargs['main_module_id']
        return reverse_lazy('submodule_list', kwargs={'main_module_id': main_module_id})
    
# url: http://127.0.0.1:8000/appone/1/submodule/4/update/
# path: path('submodule/<int:pk>/update/', SubModuleUpdateView.as_view(), name='sub_module_update'),
class SubModuleUpdateView(UpdateView):
    model = SubModule
    template_name = 'appone/sub_module_form.html'
    fields = ['title', 'topic', 'video_link', 'main_module']  # Include 'main_module'
    
    def get_context_data(self, **kwargs):
        print("SubModuleUpdateView: get_context_data")
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update Sub Module'  # Set custom title for the update page
        context['main_module'] = self.object.main_module  # Pass the main_module to the context
        return context
    
     # Dynamically set success_url based on the main_module_id
    def get_success_url(self):
        print("SubModuleUpdateView: get_success_url")
        main_module_id = self.object.main_module.id  # Get the main_module id of the updated submodule
        return reverse_lazy('submodule_list', kwargs={'main_module_id': main_module_id})

# path('submodule/<int:pk>/delete/', SubModuleDeleteView.as_view(), name='sub_module_delete'),
# path('submodules/', SubModuleListView.as_view(), name='submodule_list'),
class SubModuleDeleteView(DeleteView):
    model = SubModule
    template_name = 'appone/sub_module_confirm_delete.html'

    def __init__(self, *args, **kwargs):
        print("SubModuleDeleteView: get_success_url")
        super().__init__(*args, **kwargs)

    def get_success_url(self):
    
        return reverse_lazy('submodule_list', kwargs={'main_module_id': self.object.main_module.id})

# Update Views
# url: http://127.0.0.1:8000/appone/3/update/
# path: path('<int:pk>/update/', MainModuleUpdateView.as_view(), name='main_module_update'),
class MainModuleUpdateView(UpdateView):
    model = MainModule
    template_name = 'appone/main_module_form.html'
    fields = ['title', 'description']
    success_url = reverse_lazy('main_module_list')

    def __init__(self, *args, **kwargs):
        print("MainModuleUpdateView: UpdateView")
        super().__init__(*args, **kwargs)

# Delete Views
class MainModuleDeleteView(DeleteView):
    model = MainModule
    template_name = 'appone/main_module_confirm_delete.html'
    success_url = reverse_lazy('main_module_list')  # Redirect after deletion

    def __init__(self, *args, **kwargs):
        print("MainModuleDeleteView: DeleteView")
        super().__init__(*args, **kwargs)