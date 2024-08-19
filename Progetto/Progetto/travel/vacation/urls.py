from django.urls import path
from .views import *

app_name = 'vacation'

urlpatterns = [
     path("vacationlist/", vacation_list, name="vacation_list"),
     path("vacationlistview/", VacationListView.as_view(), name="vacation_listview"),
     path("createvacation/", CreateVacationView.as_view(), name="createvacation"),
     path("")
]
