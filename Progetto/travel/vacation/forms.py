from django import forms
from .models import List, Vacation


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

    def get_or_create_list(self):
        list_name = self.cleaned_data['list']
        list, created = List.objects.get_or_create(
            name=list_name,
            user=self.user
        )
        return list


class VacationSearchForm(forms.Form):
    # Aggiungiamo un'opzione vuota all'inizio delle scelte
    continente = forms.ChoiceField(choices=[('', 'Tutti')] + Vacation.CONTINENT_CHOICES, required=False)
    durata = forms.ChoiceField(choices=[('', 'Tutti')] + Vacation.DURATION_CHOICES, required=False)
    tipologia = forms.ChoiceField(choices=[('', 'Tutti')] + Vacation.TYPE_CHOICES, required=False)
    prezzo = forms.ChoiceField(choices=[('', 'Tutti')] + Vacation.PRICE_CHOICES, required=False)
