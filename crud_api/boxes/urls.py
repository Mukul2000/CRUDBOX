from . import views
from django.urls import path

urlpatterns = [
    path('api/boxes', views.BoxView.as_view(), name='boxes'),
    path('api/boxes/<int:id>', views.BoxView.as_view(), name='box')
]
