class GonderiClass:
    def __init__(self,id,yazar,text,dosya,tarih,makale_konu,keywords, yayinlanmis_mi, baslik, arkaplan):
        self.id = id
        self.yazar = yazar
        self.text = text
        self.dosya = dosya
        self.tarih = tarih
        self.makale_konu = makale_konu
        self.anahtar_kelimeler = keywords
        self.makale_yayinlanmis_mi = yayinlanmis_mi
        self.makale_baslik = baslik
        self.makale_arkaplan_resmi = arkaplan


class PaylasimClass:
    def __init__(self,yazar,text,dosya,tarih,makale_konu,dosyaturu):
        self.yazar = yazar
        self.text = text
        self.dosya = dosya
        self.tarih = tarih
        self.makale_konu = makale_konu
        self.dosya_turu = dosyaturu


class Filters:
    def __init__(self,makale):
        self.makale = makale
        self.tag = str(makale.makale_konu).replace(" ","-")
