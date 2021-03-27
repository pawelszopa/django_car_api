from django.conf.urls import url
from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from api.views import CarList, CarDetail, CarPopular, CarRating

schema_view = get_schema_view(
   openapi.Info(
      title="Cars API",
      default_version='v1',
      description="Endpoints of Car API",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)


urlpatterns = [
    path('cars/', CarList.as_view()),
    path('cars/<int:pk>', CarDetail.as_view()),
    path('cars/popular', CarPopular.as_view()),
    path('cars/rate', CarRating.as_view()),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]