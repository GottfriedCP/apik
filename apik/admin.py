from django.contrib import admin

from .filter import AgeFilter
from .models import Ibu, Bidan, Bayi, Imunisasi, ImunisasiDiberikan, Penyakit


@admin.register(Ibu)
class IbuAdmin(admin.ModelAdmin):
    list_display = ('nik', 'nama', 'alamat')


@admin.register(Bidan)
class BidanAdmin(admin.ModelAdmin):
    list_display = ('nik', 'nama', 'str')


@admin.register(Bayi)
class BayiAdmin(admin.ModelAdmin):
    list_display = ('nik', 'nama', 'tanggal_lahir', 'ibu', 'alamat')
    list_filter = (AgeFilter, )


@admin.register(Imunisasi)
class ImunisasiAdmin(admin.ModelAdmin):
    list_display = ('nama_imunisasi', 'syarat_usia', 'manfaat')


@admin.register(ImunisasiDiberikan)
class ImunisasiDiberikanAdmin(admin.ModelAdmin):
    list_display = ('bayi', 'imunisasi', 'tanggal_pemberian', 'jam_pencatatan', 'bidan')


@admin.register(Penyakit)
class PenyakitAdmin(admin.ModelAdmin):
    list_display = ('nama_penyakit', 'deskripsi')
