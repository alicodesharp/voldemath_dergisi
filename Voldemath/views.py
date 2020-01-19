from django.shortcuts import render, redirect
from Voldemath.forms import GirisForm, KayitForm, yeniKonuForm, GonderiForm, DerslerForm, ProfilForm, changePassForm, makaleGonderiForm, yeniMakaleKonuForm, AramaMotoruForm
from django.contrib.auth import authenticate, login, logout
from django.views.generic import TemplateView, RedirectView, FormView
from Voldemath.models import Gonderi, Konu, User, Duyurular, Makale, MakaleKonu
from django.core.paginator import Paginator
from Voldemath.classes import GonderiClass, Filters, PaylasimClass
from random import shuffle
from django.core.mail import send_mail
from django.contrib import messages


class Tum_paylasimlar(TemplateView):
    template_name = "Giris_Yaptiktan_Sonra/Tum_paylasimlar_akis.html"

    def get_context_data(self, **kwargs):
        context = super(Tum_paylasimlar, self).get_context_data(**kwargs)
        ordered_paylasimlar = Gonderi.objects.all().order_by("-tarih")
        Paylasimlar = []
        for paylasim in ordered_paylasimlar:
            Paylasimlar.append(paylasim)

        Paylasimlar_W_Attr = []
        for j in range(len(Gonderi.objects.all())):
            if str(Paylasimlar[j].dosya).endswith(".png") or str(Paylasimlar[j].dosya).endswith(".JPG") or str(
                    Paylasimlar[j].dosya).endswith(".jpeg") or str(Paylasimlar[j].dosya).endswith(".jpg") or str(
                    Paylasimlar[j].dosya).endswith(".gif") or str(Paylasimlar[j].dosya).endswith(".eps") or str(
                    Paylasimlar[j].dosya).endswith(".bmp") or str(Paylasimlar[j].dosya).endswith(".raw") or str(
                    Paylasimlar[j].dosya).endswith(".psd"):
                Paylasimlar_W_Attr.append(
                    PaylasimClass(Paylasimlar[j].yazar, Paylasimlar[j].text, Paylasimlar[j].dosya, Paylasimlar[j].tarih,
                                  Paylasimlar[j].makale_konu, "Resim"))
            else:
                Paylasimlar_W_Attr.append(
                    PaylasimClass(Paylasimlar[j].yazar, Paylasimlar[j].text, Paylasimlar[j].dosya, Paylasimlar[j].tarih,
                                  Paylasimlar[j].makale_konu, "Dosya"))

        sayfalanmis = Paginator(Paylasimlar_W_Attr, 8)  # bir üst satırdaki şeyin aynısını daha kolay yapıyor
        sayfa = self.request.GET.get("sayfa", 1)  # eğer sayfa diye birşey tanımlı değilse, 1 yani ilk sayfayı göster
        context['Paylasimlar'] = sayfalanmis.get_page(sayfa)
        context['count'] = Makale.objects.filter(makale_yayinlanmis_mi=True).count()
        return context

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect("/giris/")
        return super(Tum_paylasimlar, self).dispatch(request,*args,**kwargs)

