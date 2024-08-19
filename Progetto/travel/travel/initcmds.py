from typing import Dict, List

from vacation.models import Vacation


def erase_db():
    print("Cancello il DB")
    Vacation.objects.all().delete()


def init_db():
    if len(Vacation.objects.all()) != 0:
        return

    # se è vuoto lo inizializzo
    # può essere letto da fonti esterne, files, altri DB etc...

    vacationdict = dict(
        titles=["Viaggio nel Mediterraneo", "Alla Scoperta di Civilta' Antiche", "Natura Selvaggia: Viaggio tra"
                                                                                 "i Parchi Nazionali"],
        places=["Grecia e Italia", "Messico, Peru', Colombia", "Stati Uniti d'America"],
        durations=["2 Settimane", "2 Settimane", "4 Settimane"],
        prices=["$$", "$", "$$$"],
        types=["Mare e Citta", "Storico e Gastronomico", "Naturalistico"],
        seasons=["Estate", "Tutto l'anno", "Primavera o Autunno"],
        likes=[0, 0, 0]
    )

    for i in range(3):
        v = Vacation()
        for k in vacationdict:
            if k == 'titles':
                v.title = vacationdict[k][i]
            if k == 'places':
                v.place = vacationdict[k][i]
            if k == 'durations':
                v.duration = vacationdict[k][i]
            if k == 'prices':
                v.price = vacationdict[k][i]
            if k == 'types':
                v.type = vacationdict[k][i]
            if k == 'seasons':
                v.season = vacationdict[k][i]
            else:
                v.likes = vacationdict[k][i]
        print(v)
        v.save()

    print("DUMP DB")
    print(Vacation.objects.all())  # controlliamo
