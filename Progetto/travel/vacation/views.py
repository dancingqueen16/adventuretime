from collections import Counter

from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from .models import Vacation, List
from .forms import AddToListForm, VacationSearchForm
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, FormView
from braces import views
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages


class VacationListView(ListView):
    model = Vacation
    template_name = "vacation/vacationlist.html"


class CreateVacationView(views.SuperuserRequiredMixin, CreateView):
    model = Vacation
    template_name = "vacation/create_vacation.html"
    fields = '__all__'
    success_url = reverse_lazy("vacation:vacationlist")

    def handle_no_permission(self, request):
        return redirect('not_authorized')


class DetailVacationView(DetailView):
    model = Vacation
    template_name = "vacation/vacation.html"


class UpdateVacationView(views.SuperuserRequiredMixin,UpdateView):
    model = Vacation
    template_name = "vacation/edit_vacation.html"
    fields = "__all__"

    def handle_no_permission(self, request):
        return redirect('not_authorized')

    def get_success_url(self):
        pk = self.get_context_data()["object"].pk
        return reverse("vacation:vacation", kwargs={'pk': pk})


class DeleteVacationView(views.SuperuserRequiredMixin,DeleteView):
    model = Vacation
    template_name = "vacation/delete_vacation.html"

    def handle_no_permission(self, request):
        return redirect('not_authorized')

    def get_success_url(self):
        return reverse("vacation:vacationlist")


@login_required(login_url=reverse_lazy('not_authorized'))
def my_profile(request):
    user = get_object_or_404(User, pk=request.user.pk)

    # Ottieni le raccomandazioni delle vacanze per l'utente
    recommended_vacations = recommend_vacations(user)

    # Passa sia i dati del profilo che le vacanze raccomandate al template
    return render(request, 'vacation/myprofile.html', {
        'user': user,
        'vacations': recommended_vacations
    })


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
        selected_list = form.get_or_create_list()

        # Riferimenti ai nomi delle liste
        fatti_list_name = 'Fatte'
        da_fare_list_name = 'Da Fare'

        # Ottenere le altre liste dell'utente
        fatti_list = List.objects.filter(user=self.request.user, name=fatti_list_name).first()
        da_fare_list = List.objects.filter(user=self.request.user, name=da_fare_list_name).first()

        # Controlla se la vacanza è nella lista opposta
        if selected_list.name == fatti_list_name:
            # Se si aggiunge a "Fatte" e la vacanza è in "Da Fare", rimuoverla da "Da Fare"
            if da_fare_list and da_fare_list.vacations.filter(pk=vacation.pk).exists():
                da_fare_list.vacations.remove(vacation)
                messages.info(self.request,
                              f'La vacanza "{vacation.title}" è stata rimossa dalla lista "{da_fare_list_name}".')

        elif selected_list.name == da_fare_list_name:
            # Se si aggiunge a "Da Fare" e la vacanza è in "Fatte", non permettere l'aggiunta
            if fatti_list and fatti_list.vacations.filter(pk=vacation.pk).exists():
                messages.warning(self.request,
                                 f'La vacanza "{vacation.title}" è già nella lista "{fatti_list_name}" e non può essere aggiunta a "{da_fare_list_name}".')
                return redirect('vacation:detailvacation', pk=vacation.pk)

        # Aggiungi la vacanza alla lista selezionata, se non è già presente
        if selected_list.vacations.filter(pk=vacation.pk).exists():
            messages.warning(self.request, f'La vacanza "{vacation.title}" è già nella lista "{selected_list.name}".')
        else:
            selected_list.vacations.add(vacation)
            messages.success(self.request,
                             f'La vacanza "{vacation.title}" è stata aggiunta alla lista "{selected_list.name}".')

        return redirect('vacation:detailvacation', pk=vacation.pk)

    def form_invalid(self, form):
        messages.error(self.request, 'C\'è stato un problema con il tuo invio. Per favore, riprova.')
        return self.render_to_response(self.get_context_data(form=form))


class DoneVacations(views.LoginRequiredMixin, ListView):
    model = List
    template_name = "vacation/donevacations.html"
    context_object_name = "List"

    def handle_no_permission(self, request):
        return redirect('not_authorized')

    def get_queryset(self):
        return List.objects.filter(user=self.request.user).filter(name='Fatte')


