from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy

from .models import Vacation
from django.views.generic import ListView, CreateView


# FBV
def vacation_list(request):
    templ = "vacation/vacationlist.html"
    ctx = {"title": "Lista di Vacanze",
           "vacationlist": Vacation.objects.all()}
    return render(request, template_name=templ, context=ctx)


# CBV equivalente a sopra
class VacationListView(ListView):
    model = Vacation
    template_name = "vacation/vacationlist.html"


class CreateVacationView(CreateView):
    model = Vacation
    template_name = "vacation/vacationcreate.html"
    fields = "__all__"
    success_url = reverse_lazy("vacation_list")