from django.contrib import admin
from .models import Module, SubModule, UserAssignment

@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')

@admin.register(SubModule)
class SubModuleAdmin(admin.ModelAdmin):
    list_display = ('title', 'main_module', 'topic', 'video_link')

@admin.register(UserAssignment)
class UserAssignmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'module')
