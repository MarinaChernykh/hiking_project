from django import forms
from django.contrib.auth.forms import (
    UserCreationForm, AuthenticationForm, UsernameField)
from django.contrib.auth import get_user_model


User = get_user_model()


class CreationForm(UserCreationForm):
    """Customized new user creation form."""
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email')


class CustomAuthenticationForm(AuthenticationForm):
    username = UsernameField(
        label='Имя пользователя или email',
        widget=forms.TextInput(attrs={'autofocus': True})
    )
