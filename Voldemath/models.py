from django.db import models
from django.contrib.auth.models import User as AsilUser


class MakaleKonu(models.Model):
    konu_adi = models.CharField(max_length=150)
    tarih = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name_plural="Makale Konularımız"
    def __str__(self):
        return self.konu_adi


class Konu(models.Model):
    name = models.CharField(max_length=50)
    konukodu = models.CharField(max_length=20)
    tarih = models.DateTimeField(auto_now_add=True)
    ders_text = models.TextField(default="Konu hk. bilgi:...")
    class Meta:
        verbose_name_plural = "Konular"
    def __str__(self):
        return self.name


class User(AsilUser):
    follows = models.ManyToManyField(MakaleKonu,related_name="followed_by")
    isAdmin = models.BooleanField(default=False,null=True, blank=True)
    Makale_paylasabilir_mi = models.BooleanField(default=False, null=True, blank=True)
    Normal_paylasim_yapabilir_mi = models.BooleanField(default=False, null=True, blank=True)
    daha_once_paylasimci_istegi_yapti_mi = models.BooleanField(default=False, null=True, blank=True)
    daha_once_makaleci_istegi_yapti_mi = models.BooleanField(default=False, null=True, blank=True)
    hesap_aktif_mi = models.BooleanField(default=False, null=True, blank=True)


class Gonderi(models.Model):
    yazar = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    dosya = models.FileField(upload_to="files", null=True, blank=True)
    tarih = models.DateTimeField(auto_now_add=True)
    makale_konu = models.ForeignKey(Konu, on_delete=models.CASCADE)


class Duyurular(models.Model):
    baslik = models.CharField(max_length=100)
    text = models.CharField(max_length=1000)
    duyuru_tarih = models.DateTimeField(auto_now_add=True)


class Makale(models.Model):
    makaleyi_paylasan = models.ForeignKey(User, on_delete=models.CASCADE)
    makale_konu = models.ForeignKey(MakaleKonu,on_delete=models.CASCADE)
    makale_baslik = models.CharField(max_length=100)
    makale_yazar = models.CharField(max_length=150)
    makale_aciklama = models.CharField(max_length=1500)
    makale_anahtar_kelimeler = models.TextField(max_length=350)
    makale_yayinlanmis_mi = models.BooleanField(default=False)
    makale_pdf_dosya = models.FileField(upload_to="makale_pdfs", null=True, blank=True)
    makale_arkaplan_resmi = models.FileField(upload_to="makale_bgs", null=True, blank=True)
    makale_yukleme_tarihi = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name_plural="Makalelerimiz"