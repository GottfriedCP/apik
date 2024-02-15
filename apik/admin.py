from django.contrib import admin

from .admin_actions import export_to_excel
from .admin_filters import AgeFilter
from .models import Ibu, Bidan, Bayi, Imunisasi, ImunisasiDiberikan, Penyakit


@admin.register(Ibu)
class IbuAdmin(admin.ModelAdmin):
    list_display = ("nik", "nama", "alamat")
    search_fields = ["nik", "nama"]


@admin.register(Bidan)
class BidanAdmin(admin.ModelAdmin):
    list_display = ("nik", "nama", "str")
    search_fields = ["nik", "nama"]


@admin.register(Bayi)
class BayiAdmin(admin.ModelAdmin):
    list_display = ("nik", "nama", "tanggal_lahir", "ibu", "alamat")
    search_fields = ["nik", "nama"]
    list_filter = (AgeFilter,)
    actions = [
        export_to_excel,
    ]


@admin.register(Imunisasi)
class ImunisasiAdmin(admin.ModelAdmin):
    list_display = ("nama_imunisasi", "syarat_usia", "manfaat")


@admin.register(ImunisasiDiberikan)
class ImunisasiDiberikanAdmin(admin.ModelAdmin):
    list_display = ("bayi", "imunisasi", "tanggal_pemberian", "jam_pencatatan", "bidan")
    search_fields = ["bayi", "imunisasi"]
    actions = [
        export_to_excel,
    ]


@admin.register(Penyakit)
class PenyakitAdmin(admin.ModelAdmin):
    list_display = ("nama_penyakit", "deskripsi")
