"""MPbackend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi, views
from rest_framework import permissions
from rest_framework_swagger.views import get_swagger_view
from django.conf import settings
from django.conf.urls.static import static
# from django.conf.urls import url

from account.views import myindex


schema_view = get_swagger_view(title="FULL BLACK API")

redoc_schema_view = views.get_schema_view(
   openapi.Info(
      title="AO APIs",
      default_version='v1',
      description="API Documentation of American Outlets backend",
      terms_of_service="#",
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    
    path('docs/', redoc_schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', redoc_schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('admin/', admin.site.urls),
    path('api/',include('account.urls')),
    path('', myindex, name='index')
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)