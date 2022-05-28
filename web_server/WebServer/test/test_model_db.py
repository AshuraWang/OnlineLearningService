from WebServer.database.model import insert, query_all, delete_all
from django.http import HttpResponse

def test_model_insert(request):
    model_id = insert("mobilenet", "1111", 10, '../')
    print(f"Model {model_id} insert!")
    return HttpResponse(f"Model {model_id} insert!\n")


def test_model_query_all(request):
    response = query_all()
    return HttpResponse(response)


def test_delete_all(request):
    delete_all()
    return HttpResponse("Delete All Data in Model!!!!!\n")

