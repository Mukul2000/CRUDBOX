from . import views
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    # path('api/users', views.UserView.as_view(), name='users'),
    path('api/login', obtain_auth_token, name='login')
]
