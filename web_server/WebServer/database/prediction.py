# -*- coding: utf-8 -*-
from TestModel.models import Prediction


def insert(request_id, model_id, confidence, good, cost_time, timestamp, data):
    prediciton = Prediction(
        request_id=request_id,
        model_id=model_id,
        confidence=confidence,
        good=good,
        cost_time=cost_time,
        timestamp=timestamp,
        data=data
    )
    prediciton.save()
    return prediciton.request_id


def query_all():
    plist = Prediction.objects.order_by("-timestamp")
    response = ''
    for pred in plist:
        response += f"request_id:{pred.request_id}  " \
                    f"model_id:{pred.model_id}  " \
                    f"confidence:{pred.confidence}  " \
                    f"good:{pred.good}  " \
                    f"cost_time:{pred.cost_time}  " \
                    f"timestamp:{pred.timestamp}  " \
                    f"data:{pred.data}\n"
    return response



def delete_all():
    plist = Prediction.objects.all()
    for pred in plist:
        pred.delete()
