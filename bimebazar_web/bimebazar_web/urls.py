from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="BimeBazar API",
      default_version='v1',
      description="This is Swagger docs for BimeBazar API",
    #   terms_of_service="http://SirSaleh.github.io/",
      contact=openapi.Contact(email="animatorsaleh@gmail.com"),
    #   license=openapi.License(name="MIT"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('admin/', admin.site.urls),
    path('api/', include(('api.urls', 'api'), namespace='api')),
]
