from django.urls import include, path

from . import views, views_htmx

app_name = "apik"

htmx_urlpatterns = [
    path("get-index-table/", views_htmx.get_index_table, name="get_index_table"),
    path(
        "get-eligible-imuns-count/",
        views_htmx.get_eligible_imuns_count,
        name="get_eligible_imuns_count",
    ),
]

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("detail-bayi/<int:bayi_id>/", views.bayi_detail, name="bayi_detail"),
    path("tambah-imunisasi/", views.tambah_imunisasi, name="tambah_imunisasi"),
    path(
        "konfirmasi-hapus/",
        views.konfirmasi_hapus_imun_d,
        name="konfirmasi_hapus_imun_d",
    ),
    path("hapus/", views.hapus_imun_d, name="hapus_imun_d"),
    path("htmx/", include(htmx_urlpatterns)),
]
