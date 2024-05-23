from django.urls import path
from . import views

app_name = "predict"

urlpatterns = [
    path('', views.index, name='index'),
    path('predict/', views.predict_chances, name='predict_chances'),
    path('results/', views.view_results, name='view_results'),
]