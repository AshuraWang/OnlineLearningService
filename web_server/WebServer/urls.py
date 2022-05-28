from django.urls import path
from .test import test_model_db, test_prediction_db
from .route import metadata, history, predict
urlpatterns = [
    path('test/model_insert', test_model_db.test_model_insert),
    path('test/model_query_all', test_model_db.test_model_query_all),
    path('test/model_delete_all', test_model_db.test_model_delete_all),
    path('test/pred_insert', test_prediction_db.test_pred_insert),
    path('test/pred_query_all', test_prediction_db.test_pred_query_all),
    path('test/pred_delete_all', test_prediction_db.test_pred_delete_all),
    path('metadata', metadata.metadata),
    path('predict', predict.predict),
    path('history', history.history)
]
