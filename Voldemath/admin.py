from django.contrib import admin
from Voldemath.models import Gonderi, Konu, User, Duyurular, Makale, MakaleKonu


class KonuAdmin(admin.ModelAdmin):
    list_display = ['name', 'konukodu','ders_text','tarih']
    list_filter = ['name']

class GonderiAdmin(admin.ModelAdmin):
    list_display = ['yazar', 'text', 'tarih', 'makale_konu']
    list_filter = ['yazar', 'tarih']

class EgitmenAdmin(admin.ModelAdmin):
    list_display = ['isim', 'soyisim', 'unvan','unvan_ve_isim']
    list_filter = ['isim']


class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'first_name' ,'last_name','email']

class AnnouncementsAdmin(admin.ModelAdmin):
    list_display = ["baslik","text","gonderen_email"]

class DuyurularAdmin(admin.ModelAdmin):
    list_display = ["baslik","text","duyuru_tarih"]


class MakalelerAdmin(admin.ModelAdmin):
    list_display = ["makale_konu","makale_baslik","makale_yazar","makale_anahtar_kelimeler","makale_yukleme_tarihi"]
    list_filter = ["makale_yukleme_tarihi","makale_konu","makale_yazar"]


class MakaleKonuAdmin(admin.ModelAdmin):
    list_display = ["konu_adi","tarih"]
    list_filter = ["tarih","konu_adi"]


admin.site.register(MakaleKonu,MakaleKonuAdmin)
admin.site.register(Makale,MakalelerAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Konu, KonuAdmin)
admin.site.register(Gonderi,GonderiAdmin)
admin.site.register(Duyurular,DuyurularAdmin)
