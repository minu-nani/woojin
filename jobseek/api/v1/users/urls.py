from django.urls import path
from django.conf import settings
from . import views as user_views

urlpatterns = [
    path('user', user_views.UserViewSet.as_view({'get': 'list', 'post': 'create'}),
         name='user_basic')
]
