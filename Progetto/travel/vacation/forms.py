from django import forms
from .models import List


'''class AddToListForm(forms.Form):
    STATUS_CHOICES = [
        ('TODO', 'To Do'),
        ('DONE', 'Done'),
    ]
    status = forms.ChoiceField(choices=STATUS_CHOICES, label='Add to list')
'''


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
