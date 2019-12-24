"""dergiBaba URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from Voldemath.views import *


urlpatterns = [
    path(r'', karsilama.as_view(), name='karsilama'),
    path(r'tum_akis/', anasayfa.as_view(), name="anasayfa"),
    path(r'kendi_akisim/', MYFLOW.as_view(), name="MYFLOW"),
    path(r'gonderi_sil/<int:gonderi_id>', gonderi_sil),
    path(r'kayit/', kayit.as_view(), name='kayıt'),
    path(r'giris/', giris.as_view(), name='giris'),
    path(r'yeniKonu/', yeniKonu.as_view()),
    path(r'yeniMakaleKonusu/', yeniMakaleKonu.as_view()),
    path(r'konu_listesi/', dersler.as_view(), name='konular'),
    path(r'yeni_paylasim/', yeni_paylasim.as_view(), name="yeniPaylasim"),
    path(r'makale_paylasim/', makale_paylasim.as_view(), name="makalePaylasim"),
    path(r'cikis/', cikis.as_view(), name='cikis'),
    path(r'dergimiz/',Dergimiz.as_view()),
    path(r'sifre_degistir/',Change_Your_Password.as_view()),
    path(r'follow/<int:ders_id>', Takip),
    path(r'-adminsec-/', admin.site.urls),
    path(r'yeniPaylasimci/14504169u<int:user_id>', yeniPaylasimci),
    path(r'yeniMakaleci/14504169u<int:user_id>', yeniMakaleci),
    path(r'kullaniciya_izin_ver/14504169u<int:user_id>', kullaniciya_izin_ver),
    path(r'kullaniciya_makale_izni_ver/14504169u<int:user_id>', kullaniciya_makale_izni_ver),
    path(r'duyurular/', duyurular.as_view()),
    path(r'hesabini_aktif_et/<str:username>', hesabi_aktif_et),
    path(r'tum_paylasimcilar/',Tum_paylasimcilar.as_view()),
    path(r'profilim/',Profilim.as_view()),
    path(r'paylasimci/<int:user_id>',paylasimci),
    path(r'tum_paylasimlar/',Tum_paylasimlar.as_view()),
    path(r'nasil_basladik/',Nasil_Basladik.as_view())
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)\
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)