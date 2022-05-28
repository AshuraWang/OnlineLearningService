from django.db import models


class Model(models.Model):
    model_id = models.AutoField(primary_key=True)
    architecture = models.CharField(max_length=40)
    timestamp = models.CharField(max_length=40)
    epoch = models.IntegerField()
    path = models.CharField(max_length=100)


class Prediction(models.Model):
    request_id = models.CharField(max_length=40, primary_key=True)
    model_id = models.IntegerField()
    confidence = models.FloatField()
    good = models.IntegerField()
    cost_time = models.FloatField()
    timestamp = models.CharField(max_length=40)
    data = models.CharField(max_length=100)