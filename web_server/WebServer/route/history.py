from WebServer.database.prediction import query_all
from django.http import HttpResponse
from django.shortcuts import render


def history(request):
    nohtml = request.POST.get("nohtml")
    print(request.method)
    response, history_list = query_all()
    if not nohtml:
        return render(request, "history.html", {"history_list":history_list})
    else:
        return HttpResponse(response)