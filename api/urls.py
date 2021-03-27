from django.urls import path

from api.views import CarList, CarDetail, CarPopular, CarRating

urlpatterns = [
    path('cars/', CarList.as_view()),
    path('cars/<int:pk>', CarDetail.as_view()),
    path('cars/popular', CarPopular.as_view()),
    path('cars/rate', CarRating.as_view()),
]