from django.urls import path
from . import views
from plant.views import plant_list

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("plants/", plant_list, name="plant_list"),
]
