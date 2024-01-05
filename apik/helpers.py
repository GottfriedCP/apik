from django.utils import timezone

from dateutil.relativedelta import relativedelta

from .models import Bayi, Bidan, Imunisasi

from random import choice


def get_random_bidan_wa_number():
    pks = Bidan.objects.values_list("pk", flat=True)
    random_pk = choice(pks)
    nomor = Bidan.objects.get(pk=random_pk).get_whatsapp_number()
    print(nomor)
    if not nomor:
        return "6285275379343"
    else:
        return nomor


def get_eligible_imuns_count():
    """Hitung total dosis imunisasi yang bisa diberikan."""
    # exclude anak di atas 5 tahun
    date_59_months_ago = timezone.now().date() - relativedelta(months=59)
    balitas = Bayi.objects.filter(tanggal_lahir__gte=date_59_months_ago)

    eligible_imuns_count = 0

    for balita in balitas:
        # imunisasi yg bisa diberikan ke anak ini
        eligible_imuns = Imunisasi.objects.filter(
            syarat_usia__lte=balita.get_usia_bulan()
        )
        eligible_imuns = eligible_imuns.exclude(bayis__in=(balita,))
        eligible_imuns_count += eligible_imuns.count()

    return eligible_imuns_count
