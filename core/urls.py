from rest_framework.routers import DefaultRouter
from django.contrib import admin
from django.urls import path,include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

import api.views as view_api


schema_view = get_schema_view(
   openapi.Info(
      title="Documentação da API",
      default_version="v1",
      description="Documentação da API crm-health-plan",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="brunoalvarim1@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
)

router = DefaultRouter()

router.register('customer',view_api.Customer,basename = 'customer')
router.register('plan',view_api.Plan,basename = 'plan')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path(
      "swagger/",
      schema_view.with_ui("swagger", cache_timeout=0),
      name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),

]