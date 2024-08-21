from django.urls import path
from .views import *

app_name = 'vacation'

urlpatterns = [
     path("vacationlist/", VacationListView.as_view(), name="vacationlist"),
     path("createvacation/", CreateVacationView.as_view(), name="createvacation"),
     path("vacationdetail/<int:pk>/", DetailVacationView.as_view(), name="detailvacation"),
     path("editvacation/<int:pk>/", UpdateVacationView.as_view(), name="editvacation"),
     path("deletevacation/<pk>/", DeleteVacationView.as_view(), name="deletevacation"),
     path("myprofile", my_profile, name="myprofile")
]
