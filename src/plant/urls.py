# plant/urls.py
from django.urls import path
from . import views


urlpatterns = [
    path("", views.plant_list, name="plant_list"),
    path("plants/<int:plant_id>/", views.plant_layout, name="plant_layout"),
]
