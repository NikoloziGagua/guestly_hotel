from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django import forms
from users.models import CustomUser
from django.contrib.auth.forms import UserCreationForm

#


class CustomUserCreationForm(UserCreationForm):
    role = forms.ChoiceField(
        choices=CustomUser.ROLE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'role', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = self.cleaned_data['role']  
        if commit:
            user.save()
        return user
class CustomUserRegisterForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes to all fields
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control form-control-lg'})
            field.widget.attrs['placeholder'] = field.label
            
    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'guest'  # Force role to be guest
        if commit:
            user.save()
        return user
class AssignRoleForm(forms.Form):
    user = forms.ModelChoiceField(queryset=CustomUser.objects.all())
    role = forms.ChoiceField(choices=CustomUser.ROLE_CHOICES)   

class CustomUserChangeForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'role')  

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user 