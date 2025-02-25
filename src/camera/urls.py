# camera/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("cameras/plants/<int:plant_id>/", views.camera_list, name="camera_list"),
    path(
        "camera/stream/<int:camera_id>/",
        views.camera_stream,
        name="camera_stream",
    ),
    path(
        "camera/view/<int:plant_id>/<int:camera_id>/",
        views.camera_stream_view,
        name="camera_stream_view",
    ),
    path(
        "camera/stop/<int:plant_id>/<int:camera_id>/",
        views.stop_camera_stream_view,
        name="stop_camera_stream_view",
    ),
    path(
        "camera/go/<int:plant_id>/<int:camera_id>/",
        views.go_to_camera_ip,
        name="go_to_camera_ip",
    ),
    path("camera/", views.camera_stop_info, name="camera_stop_info")
]
