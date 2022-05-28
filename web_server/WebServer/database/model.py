# -*- coding: utf-8 -*-
from TestModel.models import Model


def insert(architecture, timestamp, epoch, path):
    model = Model(architecture=architecture, timestamp=timestamp,
                  epoch=epoch,path=path)
    model.save()
    return model.model_id


def query_all():
    modellist = Model.objects.all()
    response = ''
    for model in modellist:
        response += f"id:{model.model_id}  {model.architecture}  " \
                    f"epoch:{model.epoch}  path:{model.path} " \
                    f" time:{model.timestamp}\n"
    return response


def get_latest_model_id():
    modellist = Model.objects.order_by("-model_id")
    if len(modellist) == 0:
        return -1
    return modellist[0].model_id, modellist[0].architecture, modellist[0].path


def delete_all():
    modellist = Model.objects.all()
    for model in modellist:
        model.delete()









