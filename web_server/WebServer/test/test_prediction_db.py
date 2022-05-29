from WebServer.database.prediction import insert, query_all, delete_all
from WebServer.database.model import get_latest_model_id
from django.http import HttpResponse
import uuid
import datetime


def test_pred_insert(request):
    rid = uuid.uuid4()
    model_id =get_latest_model_id()
    confidence = 0.9
    good = 1
    cost_time = 0.003
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d--%H:%M:%S')
    data = "123.jpg"

    request_id = insert(rid, model_id, confidence, good, cost_time, timestamp, data)
    print(f"prediction {request_id} insert!")
    return HttpResponse(f"Prediction {request_id} saved!\n")


def test_pred_query_all(request):
    response = query_all()
    return HttpResponse(response)


def test_pred_delete_all(request):
    delete_all()
    return HttpResponse("Delete All Data in Prediction!!!!!\n")



