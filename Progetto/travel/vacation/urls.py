from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import *

app_name = 'vacation'

urlpatterns = [
     # Path lista vacanze
     path("vacationlist/", VacationListView.as_view(), name="vacationlist"),
     # Path per creazione, modifica e cancellazione vacanze
     path("createvacation/", CreateVacationView.as_view(), name="createvacation"),
     path("editvacation/<int:pk>/", UpdateVacationView.as_view(), name="editvacation"),
     path("deletevacation/<pk>/", DeleteVacationView.as_view(), name="deletevacation"),
     # Path dettaglio vacanza e like
     path("vacationdetail/<int:pk>/", VacationDetailView.as_view(), name="detailvacation"),
     path("vacationdetail/<int:pk>/like", like_vacation, name="like"),
     # Path ricerca vacanza
     path('search/', search_vacation, name='search_vacations'),
     # Path per profilo e correlati: cambio immagine, visualizzazione liste vacanze
     path("myprofile", my_profile, name="myprofile"),
     path("donevacations", DoneVacations.as_view(), name="donevacations"),
     path("todovacations", ToDoVacations.as_view(), name="todovacations"),
     path("likedvacations", LikedVacations.as_view(), name="likedvacations"),
     path('change_picture/', change_pic, name='change_picture')
   ]