def paylasimci(request,user_id):
    user = User.objects.get(id=user_id)
    if request.user.is_authenticated:
        ordered_paylasimlar = Gonderi.objects.filter(yazar=user).order_by("-tarih")
        ordered_gonderis = Makale.objects.filter(makaleyi_paylasan=user).order_by("-makale_yukleme_tarihi")
        Paylasimlar = []
        for paylasim in ordered_paylasimlar:
            Paylasimlar.append(paylasim)

        Paylasimlar_W_Attr = []
        for j in range(len(Gonderi.objects.all())):
            if str(Paylasimlar[j].dosya).endswith(".png") or str(Paylasimlar[j].dosya).endswith(".JPG") or str(
                    Paylasimlar[j].dosya).endswith(".jpeg") or str(Paylasimlar[j].dosya).endswith(".jpg") or str(
                    Paylasimlar[j].dosya).endswith(".gif") or str(Paylasimlar[j].dosya).endswith(".eps") or str(
                    Paylasimlar[j].dosya).endswith(".bmp") or str(Paylasimlar[j].dosya).endswith(".raw") or str(
                    Paylasimlar[j].dosya).endswith(".psd"):
                Paylasimlar_W_Attr.append(
                    PaylasimClass(Paylasimlar[j].yazar, Paylasimlar[j].text, Paylasimlar[j].dosya, Paylasimlar[j].tarih,
                                  Paylasimlar[j].makale_konu, "Resim"))
            else:
                Paylasimlar_W_Attr.append(
                    PaylasimClass(Paylasimlar[j].yazar, Paylasimlar[j].text, Paylasimlar[j].dosya, Paylasimlar[j].tarih,
                                  Paylasimlar[j].makale_konu, "Dosya"))
        Gonderiler = []
        for gonderi in ordered_gonderis:
            Gonderiler.append(gonderi)
        Gonderiler_W_Attr = []
        for j in range(len(Makale.objects.filter(makaleyi_paylasan=user))):
            if Gonderiler[j].makale_yayinlanmis_mi:
                Gonderiler_W_Attr.append(
                    GonderiClass(Gonderiler[j].id, Gonderiler[j].makale_yazar, Gonderiler[j].makale_aciklama,
                                 Gonderiler[j].makale_pdf_dosya
                                 , Gonderiler[j].makale_yukleme_tarihi, Gonderiler[j].makale_konu,
                                 Gonderiler[j].makale_anahtar_kelimeler,
                                 Gonderiler[j].makale_yayinlanmis_mi, Gonderiler[j].makale_baslik,
                                 Gonderiler[j].makale_arkaplan_resmi))

        return render(request,"Giris_Yaptiktan_Sonra/paylasimci_sayfasi.html",{
            'user': user,
            'Tum_paylasimlar':Paylasimlar_W_Attr,
            'Tum_makaleler': Gonderiler_W_Attr
        })
    else:
        return redirect("/giris/")



class Profilim(TemplateView):
    template_name = "Giris_Yaptiktan_Sonra/Profilim.html"

    def get_context_data(self, **kwargs):
        context = super(Profilim, self).get_context_data(**kwargs)
        context["count"] = Makale.objects.filter(makale_yayinlanmis_mi=True).count()
        return context

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect("/giris/")
        return super(Profilim, self).dispatch(request,*args,**kwargs)


class Tum_paylasimcilar(TemplateView):
    template_name = "Giris_Yaptiktan_Sonra/tum_paylasimcilar.html"

    def get_context_data(self, **kwargs):
        context = super(Tum_paylasimcilar, self).get_context_data(**kwargs)
        users1 = User.objects.filter(Makale_paylasabilir_mi=True)
        users2 = User.objects.filter(Normal_paylasim_yapabilir_mi=True)
        context['count'] = Makale.objects.filter(makale_yayinlanmis_mi=True).count()
        paylasimcilar = []
        for user in users1:
            paylasimcilar.append(user)
        for user in users2:
            if not user in paylasimcilar:
                paylasimcilar.append(user)

        kullanici_adet = User.objects.all().count()

        sayfalanmis = Paginator(paylasimcilar, 10)  # bir üst satırdaki şeyin aynısını daha kolay yapıyor
        sayfa = self.request.GET.get("sayfa", 1)  # eğer sayfa diye birşey tanımlı değilse, 1 yani ilk sayfayı göster
        context['Paylasimcilar'] = sayfalanmis.get_page(sayfa)
        context["Kullanici_Adet"] = kullanici_adet
        context["Paylasimci_Adet"] = len(paylasimcilar)
        return context

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect("/giris/")
        return super(Tum_paylasimcilar, self).dispatch(request,*args,**kwargs)

class karsilama(TemplateView):
    template_name = 'karsilama2.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("MYFLOW")
        return super(karsilama, self).dispatch(request,*args,**kwargs)

    def get_context_data(self, **kwargs):
        context = super(karsilama, self).get_context_data(**kwargs)
        latest_gonderis = Makale.objects.filter(makale_yayinlanmis_mi=True).order_by("-makale_yukleme_tarihi")
        filtereds = []
        for makale in latest_gonderis:
            filtereds.append(Filters(makale))
        tags = []
        last = []
        for filter in filtereds:
            if not filter.tag in tags:
                tags.append(filter.tag)
                last.append(Filters(filter.makale))
        all = []
        for makale in latest_gonderis:
            all.append(Filters(makale))
        context["portfolioFilters"] = last[:4]
        context["Makalelerimiz"] = all[:8]
        return context




