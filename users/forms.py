from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django import forms
from users.models import CustomUser
from django.contrib.auth.forms import UserCreationForm

class CustomUserCreationForm(UserCreationForm):
    """
    Extended user creation form that includes role selection.
    Used by staff members to create new users with specific roles.
    """
    role = forms.ChoiceField(
        choices=CustomUser.ROLE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
    )

    class Meta:
        model = CustomUser
        # Define all required fields for user creation by staff
        fields = ['username', 'email', 'first_name', 'last_name', 'role', 'password1', 'password2']

    def save(self, commit=True):
        """
        Override save method to handle custom role assignment
        Args:
            commit (bool): Whether to save to database immediately
        Returns:
            CustomUser: The created user instance
        """
        user = super().save(commit=False)
        user.role = self.cleaned_data['role']  
        if commit:
            user.save()
        return user

class CustomUserRegisterForm(UserCreationForm):
    """
    Public registration form for new guests.
    Automatically assigns 'guest' role and applies Bootstrap styling.
    """
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
        
    def __init__(self, *args, **kwargs):
        """
        Initialize form with Bootstrap styling for all fields
        """
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes to all fields
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control form-control-lg'})
            field.widget.attrs['placeholder'] = field.label
            
    def save(self, commit=True):
        """
        Override save method to automatically set role as 'guest'
        Args:
            commit (bool): Whether to save to database immediately
        Returns:
            CustomUser: The created user instance with guest role
        """
        user = super().save(commit=False)
        user.role = 'guest'  # Force role to be guest
        if commit:
            user.save()
        return user

class AssignRoleForm(forms.Form):
    """
    Form for staff members to change user roles
    Provides dropdowns for selecting user and their new role
    """
    user = forms.ModelChoiceField(queryset=CustomUser.objects.all())  # Dropdown to select user
    role = forms.ChoiceField(choices=CustomUser.ROLE_CHOICES)         # Dropdown to select new role

class CustomUserChangeForm(forms.ModelForm):
    """
    Form for updating existing user information
    Allows modification of basic user details and role
    """
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'role')  # Fields that can be modified

    def save(self, commit=True):
        """
        Save the updated user information
        Args:
            commit (bool): Whether to save to database immediately
        Returns:
            CustomUser: The updated user instance
        """
        user = super().save(commit=False)
        if commit:
            user.save()
        return user