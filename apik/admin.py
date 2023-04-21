from django.contrib import admin

from .models import Ibu, Bidan, Bayi, Imunisasi, ImunisasiDiberikan, Penyakit


@admin.register(Ibu)
class IbuAdmin(admin.ModelAdmin):
    list_display = ('nik', 'nama')


@admin.register(Bidan)
class BidanAdmin(admin.ModelAdmin):
    list_display = ('nik', 'nama', 'str')


@admin.register(Bayi)
class BayiAdmin(admin.ModelAdmin):
    list_display = ('nik', 'nama', 'tanggal_lahir', 'ibu')


@admin.register(Imunisasi)
class ImunisasiAdmin(admin.ModelAdmin):
    list_display = ('nama_imunisasi', 'syarat_usia')


@admin.register(ImunisasiDiberikan)
class ImunisasiDiberikanAdmin(admin.ModelAdmin):
    list_display = ('bayi', 'imunisasi', 'tanggal_pemberian')


@admin.register(Penyakit)
class PenyakitAdmin(admin.ModelAdmin):
    list_display = ('nama_penyakit', 'deskripsi')
