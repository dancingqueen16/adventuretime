# Test sulla funzione 'reccomend_vacations' per i consigli di viaggio

from django.test import TestCase
from django.contrib.auth.models import User
from .models import Vacation, List
from .views import recommend_vacations


class RecommendVacationsTestCase(TestCase):

    def setUp(self):
        # Creazione di un utente di esempio
        self.user = User.objects.create(username="testuser")

        # Creazione di alcune vacanze di esempio da inserire nelle vacanze piaciute o "da fare"
        self.vacation1 = Vacation.objects.create(
            titolo="Viaggio Culturale in Europa",
            luogo="Parigi, Bruxelles, Amsterdam, Berlino",
            continente="Europa",
            durata="2 Settimane",
            prezzo="Budget Medio",
            tipologia="Culturale",
            periodo="Primavera"
        )
        self.vacation2 = Vacation.objects.create(
            titolo="Avventura in Asia",
            luogo="Thailandia",
            continente="Asia",
            durata="2 Settimane",
            prezzo="Viaggio Low Cost",
            tipologia="Avventura",
            periodo="Estate"
        )

        # Creazione di vacanze di esempio NON conosciute dall'utente
        self.vacation3 = Vacation.objects.create(
            titolo="Relax in Sud America",
            luogo="Brasile",
            continente="Sud America",
            durata="1 Settimana",
            prezzo="Viaggio Low Cost",
            tipologia="Relax",
            periodo="Inverno"
        )
        self.vacation4 = Vacation.objects.create(
            titolo="Safari in Africa",
            luogo="Kenya",
            continente="Africa",
            durata="3 Settimane",
            prezzo="Budget Alto",
            tipologia="Avventura",
            periodo="Autunno"
        )

        # Creazione di vacanze che corrispondono al parametro più comune
        self.vacation5 = Vacation.objects.create(
            titolo="Escursione in Europa",
            luogo="Spagna",
            continente="Europa",
            durata="2 Settimane",  # Parametro comune
            prezzo="Viaggio Low Cost",
            tipologia="Avventura",
            periodo="Primavera"
        )
        self.vacation6 = Vacation.objects.create(
            titolo="Tour dei Castelli in Scozia",
            luogo="Scozia",
            continente="Europa",
            durata="2 Settimane",  # Parametro comune
            prezzo="Budget Medio",
            tipologia="Culturale",
            periodo="Estate"
        )

        # Aggiungere la vacanza1 ai "like" dell'utente
        self.vacation1.like.add(self.user)

        # Creare una lista "Da Fare" e aggiungere la vacanza2
        self.todo_list = List.objects.create(user=self.user, name='Da Fare')
        self.todo_list.vacations.add(self.vacation2)

    def test_recommend_vacations(self):
        recommended_vacations, most_common_param = recommend_vacations(self.user)

        # Verifica che le vacanze gia' conosciute non siano consigliate
        self.assertNotIn(self.vacation1, recommended_vacations)
        self.assertNotIn(self.vacation2, recommended_vacations)

        # Verifica che le vacanze non conosciute con parametro piu' comune siano consigliate
        self.assertIn(self.vacation5, recommended_vacations)
        self.assertIn(self.vacation6, recommended_vacations)

        # Verifica che il parametro più comune sia corretto
        self.assertEqual(most_common_param, '2 Settimane')  # In questo caso "2 Settimane" dovrebbe essere il più comune

    def test_recommend_vacations_no_likes_or_todo(self):
        # Crea un utente senza like o vacanze "Da Fare"
        new_user = User.objects.create(username="newuser")

        recommended_vacations, most_common_param = recommend_vacations(new_user)

        # Verifica che nessuna vacanza venga raccomandata
        self.assertFalse(recommended_vacations)
        self.assertIsNone(most_common_param)

# Test sulla vista di ricerca viaggi
from django.test import TestCase
from django.urls import reverse
from .models import Vacation
from django.core.cache import cache


