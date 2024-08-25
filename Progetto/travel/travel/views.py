from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy


def home_page(request):
    templ = "homepage.html"
    ctx = {"title": "Lista di Vacanze"}
    return render(request, template_name=templ, context=ctx)


def logging_out(request):
    templ = "logging_out.html"
    ctx = {"title": "Logout"}
    return render(request, template_name=templ, context=ctx)


class UserCreateView(CreateView):
    form_class = UserCreationForm
    template_name = "user_create.html"
    success_url = reverse_lazy("login")


def not_authorized_view(request):
    return render(request, 'not_authorized.html', {})