from django.urls import path
from .views import *

app_name = 'vacation'

urlpatterns = [
     path("vacationlist/", VacationListView.as_view(), name="vacationlist"),
     path("createvacation/", CreateVacationView.as_view(), name="createvacation"),
     path("vacationdetail/<int:pk>/", VacationDetailView.as_view(), name="detailvacation"),
     path("vacationdetail/<int:pk>/like", like_vacation, name="like"),
     path("editvacation/<int:pk>/", UpdateVacationView.as_view(), name="editvacation"),
     path("deletevacation/<pk>/", DeleteVacationView.as_view(), name="deletevacation"),
     path("myprofile", my_profile, name="myprofile"),
     path("donevacations", DoneVacations.as_view(), name="donevacations"),
     path("todovacations", ToDoVacations.as_view(), name="todovacations"),
     path("likedvacations", LikedVacations.as_view(), name="likedvacations"),
     path('search/', search_vacation, name='search_vacations')
   ]

