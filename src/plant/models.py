from django.db import models


class Plant(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    layout = models.ImageField(upload_to="", null=True, blank=True)

    def __str__(self):
        return self.name