class ToDoVacations(views.LoginRequiredMixin, ListView):
    model = List
    template_name = "vacation/todovacations.html"
    context_object_name = "List"

    def handle_no_permission(self, request):
        return redirect('not_authorized')

    def get_queryset(self):
        return List.objects.filter(user=self.request.user).filter(name='Da Fare')


class LikedVacations(views.LoginRequiredMixin, ListView):
    model = Vacation
    template_name = "vacation/likedvacations.html"
    context_object_name = "Liked"

    def handle_no_permission(self, request):
        return redirect('not_authorized')

    def get_queryset(self):
        return Vacation.objects.filter(likes=self.request.user)


@login_required(login_url=reverse_lazy('not_authorized'))
def like_vacation(request, pk):
    # Recupera l'oggetto Scheda
    vacation = get_object_or_404(Vacation, pk=pk)

    # Verifica se l'utente ha aggiunto questa vacanza alla lista "Fatte"
    fatte_list = List.objects.filter(user=request.user, name="Fatte").first()

    if fatte_list and fatte_list.vacations.filter(pk=vacation.pk).exists():
        # Controlla se l'utente ha già messo un like a questa vacanza
        if request.user in vacation.likes.all():
            vacation.likes.remove(request.user)
            messages.info(request, f'Hai rimosso il like dalla vacanza "{vacation.title}".')
        else:
            vacation.likes.add(request.user)
            messages.success(request, f'Hai messo like alla vacanza "{vacation.title}".')
    else:
        # Se la vacanza non è nella lista "Fatte", mostra un messaggio di avviso
        messages.warning(request, 'Devi prima aggiungere questa vacanza alla tua lista "Fatte" per poter mettere like.')

    return redirect(reverse("vacation:detailvacation", kwargs={"pk": pk}))


def search_vacation(request):
    form = VacationSearchForm(request.GET or None)
    vacations = None

    if request.GET and form.is_valid():  # Verifica se ci sono parametri GET e se il form è valido
        vacations = Vacation.objects.all()

        continente = form.cleaned_data.get('continente')
        if continente:  # Filtra solo se è stato selezionato un valore diverso da "Tutti"
            vacations = vacations.filter(continente=continente)

        durata = form.cleaned_data.get('durata')
        if durata:
            vacations = vacations.filter(durata=durata)

        tipologia = form.cleaned_data.get('tipologia')
        if tipologia:
            vacations = vacations.filter(tipologia=tipologia)

        prezzo = form.cleaned_data.get('prezzo')
        if prezzo:
            vacations = vacations.filter(prezzo=prezzo)

    return render(request, 'vacation/search_vacations.html', {'form': form, 'vacations': vacations})


def recommend_vacations(user):
    # Recupera le vacanze che l'utente ha piaciuto
    liked_vacations = user.liked_vacations.all()

    # Recupera tutte le vacanze nelle liste "da fare" dell'utente
    to_do_vacations = Vacation.objects.filter(user=user).filter(name='Da Fare')

    # Combina le due liste di vacanze
    all_vacations = liked_vacations | to_do_vacations

    # Se non ci sono vacanze salvate o piaciute, non fare nulla
    if not all_vacations.exists():
        return Vacation.objects.none()

    # Conta le occorrenze di ogni parametro tra le vacanze
    params = {
        'continente': [],
        'durata': [],
        'tipologia': [],
        'prezzo': []
    }

    for vacation in all_vacations:
        params['continente'].append(vacation.continente)
        params['durata'].append(vacation.durata)
        params['tipologia'].append(vacation.tipologia)
        params['prezzo'].append(vacation.prezzo)

    # Calcola il parametro più comune per ogni categoria
    most_common_params = {}
    for key, values in params.items():
        if values:
            most_common_params[key] = Counter(values).most_common(1)[0][0]

    # Filtra le vacanze in base ai parametri più comuni
    filtered_vacations = Vacation.objects.all()
    for key, value in most_common_params.items():
        if value:
            filter_kwargs = {key: value}
            filtered_vacations = filtered_vacations.filter(**filter_kwargs)

    # Ordina le vacanze in base al numero di "like"
    recommended_vacations = filtered_vacations.annotate(num_likes=Count('like')).order_by('-num_likes')

    return recommended_vacations
