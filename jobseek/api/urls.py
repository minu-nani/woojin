from django.conf import settings
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

urlpatterns = [
    path('v1/', include('jobseek.api.v1.urls')),
]

if settings.DEBUG:
    title = 'JobSeek API'
    version = 'v1'
    base_url = '/api'
    sv = get_schema_view(
        openapi.Info(
            title=title,
            default_version=version,
            description=f"JobSeek {version} Api List",
            terms_of_service="https://www.google.com/policies/terms/",
            contact=openapi.Contact(email="am.woojin@gmail.com"),
            license=openapi.License(name="MIT License"),
        ),
        permission_classes=(permissions.AllowAny,),
    )
    urlpatterns = [path('v1/docs/', sv.with_ui('swagger', cache_timeout=0)),] + urlpatterns

