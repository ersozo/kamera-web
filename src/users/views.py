from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import RegisterForm

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # Kullanıcı nesnesini oluştur
            user.set_password(
                form.cleaned_data["password1"]
            )  # Şifreyi güvenli hale getir
            user.save()  # Kullanıcıyı kaydet
            login(request, user)  # Otomatik giriş yap
            messages.success(
                request, "Hesabınız başarıyla oluşturuldu ve giriş yaptınız."
            )
            return redirect("plant_list")  # Kullanıcıyı yönlendir
    else:
        form = RegisterForm()  # Boş form oluştur

    return render(request, "users/register.html", {"form": form})


# Kullanıcı Girişi
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(
            request, data=request.POST
        )  # `data=request.POST` olarak düzeltilmeli
        if form.is_valid():
            user = form.get_user()  # Doğrudan kullanıcı nesnesini al
            login(request, user)  # Kullanıcıyı giriş yap
            messages.success(request, "Başarıyla giriş yaptınız.")
            return redirect("plant_list")  # Giriş sonrası yönlendirme
        else:
            messages.error(
                request, "Geçersiz kullanıcı adı veya parola."
            )  # Hata mesajı
    else:
        form = AuthenticationForm()  # Boş form göster

    return render(request, "users/login.html", {"form": form})  # Formu sayfaya gönder


# Kullanıcı Çıkışı
def logout_view(request):
    logout(request)  # Kullanıcıyı çıkış yap
    messages.success(request, "Başarıyla çıkış yaptınız.")  # Bilgilendirme mesajı
    return redirect("plant_list")  # Ana sayfaya yönlendir
