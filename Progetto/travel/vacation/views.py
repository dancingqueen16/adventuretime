from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from .models import Vacation, VacationList
from .forms import AddToListForm
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, FormView
from braces import views
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


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



class VacationDetailView(views.LoginRequiredMixin, DetailView, FormView):
    model = Vacation
    template_name = 'vacation/vacation.html'
    context_object_name = 'vacation'
    form_class = AddToListForm

    def get_success_url(self):
        return reverse_lazy('vacation:detailvacation', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context

    def get(self, request, *args, **kwargs):
        # Retrieve the vacation object
        self.object = self.get_object()
        # Create the form
        form = self.get_form()
        # Render the response
        context = self.get_context_data(object=self.object, form=form)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        # Retrieve the vacation object
        self.object = self.get_object()
        # Create the form with POST data
        form = self.get_form()
        if form.is_valid():
            status = form.cleaned_data['status']
            # Create or update the VacationList
            list, created = VacationList.objects.get_or_create(
                user=request.user,
                status=status
            )
            list.vacation.add(self.object)
            list.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        # Override form_valid to handle successful form submission
        return super().form_valid(form)

    def form_invalid(self, form):
        # Override form_invalid to handle form errors
        return self.render_to_response(self.get_context_data(form=form))


class ToDoVacationListView(views.LoginRequiredMixin, ListView):
    model = VacationList
    template_name = 'vacation/to_do_vacation_list.html'
    context_object_name = 'vacation_lists'

    def get_queryset(self):
        # Recupera tutte le liste di vacanze per l'utente con stato 'TODO'
        return VacationList.objects.filter(user=self.request.user, status='TODO')


class DoneVacationListView(views.LoginRequiredMixin, ListView):
    model = VacationList
    template_name = 'vacation/done_vacation_list.html'
    context_object_name = 'vacation_lists'

    def get_queryset(self):
        # Recupera tutte le liste di vacanze per l'utente con stato 'DONE'
        return VacationList.objects.filter(user=self.request.user, status='DONE')