class MYFLOW(FormView):
    template_name = "Giris_Yaptiktan_Sonra/Takip_Ettigim_Akis.html"
    success_url = "/arama_sonuclari/"
    form_class = AramaMotoruForm

    def get_context_data(self, **kwargs):
        context = super(MYFLOW, self).get_context_data(**kwargs)
        ordered_gonderis = Makale.objects.all().order_by("-makale_yukleme_tarihi")
        ordered_paylasimlar = Gonderi.objects.all().order_by("-tarih")
        Paylasimlar = []
        for paylasim in ordered_paylasimlar:
            Paylasimlar.append(paylasim)

        Paylasimlar_W_Attr = []
        for j in range(len(Gonderi.objects.all())):
            if str(Paylasimlar[j].dosya).endswith(".png") or str(Paylasimlar[j].dosya).endswith(".JPG") or str(Paylasimlar[j].dosya).endswith(".jpeg") or str(Paylasimlar[j].dosya).endswith(".jpg") or str(Paylasimlar[j].dosya).endswith(".gif") or str(Paylasimlar[j].dosya).endswith(".eps") or str(Paylasimlar[j].dosya).endswith(".bmp") or str(Paylasimlar[j].dosya).endswith(".raw") or str(Paylasimlar[j].dosya).endswith(".psd"):
                Paylasimlar_W_Attr.append(PaylasimClass(Paylasimlar[j].yazar,Paylasimlar[j].text,Paylasimlar[j].dosya,Paylasimlar[j].tarih,Paylasimlar[j].makale_konu,"Resim"))
            else:
                Paylasimlar_W_Attr.append(
                    PaylasimClass(Paylasimlar[j].yazar, Paylasimlar[j].text, Paylasimlar[j].dosya, Paylasimlar[j].tarih,
                                  Paylasimlar[j].makale_konu, "Dosya"))

        Gonderiler = []
        for gonderi in ordered_gonderis:
            Gonderiler.append(gonderi)
        Gonderiler_W_Attr = []
        Takip_Edilen_Gonderiler = []
        for j in range(len(Makale.objects.all())):
            if Gonderiler[j].makale_yayinlanmis_mi:
                Gonderiler_W_Attr.append(
                    GonderiClass(Gonderiler[j].id, Gonderiler[j].makale_yazar, Gonderiler[j].makale_aciklama, Gonderiler[j].makale_pdf_dosya
                                 , Gonderiler[j].makale_yukleme_tarihi, Gonderiler[j].makale_konu,Gonderiler[j].makale_anahtar_kelimeler,
                                 Gonderiler[j].makale_yayinlanmis_mi,Gonderiler[j].makale_baslik,Gonderiler[j].makale_arkaplan_resmi))

            ders = Gonderiler[j].makale_konu
            if ders in self.request.user.user.follows.all():
                Takip_Edilen_Gonderiler.append(
                    GonderiClass(Gonderiler[j].id, Gonderiler[j].makale_yazar, Gonderiler[j].makale_aciklama,
                                 Gonderiler[j].makale_pdf_dosya
                                 , Gonderiler[j].makale_yukleme_tarihi, Gonderiler[j].makale_konu,
                                 Gonderiler[j].makale_anahtar_kelimeler,
                                 Gonderiler[j].makale_yayinlanmis_mi, Gonderiler[j].makale_baslik,
                                 Gonderiler[j].makale_arkaplan_resmi))

        print(Takip_Edilen_Gonderiler)
        sayfalanmis = Paginator(Takip_Edilen_Gonderiler,5)  # bir üst satırdaki şeyin aynısını daha kolay yapıyor
        sayfa = self.request.GET.get("sayfa", 1)  # eğer sayfa diye birşey tanımlı değilse, 1 yani ilk sayfayı göster
        context['Makalelerimiz'] = sayfalanmis.get_page(sayfa)
        context['count'] = len(Gonderiler_W_Attr)
        context["follows"] = self.request.user.user.follows.all()
        x = Duyurular.objects.all()
        duyuru_adet = x.count()
        rastGele = []
        for konu in MakaleKonu.objects.all():
            if not konu in self.request.user.user.follows.all():
                rastGele.append(konu)
        shuffle(rastGele)
        context["rastgeleKonular"] = rastGele[:3]
        context["Paylasimlar"] = Paylasimlar_W_Attr[:2]
        context["duyurucount"] = duyuru_adet
        return context

    def form_valid(self, form):
        aranan = form.cleaned_data["aratilan_kelime"]
        makaleler = Makale.objects.filter(makale_yayinlanmis_mi=True)
        print(aranan)
        mumkunler  = []
        print(makaleler.count())
        for makale in makaleler:
            if str(aranan) in str(makale.makale_konu) or str(makale.makale_aciklama) or str(makale.makale_anahtar_kelimeler) or str(makale.makale_baslik) or str(makale.yazar):
                mumkunler.append(makale)
        print(len(mumkunler))
        sonuclar = mumkunler
        return render(self.request, "Giris_Yaptiktan_Sonra/Arama_Sonuclari.html", {
            'aratilan_kelime': form.cleaned_data["aratilan_kelime"],
            'data':sonuclar,
            'form': AramaMotoruForm
        })

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect("/giris/")
        return super(MYFLOW, self).dispatch(request,*args,**kwargs)



