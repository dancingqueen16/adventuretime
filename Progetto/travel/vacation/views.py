from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from .models import Vacation
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from braces import views


# FBV
#def vacation_list(request):
#    templ = "vacation/vacationlist.html"
#    ctx = {"title": "Lista di Vacanze",
#           "vacationlist": Vacation.objects.all()}
#   return render(request, template_name=templ, context=ctx)


# CBV equivalente a sopra
class VacationListView(ListView):
    model = Vacation
    template_name = "vacation/vacationlist.html"


class CreateVacationView(CreateView):
    model = Vacation
    template_name = "vacation/create_vacation.html"
    fields = "__all__"
    success_url = reverse_lazy("vacation_list")


class DetailVacationView(DetailView):
    model = Vacation
    template_name = "vacation/vacation.html"


class UpdateVacationView(views.SuperuserRequiredMixin,UpdateView):
    model = Vacation
    template_name = "vacation/edit_vacation.html"
    fields = "__all__"

    def get_success_url(self):
        pk = self.get_context_data()["object"].pk
        return reverse("vacation:vacation", kwargs={'pk': pk})


class DeleteVacationView(views.SuperuserRequiredMixin,DeleteView):
    model = Vacation
    template_name = "vacation/delete_vacation.html"

    def get_success_url(self):
        return reverse("vacation:vacationlist")


