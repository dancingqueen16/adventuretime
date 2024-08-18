from django.urls import path
from .views import *

app_name = 'vacation'

urlpatterns = [
     path("vacationlist/", vacation_list, name="vacation_list")

]