class kayit(FormView):
    template_name = 'kayit.html'
    form_class = KayitForm
    success_url = '/giris/'
    def get_context_data(self, **kwargs):
        context = super(kayit, self).get_context_data(**kwargs)
        context['form'] = KayitForm()
        return context

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("/")
        return super(kayit, self).dispatch(request,*args,**kwargs)

    def form_valid(self, form):
        username = form.cleaned_data['username']
        if not User.objects.filter(username=username):
            user = User.objects.create(
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                email=form.cleaned_data['email'],
                username=form.cleaned_data['username'],
            )
            user.set_password('{}'.format(form.cleaned_data['password']))
            user.save()
            link = "https://gsuvoldemath.pythonanywhere.com/hesabini_aktif_et/" + str(username)
            send_mail('Hesabını aktif et'
                      ,'Merhaba '+str(form.cleaned_data["first_name"])+ " "+ str(form.cleaned_data["last_name"])+ ". Voldemath hesabını aktifleştirmek için aşağıdaki linke tıkla \n"+
                      "\n"+
                      link,'gsu.voldemath@gmail.com',[str(form.cleaned_data["email"])],fail_silently=False)
            messages.success(self.request,"Başarılı bir şekilde hesabın oluşturuldu, giriş yapabilmek için, mailine gönderilen aktivasyon linkine tıklamalısın.")
            return super(kayit, self).form_valid(form)
        else:
            errormsg = "Bu kullanıcı adıyla kayıtlı bir üyemiz mevcuttur, lütfen farklı bir kullanıcı adı tercih ediniz."
            return render(self.request, "kayit.html", {
                'error': errormsg,
                'form': form
            })


class anasayfa(FormView):
    template_name = "Giris_Yaptiktan_Sonra/Tum_Akis.html"
    success_url = "/arama_sonuclari/"
    form_class = AramaMotoruForm
    def get_context_data(self, **kwargs):
        context = super(anasayfa, self).get_context_data(**kwargs)
        ordered_gonderis = Makale.objects.all().order_by("-makale_yukleme_tarihi")
        context["portfolioFilters"] = Makale.objects.all().order_by("-makale_yukleme_tarihi")[:5]
        Gonderiler = []
        for gonderi in ordered_gonderis:
            Gonderiler.append(gonderi)
        Gonderiler_W_Attr = []
        for j in range(len(Makale.objects.all())):
            if Gonderiler[j].makale_yayinlanmis_mi:
                Gonderiler_W_Attr.append(
                    GonderiClass(Gonderiler[j].id, Gonderiler[j].makale_yazar, Gonderiler[j].makale_aciklama,
                                 Gonderiler[j].makale_pdf_dosya
                                 , Gonderiler[j].makale_yukleme_tarihi, Gonderiler[j].makale_konu, Gonderiler[j].makale_anahtar_kelimeler,
                                 Gonderiler[j].makale_yayinlanmis_mi, Gonderiler[j].makale_baslik,Gonderiler[j].makale_arkaplan_resmi))
        print(Gonderiler_W_Attr)
        sayfalanmis = Paginator(Gonderiler_W_Attr, 5)  # bir üst satırdaki şeyin aynısını daha kolay yapıyor
        sayfa = self.request.GET.get("sayfa", 1)  # eğer sayfa diye birşey tanımlı değilse, 1 yani ilk sayfayı göster
        context['Makalelerimiz'] = sayfalanmis.get_page(sayfa)
        context['count'] = len(Gonderiler_W_Attr)
        x = Duyurular.objects.all()
        duyuru_adet = x.count()
        context["duyurucount"] = duyuru_adet
        rastGele = []
        for konu in MakaleKonu.objects.all():
            if not konu in self.request.user.user.follows.all():
                rastGele.append(konu)
        shuffle(rastGele)
        context["rastgeleKonular"] = rastGele[:3]
        return context  # eğer makale çok uzunsa ve bunu 1 sayfada değil de bölerek göstermek istiyorsak

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect("/giris/")
        return super(anasayfa, self).dispatch(request,*args,**kwargs)

