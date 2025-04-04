from django.urls import path
from . import views

urlpatterns = [
    path("awattar_price/", views.index, name="index"),
]
