from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .models import Bayi, Bidan, Ibu, Imunisasi

import datetime


@login_required
def index(request):
    ibu = False
    bidan = False
    balitas = Bayi.objects.select_related('ibu').prefetch_related('bidans')
    if request.user.groups.filter(name='ibu').exists():
        ibu = Ibu.objects.get(nik=request.session['apik_nik'])
        balitas = balitas.filter(ibu=ibu)
    else:
        # berarti bidan.
        bidan = Bidan.objects.get(nik=request.session['apik_nik'])
        balitas = balitas.all()

    eligible_imuns_count_list = []
    for balita in balitas:
        imunisasis = Imunisasi.objects.prefetch_related('bayis')
        # list imunisasi yang belum diberikan
        eligible_imuns = imunisasis.exclude(
            bayis__in=(balita, ))
        # list imunisasi yang memenuhi syarat usia dari query above
        eligible_imuns = eligible_imuns.filter(
            syarat_usia__lte=balita.get_usia_bulan())
        eligible_imuns_count_list.append(eligible_imuns.count())
    balitas = zip(balitas, eligible_imuns_count_list)

    return render(request, 'apik/index.html', {
        'ibu': ibu,
        'bidan': bidan,
        'balitas': balitas,
    })


def login_view(request):
    if request.user.is_authenticated:
        return redirect('apik:index')

    err_msg = False
    PASSWORD_IBU = 'nkrikeren'
    PASSWORD_BIDAN = 'nkrikeren2023'
    if request.method == 'POST':
        peran = request.POST.get('peran', False)
        if peran in ('bidan', 'ibu'):
            nik = request.POST.get('nik')
            password = request.POST.get('password')
            # LOGIN BIDAN
            if peran == 'bidan' and password == PASSWORD_BIDAN:
                bidan = Bidan.objects.filter(nik=nik).exists()
                if bidan:
                    user = authenticate(
                        request, username='bidan', password='bidan')
                    if user is not None:
                        login(request, user)
                        request.session['apik_nik'] = nik
                        return redirect('apik:index')
            # LOGIN IBU
            if peran == 'ibu' and password == PASSWORD_IBU:
                ibu = Ibu.objects.filter(nik=nik).exists()
                if ibu:
                    user = authenticate(
                        request, username='ibu', password='ibu')
                    if user is not None:
                        login(request, user)
                        request.session['apik_nik'] = nik
                        return redirect('apik:index')
        # user tidak ditemukan
        err_msg = 'NIK, password, atau peran keliru'

    return render(request, 'apik/login.html', {
        'hide_navbar': True,
        'err_msg': err_msg,
    })


@login_required
def logout_view(request):
    if request.method == 'POST':
        # destroy app vars in session

        session_keys_list = []
        for k in request.session.keys():
            if str(k).startswith('apik_'):
                session_keys_list.append(k)
        for k in session_keys_list:
            del request.session[k]
        logout(request)

    return redirect("/")


@login_required
def bayi_detail(request, bayi_id):
    balita = get_object_or_404(Bayi, pk=bayi_id)

    # imunisasi yg bisa diberikan ke anak ini
    eligible_imuns = Imunisasi.objects.filter(
        syarat_usia__lte=balita.get_usia_bulan())
    eligible_imuns = eligible_imuns.exclude(bayis__in=(balita, ))

    return render(request, 'apik/detail-bayi.html', {
        'balita': balita,
        'eligible_imuns': eligible_imuns,
        'user_is_bidan': request.user.groups.filter(name='bidan').exists(),
    })


@login_required
def tambah_imunisasi(request):
    """Mencatat imunisasi baru untuk bayi. POST"""
    if request.method == 'POST':
        bayi_id = int(request.POST['bayi_id'])
        imun_id = int(request.POST['imun_id'])
        tanggal_input = request.POST['tanggal']
        tanggal = datetime.datetime.strptime(tanggal_input, "%d-%m-%Y")

        bayi = Bayi.objects.get(pk=bayi_id)
        imunisasi = Imunisasi.objects.get(pk=imun_id)
        # imun_d = ImunisasiDiberikan.objects.create(imunisasi=imunisasi, tanggal_pemberian=tanggal)
        imunisasi.bayis.add(bayi, through_defaults={
                            'tanggal_pemberian': tanggal})

        return redirect('apik:bayi_detail', bayi_id)
