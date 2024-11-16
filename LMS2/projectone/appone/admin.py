from django.contrib import admin
from .models import Module, UserAssignment

@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description')

@admin.register(UserAssignment)
class UserAssignmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'module')
