from vacation.models import *


def init_db():
    if len(Vacation.objects.all()) != 0:
        return

    # se è vuoto lo inizializzo
    # può essere letto da fonti esterne, files, altri DB etc...

    vacationdict = {
        "titles": ["Viaggio nel Mediterraneo", "Alla Scoperta di Civilta' Antiche", "Natura Selvaggia: Viaggio tra"
                                                                                    "i Parchi Nazionali"],
        "places": ["Grecia e Italia", "Messico, Peru', Colombia", "Stati Uniti d'America"],
        "durations": ["2 Settimane", "2 Settimane", "4 Settimane"],
        "prices": ["$$", "$", "$$$"],
        "types": ["Mare e Citta", "Storico e Gastronomico", "Naturalistico"],
        "seasons": ["Estate", "Tutto l'anno", "Primavera o Autunno"]

    }

    for i in range(3):
        v = Vacation()
        for k in vacationdict:
            if k == "titles":
                v.title = vacationdict[k][i]
            if k == "places":
                v.place = vacationdict[k][i]
            if k == "durations":
                v.duration = vacationdict[k][i]
            if k == "prices":
                v.price = vacationdict[k][i]
            if k == "types":
                v.type = vacationdict[k][i]
            else:
                v.season = vacationdict[k][i]
        # print(l)
        v.save()

    print("DUMP DB")
    print(Vacation.objects.all())  # controlliamo