class SearchVacationViewTestCase(TestCase):

    def setUp(self):
        cache.clear()
        # Creazione di alcune vacanze di esempio
        self.vacation1 = Vacation.objects.create(
            titolo="Weekend a Parigi",
            luogo="Parigi",
            continente="Europa",
            durata="Weekend Lungo (2-4 Giorni)",
            prezzo="Budget Medio",
            tipologia="Culturale",
            periodo="Primavera"
        )
        self.vacation2 = Vacation.objects.create(
            titolo="Safari in Africa",
            luogo="Kenya",
            continente="Africa",
            durata="1 Settimana",
            prezzo="Viaggio di Lusso",
            tipologia="Avventura",
            periodo="Estate"
        )

        self.vacation3 = Vacation.objects.create(
            titolo="Viaggio Culturale in Asia",
            luogo="Giappone",
            continente="Asia",
            durata="2 Settimane",
            prezzo="Budget Medio",
            tipologia="Culturale",
            periodo="Autunno"
        )
        self.vacation4 = Vacation.objects.create(
            titolo="Avventura in Sud America",
            luogo="Brasile",
            continente="Sud America",
            durata="2 Settimane",
            prezzo="Viaggio Low Cost",
            tipologia="Avventura",
            periodo="Inverno"
        )

    def test_search_vacation_by_continent(self):
        response = self.client.get(reverse('vacation:search_vacations'), {'continente': 'Europa'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.vacation1.titolo)
        self.assertNotContains(response, self.vacation2.titolo)
        self.assertNotContains(response, self.vacation3.titolo)
        self.assertNotContains(response, self.vacation4.titolo)

    def test_search_vacation_no_filters(self):
        response = self.client.get(reverse('vacation:search_vacations'), {
            'continente': '',
            'durata': '',
            'tipologia': '',
            'prezzo': ''
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.vacation1.titolo)
        self.assertContains(response, self.vacation2.titolo)
        self.assertContains(response, self.vacation3.titolo)
        self.assertContains(response, self.vacation4.titolo)

    def test_search_vacation_by_type(self):
        response = self.client.get(reverse('vacation:search_vacations'), {'tipologia': 'Avventura'})
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, self.vacation1.titolo)
        self.assertContains(response, self.vacation2.titolo)
        self.assertNotContains(response, self.vacation3.titolo)
        self.assertContains(response, self.vacation4.titolo)

    def test_search_vacation_by_duration(self):
        response = self.client.get(reverse('vacation:search_vacations'), {'durata': '2 Settimane'})
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, self.vacation1.titolo)
        self.assertNotContains(response, self.vacation2.titolo)
        self.assertContains(response, self.vacation3.titolo)
        self.assertContains(response, self.vacation4.titolo)

    def test_search_vacation_by_budget(self):
        response = self.client.get(reverse('vacation:search_vacations'), {'prezzo': 'Budget Medio'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.vacation1.titolo)
        self.assertNotContains(response, self.vacation2.titolo)
        self.assertContains(response, self.vacation3.titolo)
        self.assertNotContains(response, self.vacation4.titolo)

    def test_search_vacation_multiple_filters(self):
        response = self.client.get(reverse('vacation:search_vacations'), {
            'continente': 'Asia',
            'durata': '2 Settimane',
            'tipologia': 'Culturale'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.vacation3.titolo)  # Vacanza che corrisponde a tutti i filtri
        self.assertNotContains(response, self.vacation1.titolo)  # Non dovrebbe comparire
        self.assertNotContains(response, self.vacation2.titolo)  # Non dovrebbe comparire
        self.assertNotContains(response, self.vacation1.titolo)

    def test_search_vacation_no_match(self):
        response = self.client.get(reverse('vacation:search_vacations'), {
            'continente': 'Oceania'
        })
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, self.vacation1.titolo)
        self.assertNotContains(response, self.vacation2.titolo)
        self.assertNotContains(response, self.vacation3.titolo)
        self.assertNotContains(response, self.vacation4.titolo)
