from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy


# View per l'homepage
def home_page(request):
    templ = "homepage.html"
    ctx = {"title": "Lista di Vacanze"}
    return render(request, template_name=templ, context=ctx)


# View per la registrazione di un nuovo utente
class UserCreateView(CreateView):
    form_class = UserCreationForm
    template_name = "user_create.html"
    success_url = reverse_lazy("login")


# View per operazioni non autorizzate
def not_authorized_view(request):
    return render(request, 'not_authorized.html', {})
