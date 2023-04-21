from django.urls import path

from . import views

app_name = 'apik'

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('detail-bayi/<int:bayi_id>/', views.bayi_detail, name='bayi_detail'),
    path('tambah-imunisasi/', views.tambah_imunisasi, name='tambah_imunisasi'),
]
