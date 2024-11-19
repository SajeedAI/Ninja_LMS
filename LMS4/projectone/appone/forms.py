from django import forms
from .models import Module, SubModule
from .models import UserAssignment
from django.contrib.auth.models import User

class ModuleForm(forms.ModelForm):
    class Meta:
        model = Module
        fields = ['title', 'description', 'image']
        exclude = ['date_created']  # Automatically excludes non-editable fields

class SubModuleForm(forms.ModelForm):
    class Meta:
        model = SubModule
        fields = ['title', 'description', 'main_module', 'session', 'topic', 'video_link']
        exclude = ['date_created']  # Automatically excludes non-editable fields

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
    role = forms.ChoiceField(choices=[('user', 'User'), ('staff', 'Staff'), ('superuser', 'Superuser')], required=True)
    modules = forms.ModelMultipleChoiceField(
        queryset=Module.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'role']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data
    
    def save(self, commit=True):
        user = super().save(commit=False)
        role = self.cleaned_data.get('role')

        # Set user role based on the selected role
        if role == 'staff':
            user.is_staff = True
        elif role == 'superuser':
            user.is_superuser = True

        user.set_password(self.cleaned_data["password"])

        if commit:
            user.save()

        # Handle module assignments
        modules = self.cleaned_data.get('modules')
        if modules:
            # Assign selected modules to the user (assuming you have a UserAssignment model)
            for module in modules:
                UserAssignment.objects.create(user=user, module=module)

        return user