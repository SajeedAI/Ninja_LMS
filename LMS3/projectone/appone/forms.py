from django import forms
from .models import Module, SubModule
from .models import UserAssignment
from django.contrib.auth.models import User

class ModuleForm(forms.ModelForm):
    class Meta:
        model = Module
        fields = ['title', 'description']

class SubModuleForm(forms.ModelForm):
    class Meta:
        model = SubModule
        fields = ['title', 'description', 'main_module', 'topic', 'video_link']
       
class UserAssignmentForm(forms.ModelForm):
    class Meta:
        model = UserAssignment
        fields = ['user', 'module']
        widgets = {
            'user': forms.Select(attrs={'class': 'form-control'}),
            'module': forms.Select(attrs={'class': 'form-control'}),
        }

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    modules = forms.ModelMultipleChoiceField(
        queryset=Module.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data
    
