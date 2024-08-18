from django.http import HttpResponse
from django.shortcuts import render
from .models import Vacation


def vacation_list(request):
    templ = "vacation/vacationlist.html"
    ctx = {"title": "Lista di Vacanze",
           "vacationlist": Vacation.objects.all()}
    return render(request, template_name=templ, context=ctx)
