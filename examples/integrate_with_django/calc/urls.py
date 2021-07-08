from django.urls import path

from calc import views

urlpatterns = [
    path('add', views.addition),
]
