from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django import forms
from users.models import CustomUser
from django.contrib.auth.forms import UserCreationForm

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        # Only allow users to fill in basic fields; do not include 'role'
        fields = ('username', 'email',)

    def save(self, commit=True):
        user = super().save(commit=False)
        # Force the role to 'guest' regardless of any input
        user.role = 'guest'
        if commit:
            user.save()
        return user
class AssignRoleForm(forms.Form):
    user = forms.ModelChoiceField(queryset=CustomUser.objects.all())
    role = forms.ChoiceField(choices=CustomUser.ROLE_CHOICES)   