class giris(FormView):
    template_name = 'enter-world.html'
    form_class = GirisForm
    success_url = '/kendi_akisim/'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("/")
        return super(giris, self).dispatch(request,*args,**kwargs)

    def form_valid(self, form):
        user = authenticate(
           username = form.cleaned_data['username'],
           password = form.cleaned_data['password']
        )
        if user:
            if user.user.hesap_aktif_mi:
                login(self.request,user)
                return super(giris, self).form_valid(form)
            else:
                messages.error(self.request,"Hesabınıza giriş yapabilmek için önce mailinize gönderilen aktivasyon linkine tıklamalısınız.")
                return redirect("/giris/")
        else:
            messages.error(self.request,"Yanlış kullanıcı adı veya şifre girdiniz. Lütfen tekrar deneyiniz.")
            return redirect("/giris/")


def hesabi_aktif_et(request,username):
    user = User.objects.get(username=username)
    user.hesap_aktif_mi = True
    user.save()
    messages.success(request,"Hesabınız aktif edilmiştir, giriş yapabilirsiniz.")
    return redirect("/giris/")


class dersler(FormView):
    template_name = "konu_listesi.html"
    form_class = ProfilForm

    def get_context_data(self, **kwargs):
        context = super(dersler, self).get_context_data(**kwargs)
        context['count'] = Makale.objects.filter(makale_yayinlanmis_mi=True).count()
        dersler2 = MakaleKonu.objects.all()
        context['form'] = DerslerForm()
        context['dersler'] = dersler2
        x = Duyurular.objects.all()
        duyuru_adet = x.count()
        context["duyurucount"] = duyuru_adet
        return context

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect("/")
        return super(dersler, self).dispatch(request,*args,**kwargs)


def Takip(request,ders_id):
    ders = MakaleKonu.objects.get(id=ders_id)
    if request.user.is_authenticated:
        if ders in request.user.user.follows.all():
            request.user.user.follows.remove(ders)
        else:
            request.user.user.follows.add(ders)
        return redirect(request.META['HTTP_REFERER'])
    else:
        return redirect("/giris/")

import datetime
class Dergimiz(TemplateView):
    template_name = "Giris_Yapmadan_Once/about_gsumath.html"

    def get_context_data(self, **kwargs):
        context = super(Dergimiz, self).get_context_data(**kwargs)
        context["time"] = datetime.datetime.now()
        return context


class Nasil_Basladik(TemplateView):
    template_name = "Giris_Yapmadan_Once/nasil_basladik.html"

    def get_context_data(self, **kwargs):
        context = super(Nasil_Basladik, self).get_context_data(**kwargs)
        context["time"] = datetime.datetime.now()
        return context


class Change_Your_Password(FormView):
    template_name = "changePass.html"
    form_class = changePassForm
    success_url = "/"

    def form_valid(self, form):
        user = User.objects.get(username=self.request.user.username)
        user2 = authenticate(
            username=user.username,
            password=form.cleaned_data['eski_password']
        )
        if user2:
            if form.cleaned_data["new_password"] == form.cleaned_data["new_password_again"]:
                user.set_password(form.cleaned_data["new_password"])
                user.save()
                messages.success(self.request,"Şifreniz başarıyla değiştirildi.")
                return super(Change_Your_Password, self).form_valid(form)
            else:
                messages.error(self.request, "Eski veya yeni şifreleri hatalı girdiniz. Tekrar deneyiniz.")
                return render("sifre_degistir/")

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect("/giris/")
        return super(Change_Your_Password, self).dispatch(request,*args,**kwargs)

