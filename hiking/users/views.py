from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy

from .forms import CreationForm, CustomAuthenticationForm


class SignUp(CreateView):
    """New user creation view."""
    form_class = CreationForm
    success_url = reverse_lazy('trails:index')
    template_name = 'users/signup.html'


class CustomLoginView(LoginView):
    authentication_form = CustomAuthenticationForm
