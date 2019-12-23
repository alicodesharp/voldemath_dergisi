from django import forms
from Voldemath.models import Konu, Gonderi, Makale, MakaleKonu


class GirisForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(max_length=30, widget=forms.PasswordInput)


class yeniKonuForm(forms.Form):
    konuname = forms.CharField(max_length=100)


class yeniMakaleKonuForm(forms.Form):
    konuname = forms.CharField(max_length=150)


class GonderiForm(forms.Form):
    text = forms.CharField(max_length=500)
    dosya = forms.FileField(required=False)
    ders = forms.ModelChoiceField(
        queryset= Konu.objects.all(),
        label="ders"
    )


class makaleGonderiForm(forms.Form):
    makale_konu = forms.ModelChoiceField(
        queryset=MakaleKonu.objects.all(),
        label="makale_konu"
    )
    makale_baslik = forms.CharField(max_length=100)
    makale_yazar = forms.CharField(max_length=150)
    makale_aciklama = forms.CharField(max_length=1500)
    makale_anahtar_kelimeler = forms.CharField(max_length=350)
    makale_pdf_dosya = forms.FileField(required=False)
    makale_arkaplan_resmi = forms.FileField(required=False)


class changePassForm(forms.Form):
    eski_password = forms.CharField(max_length=20)
    new_password = forms.CharField(max_length=20)
    new_password_again = forms.CharField(max_length=20)


class ProfilForm(forms.Form):
    pass


class AramaMotoruForm(forms.Form):
    aratilan_kelime = forms.CharField(max_length=100)


class KayitForm(forms.Form):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    email = forms.CharField(max_length=50)
    username = forms.CharField(max_length=50)
    password = forms.CharField(max_length=30, widget=forms.PasswordInput)


class DerslerForm(forms.Form):
    ders = forms.ModelChoiceField(
        queryset=Konu.objects.all(),
        label="Makale konu"
    )
