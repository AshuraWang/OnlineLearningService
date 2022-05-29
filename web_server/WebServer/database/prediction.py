# -*- coding: utf-8 -*-
from DatabaseModel.models import Prediction

GOOD_DICT = {0: "NG", 1: "OK"}


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
    plist = Prediction.objects.order_by("timestamp")
    response = ''
    history_list = []
    for pred in plist:
        r = f"model_id: {'%3d'%pred.model_id}    " \
            f"confidence: {'%.2f'%pred.confidence}    " \
            f"good: {GOOD_DICT[pred.good]}    " \
            f"cost_time: {'% 3d'%pred.cost_time}    " \
            f"timestamp: {pred.timestamp}    " \
            f"data: {'%40s' % pred.data}    " \
            f"request_id: {'%40s' % pred.request_id}\n    "
            # r = "{0: >100s}".format(pred.request_id)
        response += r

        history = ['%300s' % pred.data, GOOD_DICT[pred.good], '%.2f'%pred.confidence,
                   '%3d'%pred.model_id,   '% 3dms'%pred.cost_time,
                   pred.timestamp, '%300s' % pred.request_id]
        history_list.append(history)
    return response, history_list



def delete_all():
    plist = Prediction.objects.all()
    for pred in plist:
        pred.delete()
