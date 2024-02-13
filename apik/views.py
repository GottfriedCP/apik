from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from dateutil.relativedelta import relativedelta

from .helpers import get_random_bidan_wa_number, get_eligible_imuns_count
from .models import Bayi, Bidan, Ibu, Imunisasi, ImunisasiDiberikan

import datetime


@login_required
def index(request):
    ibu = False
    bidan = False
    try:
        nik_session = request.session["apik_nik"]
    except KeyError:
        return HttpResponseForbidden("Mohon logout dahulu via situs Administrasi APIK.")
    balitas = Bayi.objects.select_related("ibu").prefetch_related("bidans")
    if request.user.groups.filter(name="ibu").exists():
        # user adalah ibu
        ibu = Ibu.objects.get(nik=nik_session)
        balitas = balitas.filter(ibu=ibu)
    else:
        # user adalah bidan
        bidan = Bidan.objects.get(nik=nik_session)
        balitas = balitas.all()
        # exclude anak di atas 5 tahun
        date_59_months_ago = timezone.now().date() - relativedelta(months=59)
        balitas = balitas.filter(tanggal_lahir__gte=date_59_months_ago)

    jumlah_balita = balitas.count()

    eligible_imuns_count_list = []
    imunisasis = Imunisasi.objects.prefetch_related("bayis")
    for balita in balitas:
        #imunisasis = Imunisasi.objects.prefetch_related("bayis")
        # list imunisasi yang belum diberikan
        eligible_imuns = imunisasis.exclude(bayis__in=(balita,))
        # list imunisasi yang memenuhi syarat usia dari query above
        eligible_imuns = eligible_imuns.filter(syarat_usia__lte=balita.get_usia_bulan())
        eligible_imuns_count_list.append(eligible_imuns.count())
    balitas = zip(balitas, eligible_imuns_count_list)

    return render(
        request,
        "apik/index.html",
        {
            "ibu": ibu,
            "bidan": bidan,
            "balitas": balitas,
            "random_wa_number": get_random_bidan_wa_number(),
            # get jml total dosis imunisasi yg bisa diberikan
            "eligible_imuns_count": get_eligible_imuns_count(),
            "jumlah_balita": jumlah_balita,
        },
    )


def login_view(request):
    if request.user.is_authenticated:
        return redirect("apik:index")

    err_msg = False
    PASSWORD_IBU = "123"
    PASSWORD_BIDAN = "payung"
    if request.method == "POST":
        peran = request.POST.get("peran", False)
        if peran in ("bidan", "ibu"):
            nik = request.POST.get("nik")
            password = request.POST.get("password")
            # LOGIN BIDAN
            if peran == "bidan" and password == PASSWORD_BIDAN:
                bidan = Bidan.objects.filter(nik=nik).exists()
                if bidan:
                    user = authenticate(request, username="bidan", password="bidan")
                    if user is not None:
                        login(request, user)
                        request.session["apik_nik"] = nik
                        return redirect("apik:index")
            # LOGIN IBU
            if peran == "ibu" and password == PASSWORD_IBU:
                ibu = Ibu.objects.filter(nik=nik).exists()
                if ibu:
                    user = authenticate(request, username="ibu", password="ibu")
                    if user is not None:
                        login(request, user)
                        request.session["apik_nik"] = nik
                        return redirect("apik:index")
        # user tidak ditemukan
        err_msg = "NIK, password, atau peran keliru"

    return render(
        request,
        "apik/login.html",
        {
            "hide_navbar": True,
            "err_msg": err_msg,
        },
    )


@login_required
def logout_view(request):
    if request.method == "POST":
        # destroy app vars in session

        session_keys_list = []
        for k in request.session.keys():
            if str(k).startswith("apik_"):
                session_keys_list.append(k)
        for k in session_keys_list:
            del request.session[k]
        logout(request)

    return redirect("/")


@login_required
def bayi_detail(request, bayi_id):
    balita = get_object_or_404(Bayi, pk=bayi_id)

    # imunisasi yg bisa diberikan ke anak ini
    eligible_imuns = Imunisasi.objects.filter(syarat_usia__lte=balita.get_usia_bulan())
    eligible_imuns = eligible_imuns.exclude(bayis__in=(balita,))

    user_is_bidan = request.user.groups.filter(name="bidan").exists()
    return render(
        request,
        "apik/detail-bayi.html",
        {
            "balita": balita,
            "eligible_imuns": eligible_imuns,
            "user_is_bidan": user_is_bidan,
            "ibu": not user_is_bidan,
            "random_wa_number": get_random_bidan_wa_number(balita),
        },
    )


@login_required
def tambah_imunisasi(request):
    """Mencatat imunisasi baru untuk bayi. POST"""
    if request.method == "POST":
        bayi_id = int(request.POST["bayi_id"])
        imun_id = int(request.POST["imun_id"])
        tanggal_input = request.POST["tanggal"]
        tanggal = datetime.datetime.strptime(tanggal_input, "%d-%m-%Y")
        nik_bidan = request.session["apik_nik"]

        bayi = Bayi.objects.get(pk=bayi_id)
        imunisasi = Imunisasi.objects.get(pk=imun_id)
        through_defaults = {
            "tanggal_pemberian": tanggal,
            "jam_pencatatan": datetime.datetime.now(),  # tidak perlu TZ aware
            "bidan": Bidan.objects.get(nik=nik_bidan),
        }
        imunisasi.bayis.add(bayi, through_defaults=through_defaults)

        return redirect("apik:bayi_detail", bayi_id)


@login_required
def konfirmasi_hapus_imun_d(request):
    """Konfirmasi ke pengguna sebelum hapus data imun diberikan. POST"""
    if request.method == "POST":
        imun_d_id = request.POST.get("imun_d_id", "unknown")
        imun_d = get_object_or_404(ImunisasiDiberikan, pk=imun_d_id)

        return render(
            request,
            "apik/konfirmasi-hapus-imun.html",
            {
                "imun_d": imun_d,
            },
        )


@login_required
def hapus_imun_d(request):
    """Hapus data imunisasi yg diberikan ke seorang bayi. POST"""
    if request.method == "POST":
        imun_d_id = request.POST.get("imun_d_id", "unknown")
        imun_d = get_object_or_404(ImunisasiDiberikan, pk=imun_d_id)
        bayi = imun_d.bayi
        imun_d.delete()

        return redirect("apik:bayi_detail", bayi_id=bayi.pk)
