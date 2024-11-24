from django.contrib import admin
from .models import Question, Option

class OptionInline(admin.TabularInline):
    model = Option

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    inlines = [OptionInline]
