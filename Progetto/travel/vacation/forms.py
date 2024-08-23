from django import forms
from .models import VacationList


class AddToListForm(forms.Form):
    STATUS_CHOICES = [
        ('TODO', 'To Do'),
        ('DONE', 'Done'),
    ]
    status = forms.ChoiceField(choices=STATUS_CHOICES, label='Add to list')
