# Generated by Django 2.2.7 on 2019-11-24 11:16

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='Announcements',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('baslik', models.CharField(max_length=100)),
                ('text', models.CharField(max_length=1000)),
                ('gonderen_email', models.CharField(max_length=50)),
                ('gonderi_tarih', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Duyurular',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('baslik', models.CharField(max_length=100)),
                ('text', models.CharField(max_length=1000)),
                ('duyuru_tarih', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Egitmen',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unvan_ve_isim', models.CharField(max_length=100)),
                ('isim', models.CharField(max_length=50)),
                ('soyisim', models.CharField(max_length=50)),
                ('unvan', models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                'verbose_name_plural': 'Eğitmenler',
            },
        ),
        migrations.CreateModel(
            name='Konu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('konukodu', models.CharField(max_length=20)),
                ('tarih', models.DateTimeField(auto_now_add=True)),
                ('ders_text', models.TextField(default='Konu hk. bilgi:...')),
            ],
            options={
                'verbose_name_plural': 'Konular',
            },
        ),
        migrations.CreateModel(
            name='MakaleKonu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('konu_adi', models.CharField(max_length=150)),
                ('tarih', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'Makale Konularımız',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('okul_no', models.IntegerField(blank=True, null=True, unique=True)),
                ('isAdmin', models.BooleanField(blank=True, default=False, null=True)),
                ('isOfficer', models.BooleanField(blank=True, default=False, null=True)),
                ('Makale_paylasabilir_mi', models.BooleanField(blank=True, default=False, null=True)),
                ('Normal_paylasim_yapabilir_mi', models.BooleanField(blank=True, default=False, null=True)),
                ('follows', models.ManyToManyField(related_name='followed_by', to='Voldemath.MakaleKonu')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Makale',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('makale_baslik', models.CharField(max_length=100)),
                ('makale_yazar', models.CharField(max_length=150)),
                ('makale_aciklama', models.CharField(max_length=1500)),
                ('makale_anahtar_kelimeler', models.TextField(max_length=350)),
                ('makale_yukleme_tarihi', models.DateTimeField(auto_now_add=True)),
                ('makale_yayinlanmis_mi', models.BooleanField(default=False)),
                ('makale_pdf_dosya', models.FileField(blank=True, null=True, upload_to='makale_pdfs')),
                ('makale_arkaplan_resmi', models.FileField(blank=True, null=True, upload_to='makale_bgs')),
                ('makale_konu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Voldemath.MakaleKonu')),
            ],
            options={
                'verbose_name_plural': 'Makalelerimiz',
            },
        ),
        migrations.CreateModel(
            name='Gonderi',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('dosya', models.FileField(blank=True, null=True, upload_to='files')),
                ('tarih', models.DateTimeField(auto_now_add=True)),
                ('makale_konu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Voldemath.Konu')),
                ('yazar', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Voldemath.User')),
            ],
        ),
    ]
