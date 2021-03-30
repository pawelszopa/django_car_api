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

app_name = 'api'

urlpatterns = [
    path('cars/', CarList.as_view(), name='car_list'),
    path('cars/<int:pk>', CarDetail.as_view(), name='car_detail'),
    path('popular/', CarPopular.as_view(), name='car_popular'),
    path('rate/', CarRating.as_view(), name='car_rate'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
