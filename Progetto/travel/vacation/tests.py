from django.test import TestCase
from django.contrib.auth.models import User
from travel.vacation.models import Vacation, List
from travel.vacation.views import recommend_vacations


class RecommendVacationsTestCase(TestCase):

    def setUp(self):
        # Creazione di un utente di esempio
        self.user = User.objects.create(username="testuser")

        # Creazione di alcune vacanze di esempio
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

        # Aggiungere la vacanza1 ai "like" dell'utente
        self.vacation1.like.add(self.user)

        # Creare una lista "Da Fare" e aggiungere la vacanza2
        self.todo_list = List.objects.create(user=self.user, name='Da Fare')
        self.todo_list.vacations.add(self.vacation2)

    def test_recommend_vacations(self):
        recommended_vacations, most_common_param = recommend_vacations(self.user)

        # Verifica che le vacanze siano raccomandate in base ai parametri
        self.assertIn(self.vacation1, recommended_vacations)
        self.assertIn(self.vacation2, recommended_vacations)

        # Verifica che il parametro più comune sia corretto
        self.assertEqual(most_common_param, '2 Settimane')  # In questo caso "2 Settimane" dovrebbe essere il più comune

    def test_recommend_vacations_no_likes_or_todo(self):
        # Crea un utente senza like o vacanze "Da Fare"
        new_user = User.objects.create(username="newuser")

        recommended_vacations, most_common_param = recommend_vacations(new_user)

        # Verifica che nessuna vacanza venga raccomandata
        self.assertFalse(recommended_vacations)
        self.assertIsNone(most_common_param)