class yeni_paylasim(FormView):
    template_name = "yeni_paylasim.html"
    form_class = GonderiForm
    success_url = "/kendi_akisim/"

    def get_context_data(self, **kwargs):
        context = super(yeni_paylasim, self).get_context_data(**kwargs)
        context["gonderiler"] = Gonderi.objects.all().order_by("-tarih")
        context["dersler"] = Konu.objects.all().order_by("-tarih")
        return context

    def form_valid(self, form):
        if "dosya" in self.request.FILES:
            Gonderi.objects.create(
                yazar = User.objects.get(id=self.request.user.id),
                text=form.cleaned_data["text"],
                dosya=self.request.FILES["dosya"],
                makale_konu=form.cleaned_data["ders"],
            )
        else:
            Gonderi.objects.create(
                yazar= User.objects.get(id=self.request.user.id),
                text=form.cleaned_data["text"],
                makale_konu=form.cleaned_data["ders"],
            )
        return super(yeni_paylasim, self).form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.user.is_authenticated:
            return redirect("/giris/")
        return super(yeni_paylasim, self).dispatch(request,*args,**kwargs)

class makale_paylasim(FormView):
    template_name = "makale_paylasim.html"
    form_class = makaleGonderiForm
    success_url = "/kendi_akisim/"

    def get_context_data(self, **kwargs):
        context = super(makale_paylasim, self).get_context_data(**kwargs)
        context["makale_konular"] = MakaleKonu.objects.all().order_by("-tarih")
        return context

    def form_valid(self, form):
        kullanicilar = User.objects.filter(isAdmin=True)
        admin_mail_list = []
        for kullanici in kullanicilar:
            admin_mail_list.append(kullanici.email)


        user = self.request.user.user
        if "makale_pdf_dosya" in self.request.FILES:
            Makale.objects.create(
                makaleyi_paylasan=User.objects.get(id=self.request.user.id),
                makale_konu = form.cleaned_data["makale_konu"],
                makale_baslik = form.cleaned_data["makale_baslik"],
                makale_yazar = form.cleaned_data["makale_yazar"],
                makale_aciklama = form.cleaned_data["makale_aciklama"],
                makale_anahtar_kelimeler = form.cleaned_data["makale_anahtar_kelimeler"],
                makale_pdf_dosya = self.request.FILES["makale_pdf_dosya"],
                makale_arkaplan_resmi = self.request.FILES["makale_arkaplan_resmi"]
            )
            send_mail('Yeni bir makale paylaşıldı', "Merhabalar değerli Voldemath Dergisi admini,\n"+str(user.first_name)+' '+str(user.last_name)+' isimli, '+str(user.username)+' kullanıcı adlı makele paylaşımcısı tarafından bir makale paylaşıldı. Bu makaleyi admin-panelinde kontrol edip onaylayabilirsin.'
                      ,'gsu.voldemath@gmail.com',admin_mail_list,fail_silently=False)
            messages.success(self.request,"Makalen başarıyla yayınlanmak üzere adminlere gönderildi.")

        else:
            Makale.objects.create(
                makaleyi_paylasan=User.objects.get(id=self.request.user.id),
                makale_konu=form.cleaned_data["makale_konu"],
                makale_baslik=form.cleaned_data["makale_baslik"],
                makale_yazar=form.cleaned_data["makale_yazar"],
                makale_aciklama=form.cleaned_data["makale_aciklama"],
                makale_anahtar_kelimeler=form.cleaned_data["makale_anahtar_kelimeler"],
                makale_arkaplan_resmi=self.request.FILES["makale_arkaplan_resmi"]
            )
            send_mail('Yeni bir makale paylaşıldı', str(user.first_name) + ' ' + str(user.last_name) + 'adlı, ' + str(
                user.username) + ' kullanıcı adlı makele paylaşımcısı tarafından bir makale paylaşıldı. Bu makaleyi admin-panelinde kontrol edip onaylayabilirsin.'
                      , 'gsu.voldemath@gmail.com', admin_mail_list, fail_silently=False)
        return super(makale_paylasim, self).form_valid(form)

    def form_invalid(self, form):
        return super(makale_paylasim, self).form_invalid(form)

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect("/giris/")
        return super(makale_paylasim, self).dispatch(request,*args,**kwargs)


def gonderi_sil(request,gonderi_id):
    silinecek_oge = Makale.objects.filter(id=gonderi_id)
    silinecek_oge.delete()
    return redirect(request.META['HTTP_REFERER'])


