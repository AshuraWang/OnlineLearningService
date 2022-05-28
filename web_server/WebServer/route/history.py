from WebServer.database.prediction import query_all
from django.http import HttpResponse


def history(request):
    response = query_all()
    return HttpResponse(response)