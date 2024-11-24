from django.contrib import admin
from .models import Week, Question, Option, UserResponse

class OptionInline(admin.TabularInline):
    model = Option
    extra = 4  # Default number of empty option fields

class QuestionAdmin(admin.ModelAdmin):
    inlines = [OptionInline]
    list_display = ['text', 'week']
    search_fields = ['text']
    list_filter = ['week']

class UserResponseAdmin(admin.ModelAdmin):
    list_display = ['question', 'selected_option', 'is_correct']
    list_filter = ['is_correct', 'question__week']
    search_fields = ['question__text', 'selected_option']

admin.site.register(Week)
admin.site.register(Question, QuestionAdmin)
admin.site.register(UserResponse, UserResponseAdmin)
