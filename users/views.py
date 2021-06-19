from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from .forms import CreationForm

class sign_up(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy("login")
    template_name = "signUp.html"
