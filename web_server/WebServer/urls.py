from django.urls import path
from .test import test_model_db
from .route import metadata
urlpatterns = [
    path('test/model_insert', test_model_db.test_model_insert),
    path('test/model_query_all', test_model_db.test_model_query_all),
    path('test/model_delete_all', test_model_db.test_delete_all),
    path('metadata', metadata.metadata)
]
