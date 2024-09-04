from django import forms
from .models import List, Vacation, UserProfile


class VacationForm(forms.ModelForm):
    class Meta:
        model = Vacation
        exclude = ['like']  # Escludi il campo 'like'


# Form per aggiungere vacanze a una lista
class AddToListForm(forms.Form):
    LIST_CHOICES = [
        ('Fatte', 'Fatte'),
        ('Da Fare', 'Da Fare'),
    ]

    list = forms.ChoiceField(
        choices=LIST_CHOICES,
        label="Seleziona List",
        widget=forms.Select(attrs={"class": "form-control"})
    )

    def __init__(self, user, *args, **kwargs):
        super(AddToListForm, self).__init__(*args, **kwargs)
        self.user = user

    # Metodo che ritorna la lista selezionata o la crea in caso non esista
    def get_or_create_list(self):
        list_name = self.cleaned_data['list']
        lista, created = List.objects.get_or_create(
            name=list_name,
            user=self.user
        )
        return lista


# Form per la rimozione di una vacanza da una lista
class RemoveFromListForm(forms.Form):
    list = forms.ChoiceField(
        label="Seleziona Lista",
        widget=forms.Select(attrs={"class": "form-control"})
    )

    def __init__(self, user, vacation, *args, **kwargs):
        super(RemoveFromListForm, self).__init__(*args, **kwargs)
        self.user = user
        self.vacation = vacation
        # Filtra le liste dell'utente che contengono la vacanza corrente
        if user.is_authenticated:
            lists_with_vacation = user.list.filter(vacations=self.vacation)
            self.fields['list'].choices = [(lst.id, lst.name) for lst in lists_with_vacation]

    def remove_vacation(self):
        list_id = self.cleaned_data['list']
        selected_list = List.objects.get(id=list_id, user=self.user)
        selected_list.vacations.remove(self.vacation)


# Form per la ricerca di vacanze
class VacationSearchForm(forms.Form):
    # Aggiungiamo un'opzione vuota all'inizio delle scelte
    continente = forms.ChoiceField(choices=[('', 'Tutti')] + Vacation.CONTINENT_CHOICES, required=False)
    durata = forms.ChoiceField(choices=[('', 'Tutti')] + Vacation.DURATION_CHOICES, required=False)
    tipologia = forms.ChoiceField(choices=[('', 'Tutti')] + Vacation.TYPE_CHOICES, required=False)
    prezzo = forms.ChoiceField(choices=[('', 'Tutti')] + Vacation.PRICE_CHOICES, required=False)


# Form per cambiare immagine profilo
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_image']
