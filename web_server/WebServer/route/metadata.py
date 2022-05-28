from WebServer.database.model import query_all
from django.http import HttpResponse

def metadata(request):
    response = query_all()
    return HttpResponse(response)