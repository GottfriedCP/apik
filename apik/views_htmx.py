from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render
from django.utils import timezone

from dateutil.relativedelta import relativedelta

from .models import Bayi, Bidan, Ibu, Imunisasi, ImunisasiDiberikan


@login_required
def get_index_table(request):
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
        balitas = balitas.all()
        # exclude anak di atas 5 tahun
        date_59_months_ago = timezone.now().date() - relativedelta(months=59)
        balitas = balitas.filter(tanggal_lahir__gte=date_59_months_ago)

    eligible_imuns_count_list = []
    imunisasis = Imunisasi.objects.prefetch_related("bayis")
    for balita in balitas:
        # imunisasis = Imunisasi.objects.prefetch_related("bayis")
        # list imunisasi yang belum diberikan
        eligible_imuns = imunisasis.exclude(bayis__in=(balita,))
        # list imunisasi yang memenuhi syarat usia dari query above
        eligible_imuns = eligible_imuns.filter(syarat_usia__lt=balita.get_usia_bulan())
        eligible_imuns = eligible_imuns.exclude(
            maksimum_usia__lte=balita.get_usia_bulan()
        )
        eligible_imuns_count_list.append(eligible_imuns.count())
    balitas = zip(balitas, eligible_imuns_count_list)

    return render(
        request,
        "apik/htmx/index_table.html",
        {
            "balitas": balitas,
        },
    )


@login_required
def get_eligible_imuns_count(request):
    # exclude anak di atas 5 tahun
    date_59_months_ago = timezone.now().date() - relativedelta(months=59)
    balitas = Bayi.objects.filter(tanggal_lahir__gte=date_59_months_ago)

    imunisasis = Imunisasi.objects.prefetch_related("bayis")

    eligible_imuns_count = 0

    for balita in balitas:
        # 1. imunisasi yg bisa diberikan ke anak ini
        eligible_imuns = imunisasis.filter(syarat_usia__lt=balita.get_usia_bulan())
        # 2. exclude imunisasi yg sudah diberikan ke anak ini
        # {% if imun_e.maksimum_usia and balita.get_usia_bulan >= imun_e.maksimum_usia %}
        eligible_imuns = eligible_imuns.exclude(bayis__in=(balita,))
        eligible_imuns = eligible_imuns.exclude(
            maksimum_usia__lte=balita.get_usia_bulan()
        )
        for eligible_imun in eligible_imuns:
            if eligible_imun.maksimum_usia:
                if balita.get_usia_bulan() < eligible_imun.maksimum_usia:
                    eligible_imuns_count += 1
            else:
                eligible_imuns_count += 1

    return render(
        request,
        "apik/htmx/eligible_imuns_count.html",
        {"eligible_imuns_count": eligible_imuns_count},
    )
