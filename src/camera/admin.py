from django.contrib import admin
from .models import Camera


@admin.register(Camera)
class CameraAdmin(admin.ModelAdmin):
    list_display = ("id", "ip_address", "plant", "top", "left", "direction", "description")
    list_filter = ("plant", "direction")
    search_fields = ("ip_address", "plant__name", "description")
    ordering = ("plant", "ip_address")
