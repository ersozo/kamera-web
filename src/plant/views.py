# plant/views.py
from django.shortcuts import render, get_object_or_404
from plant.models import Plant
from camera.models import Camera
from django.contrib.auth.decorators import login_required

def plant_list(request):
    plants = Plant.objects.all()
    context = {"plants": plants}
    return render(request, template_name="plant/city.html", context=context)

@login_required(login_url="login")
def plant_layout(request, plant_id):
    plant = get_object_or_404(Plant, id=plant_id)
    cameras = Camera.objects.filter(plant=plant)
    context = {
        "plant_name": plant.name,
        "plant": plant,
        "cameras": cameras,
    }
    return render(request, template_name="plant/plant_layout.html", context=context)