class cikis(RedirectView):
    permanent = False
    pattern_name = "karsilama"
    def get_redirect_url(self, *args, **kwargs):
        logout(self.request)
        return super(cikis, self).get_redirect_url(*args,**kwargs)


class yeniKonu(FormView):
    form_class = yeniKonuForm
    template_name = "konu_olustur.html"
    success_url = "/yeni_paylasim/"

    def form_valid(self, form):
        from random import randrange
        randns = []
        for i in range(3):
            randns.append(randrange(0,10))
        randstr = (str(form.cleaned_data["konuname"])[:3]).upper()

        Konu.objects.create(
            name=form.cleaned_data["konuname"],
            konukodu = randstr+str(randns[0])+str(randns[1])+str(randns[2]),
            ders_text= "Konu hk. bilgi..."
        )
        return super(yeniKonu, self).form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect("/giris/")
        return super(yeniKonu, self).dispatch(request,*args,**kwargs)

class yeniMakaleKonu(FormView):
    form_class = yeniMakaleKonuForm
    template_name = "makale_konu_olustur.html"
    success_url = "/makale_paylasim/"

    def form_valid(self, form):
        MakaleKonu.objects.create(
            konu_adi=form.cleaned_data["konuname"],
        )
        return super(yeniMakaleKonu, self).form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.user.is_authenticated:
            return redirect("/giris/")
        return super(yeniMakaleKonu, self).dispatch(request,*args,**kwargs)


def yeniPaylasimci(request, user_id):
    istek_yollayan_kullanici = User.objects.get(id=user_id)
    adminlerin_email_adresleri = []
    kullanicilar = User.objects.all()
    for kullanici in kullanicilar:
        if kullanici.isAdmin:
            adminlerin_email_adresleri.append(str(kullanici.email))
    link = 'https://gsuvoldemath.pythonanywhere.com/kullaniciya_izin_ver/14504169u'+str(user_id)
    profil_link = 'https://gsuvoldemath.pythonanywhere.com/profil/'+str(user_id)
    print(adminlerin_email_adresleri)
    print(link)
    print(profil_link)
    if request.user.is_authenticated:
        if not istek_yollayan_kullanici.daha_once_paylasimci_istegi_yapti_mi:
            send_mail("Voldemath'da yeni bir paylaşımcı isteği var","Merhaba "+ str(istek_yollayan_kullanici.first_name) + ' ' + str(
                istek_yollayan_kullanici.last_name)+ ' adlı kullanıcı senden paylaşım yapabilmek için izin istiyor.'
                                                     'Eğer kullanıcının paylaşım yapabilmesini istiyorsan aşağıdaki linke tıklayabilirsin. \n'
                                                     'İzin vermek için link: '+str(link),str(istek_yollayan_kullanici.email),adminlerin_email_adresleri,fail_silently=False)
            istek = User.objects.get(id=user_id)
            istek.daha_once_paylasimci_istegi_yapti_mi = True
            istek.save()
            print(istek_yollayan_kullanici.daha_once_paylasimci_istegi_yapti_mi)
            messages.success(request, "Paylaşım gönderebilmen için gerekli izin adminlerimizden istendi. Kabul edildiği takdirde size bir e-mail gönderilecektir. Sabrınız ve ilginiz için teşekkür ederiz.")
            return redirect("/yeni_paylasim/")
        else:
            messages.error(request, "İsteğin bize daha önce ulaştı. En kısa sürede adminlerimiz kontrol edip onaylayacaklardır. Sabrınız ve ilginiz için teşekkür ederiz.")
            return redirect("/yeni_paylasim/")
    else:
        return redirect("/giris/")

