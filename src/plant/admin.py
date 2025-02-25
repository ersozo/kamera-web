from django.contrib import admin
from .models import Plant


@admin.register(Plant)
class PlantAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "created_at",
        "layout",
    )  # Fields displayed in the admin list view
    list_filter = ("created_at",)  # Filters for the admin interface
    search_fields = ("name",)  # Searchable fields
    ordering = ("-created_at",)  # Default ordering of the list
