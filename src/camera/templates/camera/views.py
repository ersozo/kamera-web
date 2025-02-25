from django.shortcuts import render, get_object_or_404
from plant.models import Plant
from camera.models import Camera
from django.http import StreamingHttpResponse
from threading import Lock, Event, Thread
import cv2

USERNAME = "admin"
PASSWORD = "bakim.2023"

frame = None
cap = None  # Kamera nesnesini global olarak tanımlıyoruz
lock = Lock()  # Thread güvenliği için bir kilit oluşturuyoruz
stop_thread_event = Event()


def capture_frames(camera_ip):
    """
    Kameradan gelen çerçeveleri yakalayarak global frame değişkenine atar.
    """
    global frame, cap
    stop_thread_event.clear()
    with lock:
        if cap:
            cap.release()  # Önceki kamera bağlantısını serbest bırak
        full_ip = f"rtsp://{USERNAME}:{PASSWORD}@{camera_ip}"
        cap = cv2.VideoCapture(full_ip)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    while not stop_thread_event.is_set():
        with lock:
            if not cap.isOpened():
                print("Kamera bağlantısı açılmadı.")
                break
            success, frame = cap.read()
            if not success:
                print("Kamera çerçevesi alınamadı.")
                break


def generate_stream():
    """
    Canlı video akışı için JPEG çerçeveleri üreten bir jeneratör.
    """
    global frame
    while True:
        if frame is not None:
            ret, buffer = cv2.imencode(".jpg", frame)
            yield (
                b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n\r\n" + buffer.tobytes() + b"\r\n"
            )


def camera_stream(request,camera_id):
    """
    Belirtilen kameradan canlı yayın başlatır.
    """
    global stop_thread_event
    stop_thread_event.set()  # Mevcut thread'i durdur
    stop_thread_event = Event()  # Yeni bir event başlat
    camera = get_object_or_404(Camera, id=camera_id)
    camera_ip = camera.ip_address
    Thread(target=capture_frames, args=(camera_ip,), daemon=True).start()
    return StreamingHttpResponse(
        generate_stream(),
        content_type="multipart/x-mixed-replace; boundary=frame",
    )




def camera_list(request, plant_id):
    """
    Bir tesise ait kameraların listesini döndürür.
    """
    plant = get_object_or_404(Plant, id=plant_id)
    cameras = Camera.objects.filter(plant=plant_id)
    plant_name = plant.name
    context = {
        "plant_name":plant_name,
        "cameras": cameras,
    }
    return render(request, template_name="camera/camera_list.html", context=context)


def camera_stream_view(request, plant_id, camera_id):
    plant = get_object_or_404(Plant, id=plant_id)
    cameras = Camera.objects.filter(plant=plant_id)
    context = {
        "plant": plant.id,
        "camera_id": cameras,
        "stream_url": f"/camera/stream/{camera_id}/",
    }
    return render(request, template_name="camera/camera_stream.html", context=context)