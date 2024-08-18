from django.http import HttpResponse

def home_page(request):
    response = "Benvenuto nel mio sito"

    return HttpResponse(response)
