from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from .models import Vacation, List
from .forms import AddToListForm
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, FormView
from braces import views
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages


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


class CreateVacationView(views.SuperuserRequiredMixin,CreateView):
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


@login_required
def my_profile(request):
    user = get_object_or_404(User, pk=request.user.pk)
    return render(request,"vacation/myprofile.html")


class VacationDetailView(FormView, DetailView):
    model = Vacation
    template_name = 'vacation/vacation.html'
    form_class = AddToListForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        vacation = self.get_object()
        list = form.get_or_create_list()
        if list.vacations.filter(pk=vacation.pk).exists():
            messages.warning(self.request, f'La vacanza "{vacation.title}" è già nella playlist "{list.name}".')
        else:
            list.vacations.add(vacation)
            messages.success(self.request,
                             f'La vacanza "{vacation.title}" è stata aggiunta alla playlist "{list.name}".')
        return redirect('vacation:detailvacation', pk=vacation.pk)

    def form_invalid(self, form):
        messages.error(self.request, 'C\'è stato un problema con il tuo invio. Per favore, riprova.')
        return self.render_to_response(self.get_context_data(form=form))


class DoneVacations(views.LoginRequiredMixin, ListView):
    model = List
    template_name = "vacation/donevacations.html"
    context_object_name = "List"

    def get_queryset(self):
        return List.objects.filter(user=self.request.user).filter(name='Fatte')


class ToDoVacations(views.LoginRequiredMixin, ListView):
    model = List
    template_name = "vacation/donevacations.html"
    context_object_name = "List"

    def get_queryset(self):
        return List.objects.filter(user=self.request.user).filter(name='Da Fare')


class LikedVacations(views.LoginRequiredMixin, ListView):
    model = Vacation
    template_name = "vacation/likedvacations.html"
    context_object_name = "Liked"

    def get_queryset(self):
        return Vacation.objects.filter(likes=self.request.user)


@login_required
def like_vacation(request, pk):
    # Recupera l'oggetto Scheda
    vacation = get_object_or_404(Vacation, pk=pk)
    # Controlla se l'utente ha già messo un like a questo post
    if request.user in vacation.likes.all():
        vacation.likes.remove(request.user)
    else:
        vacation.likes.add(request.user)
    return redirect(reverse("vacation:detailvacation", kwargs={"pk": pk}))