def yeniMakaleci(request,user_id):
    istek_yollayan_kullanici = User.objects.get(id=user_id)
    adminlerin_email_adresleri = []
    kullanicilar = User.objects.all()
    for kullanici in kullanicilar:
        if kullanici.isAdmin:
            adminlerin_email_adresleri.append(str(kullanici.email))
    link = 'https://gsuvoldemath.pythonanywhere.com/kullaniciya_makale_izni_ver/14504169u' + str(user_id)
    profil_link = 'https://gsuvoldemath.pythonanywhere.com/profil/' + str(user_id)
    print(adminlerin_email_adresleri)
    print(link)
    print(profil_link)
    if request.user.is_authenticated:
        if not istek_yollayan_kullanici.daha_once_makaleci_istegi_yapti_mi:
            send_mail("Voldemath'da yeni bir makaleci isteği var",
                      "Merhaba " + str(istek_yollayan_kullanici.first_name) + ' ' + str(
                          istek_yollayan_kullanici.last_name) + ' adlı kullanıcı senden yeni makaleler paylaşabilmek için izin istiyor.'
                                                                'Eğer kullanıcının paylaşım yapabilmesini istiyorsan aşağıdaki linke tıklayabilirsin. \n'
                                                                'İzin vermek için link: ' + str(
                          link), str(istek_yollayan_kullanici.email),
                      adminlerin_email_adresleri, fail_silently=False)
            istek = User.objects.get(id=user_id)
            istek.daha_once_makaleci_istegi_yapti_mi = True
            istek.save()
            print(istek_yollayan_kullanici.daha_once_paylasimci_istegi_yapti_mi)
            messages.success(request,
                             "Makale paylaşımı yapabilmen için gerekli izin adminlerimizden istendi. Kabul edildiği takdirde size bir e-mail gönderilecektir. Sabrınız ve ilginiz için teşekkür ederiz.")
            return redirect("/makale_paylasim/")
        else:
            messages.error(request,
                           "İsteğin bize daha önce ulaştı. En kısa sürede adminlerimiz kontrol edip onaylayacaklardır. Sabrınız ve ilginiz için teşekkür ederiz.")
            return redirect("/makale_paylasim/")
    else:
        return redirect("/giris/")

def kullaniciya_izin_ver(request,user_id):
    kullanici = User.objects.get(id=user_id)
    if request.user.is_authenticated:
        if request.user.user.isAdmin:
            kullanici.Normal_paylasim_yapabilir_mi = True
            kullanici.save()
            send_mail('Makale paylaşımı izni verildi!',
                      'Tebrikler, artık Voldemath dergisinde normal paylaşımlarda bulunabilirsin.',
                      str(request.user.user.email), [str(kullanici.email)], fail_silently=False)
            messages.success(request,'Başarılı bir şekilde '+ str(kullanici.first_name)+' '+str(kullanici.last_name)+' kullanıcısına paylaşım onayı verilmiştir.')
            return redirect("/")
        else:
            messages.error(request,'Bu yetkiye sahip değilsiniz, ancak adminler kullanıcılara yetki verebilir.')
            return redirect("/")
    else:
        return redirect("/giris/")


def kullaniciya_makale_izni_ver(request,user_id):
    kullanici = User.objects.get(id=user_id)
    if request.user.is_authenticated:
        if request.user.user.isAdmin:
            kullanici.Makale_paylasabilir_mi = True
            kullanici.save()
            send_mail('Makale paylaşımı izni verildi!','Tebrikler, artık Voldemath dergisinde makale paylaşımında bulunabilirsin.',str(request.user.user.email),[str(kullanici.email)],fail_silently=False)
            messages.success(request, 'Başarılı bir şekilde ' + str(kullanici.first_name) + ' ' + str(
                kullanici.last_name) + ' kullanıcısına makale paylaşım onayı verilmiştir.')
            return redirect("/")
        else:
            messages.error(request, 'Bu yetkiye sahip değilsiniz, ancak adminler kullanıcılara yetki verebilir. Admin hesabınızla giriş yapınız.')
            return redirect("/")
    else:
        return redirect("/giris/")


class duyurular(TemplateView):
    template_name = "Giris_Yaptiktan_Sonra/Duyurular.html"

    def get_context_data(self, **kwargs):
        context = super(duyurular, self).get_context_data(**kwargs)
        duyurularr = []
        context['count'] = Makale.objects.filter(makale_yayinlanmis_mi=True).count()
        Duyurus = Duyurular.objects.all()
        for duyuru in Duyurus:
            duyurularr.append(duyuru)
        sayfalanmis = Paginator(duyurularr, 2)  # bir üst satırdaki şeyin aynısını daha kolay yapıyor
        sayfa = self.request.GET.get("sayfa", 1)  # eğer sayfa diye birşey tanımlı değilse, 1 yani ilk sayfayı göster
        context['duyurular'] = sayfalanmis.get_page(sayfa)
        return context

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect("/giris/")
        return super(duyurular, self).dispatch(request,*args,**kwargs)

