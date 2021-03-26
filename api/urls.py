from django.urls import path

from api.views import CarList

urlpatterns = [
    path('cars/', CarList.as_view())
]