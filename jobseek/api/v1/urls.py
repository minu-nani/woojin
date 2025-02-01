from django.urls import path, include

urlpatterns = [
    path('users/', include('jobseek.api.v1.users.urls')),
]