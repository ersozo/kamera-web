# -*- coding: utf-8 -*-
from django.urls import reverse
from django.shortcuts import get_object_or_404, render, redirect
from camera.models import Camera, Plant
from django.http import StreamingHttpResponse
from threading import Lock, Event, Thread
import cv2
import time
from django.contrib import messages
import logging

USERNAME = "admin"
PASSWORD = "bakim.2023"

# Kamera akışlarını yöneten global bir sözlük
camera_streams = {}

cv2.setNumThreads(1)

class CameraStream:
    def __init__(self, ip, username, password):
        self.ip = ip
        self.username = username
        self.password = password
        self.cap = None
        self.frame = None
        self.lock = Lock()
        self.stop_event = Event()
        self.thread = None
        self.last_frame_time = 0  # FPS kontrolü için
        self.frame_interval = 1 / 20  # Maksimum 20 FPS

    def start(self):
        """
        Kameradan görüntü yakalamaya başlar.
        """
        if self.thread is None or not self.thread.is_alive():
            self.stop_event.clear()
            self.thread = Thread(target=self._capture_frames, daemon=True)
            self.thread.start()

    def _connect_camera(self):
        """
        Kameraya bağlantıyı başlatır.
        """
        full_ip = f"rtsp://{self.username}:{self.password}@{self.ip}?udp"
        self.cap = cv2.VideoCapture(full_ip)
        if not self.cap.isOpened():
            print(f"Bağlantı başarısız: {self.ip}")
            return False

        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 3)  # Buffer'ı sınırla
        self.cap.set(cv2.CAP_PROP_FPS, 15)  # Maksimum 15 FPS

        print(f"Kamera bağlantısı başarılı: {self.ip}")
        return True

    def _capture_frames(self):
        """
        Kameradan alınan kareleri sürekli olarak günceller.
        Optimize edilmiş versiyon - daha iyi hata yönetimi ve frame kontrolü ile.
        """
        reconnect_delay = 1.0  # Yeniden bağlanma için bekleme süresi

        while not self.stop_event.is_set():
            try:
                # Kamera bağlantısını kontrol et ve gerekirse yeniden bağlan
                if self.cap is None or not self.cap.isOpened():
                    print(f"Kamera bağlantısı kuruluyor: {self.ip}")
                    if not self._connect_camera():
                        time.sleep(reconnect_delay)
                        continue

                # Frame'i oku
                success, frame = self.cap.read()
                if not success:
                    print(f"Frame okunamadı: {self.ip}")
                    self.cap.release()
                    self.cap = None
                    continue

                # FPS kontrolü
                current_time = time.time()
                time_diff = current_time - self.last_frame_time

                if time_diff >= self.frame_interval:
                    with self.lock:
                        self.frame = frame
                    self.last_frame_time = current_time
                else:
                    # FPS limitini aşmamak için kısa bir süre bekle
                    sleep_time = max(0, self.frame_interval - time_diff)
                    time.sleep(sleep_time * 0.5)  # Tam interval'in yarısı kadar bekle

            except cv2.error as e:
                print(f"OpenCV hatası: {e}")
                if self.cap:
                    self.cap.release()
                    self.cap = None
                time.sleep(0.1)

            except Exception as e:
                print(f"Beklenmeyen hata: {e}")
                if self.cap:
                    self.cap.release()
                    self.cap = None
                time.sleep(0.1)

    def stop(self):
        """
        Kameradan gelen akışı durdurur.
        """
        self.stop_event.set()
        print(f"Kamera akışı durduruldu: {self.ip}")
        if self.cap:
            self.cap.release()
            self.cap = None

    def get_frame(self):
        """
        Son kaydedilen frame'i döndürür.
        """
        with self.lock:
            return self.frame


def get_camera_stream(camera_ip):
    """
    Eğer kamera için daha önce başlatılmış bir akış yoksa yeni bir tane başlatır.
    """
    if camera_ip not in camera_streams:
        camera_streams[camera_ip] = CameraStream(camera_ip, USERNAME, PASSWORD)
        camera_streams[camera_ip].start()
    return camera_streams[camera_ip]


def generate_stream(camera_stream):
    """
    Kamera akışını oluşturur.
    """
    while True:
        frame = camera_stream.get_frame()
        if frame is not None:
            ret, buffer = cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
            yield (
                b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n\r\n" + buffer.tobytes() + b"\r\n"
            )
        else:
            time.sleep(0.05)

def camera_stream(request, camera_id):
    """
    Belirtilen kamera için canlı yayın başlatır.
    """
    camera = get_object_or_404(Camera, id=camera_id)
    camera_ip = camera.ip_address
    camera_stream_obj = get_camera_stream(camera_ip)
    return StreamingHttpResponse(
        generate_stream(camera_stream_obj),
        content_type="multipart/x-mixed-replace; boundary=frame",
    )


def stop_camera_stream(camera_id):
    """
    Belirtilen kameranın akışını durdurur.
    """
    camera = get_object_or_404(Camera, id=camera_id)
    camera_ip = camera.ip_address
    if camera_ip in camera_streams:
        camera_streams[camera_ip].stop()
        del camera_streams[camera_ip]


def camera_stream_view(request, plant_id, camera_id):
    """
    Seçilen kameranın canlı yayınını görüntüler.
    """
    plant = get_object_or_404(Plant, id=plant_id)
    camera = get_object_or_404(Camera, id=camera_id, plant=plant)
    return render(
        request,
        "camera/camera_stream.html",
        {
            "plant": plant,
            "camera": camera,
            "stream_url": f"/camera/stream/{camera_id}/",
        },
    )


# def stop_camera_stream_view(request, plant_id, camera_id):
#     """
#     Kamerayı durdurur ve layout'a geri döner.
#     """
#     stop_camera_stream(camera_id)
#     return redirect(reverse("plant_layout", kwargs={"plant_id": plant_id}))


logger = logging.getLogger(__name__)

def stop_camera_stream_view(request, plant_id, camera_id):
    """
    Kamerayı durdurur ve ana sayfaya döner.
    """
    try:
        stop_camera_stream(camera_id)
        messages.success(request, "Kamera durduruldu.")
    except Exception as e:
        logger.error(f"Kamera durdurulurken hata oluştu: {e}")
    # return render(request, template_name="plant/city.html", context=context)
    return render(
        request, template_name="camera/camera_stop_info.html")

def go_to_camera_ip(request, plant_id, camera_id):
    """
    Kameraya doğrudan yönlendirme yapar.
    """
    camera = get_object_or_404(Camera, id=camera_id)
    camera_ip = camera.ip_address
    return redirect(f"http://{camera_ip}")



def camera_list(request, plant_id):
    """
    Bir tesise ait kameraların listesini döndürür.
    """
    plant = get_object_or_404(Plant, id=plant_id)
    # cameras = Camera.objects.filter(plant=plant_id)
    cameras = Camera.objects.filter(plant=plant_id)
    plant_name = plant.name
    context = {
        "plant": plant_id,
        "plant_name": plant_name,
        "cameras": cameras,
    }
    return render(request, template_name="camera/camera_list.html", context=context)



def camera_stop_info(request, plant_id):
    """
    Kamera durdurma bilgisini gösteren sayfa.
    """
    return render(request, "camera/camera_stop_info.html")
