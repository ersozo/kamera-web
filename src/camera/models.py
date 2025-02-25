from django.db import models
from plant.models import Plant


class Camera(models.Model):
    ip_address = models.GenericIPAddressField()
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE)
    top = models.PositiveIntegerField()
    left = models.PositiveIntegerField()
    direction = models.IntegerField()
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Camera {self.ip_address} at {self.plant.name}"
