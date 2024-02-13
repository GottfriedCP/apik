from django.conf import settings
from django.utils import timezone

from dateutil.relativedelta import relativedelta

from .models import Bayi, Bidan, Imunisasi

from random import choice


def get_random_bidan_wa_number(balita: Bayi = None):
    nomor = ""
    if balita.bidans.count() > 0:
        nomor = balita.bidans.first().get_whatsapp_number()
    else:
        pks = Bidan.objects.values_list("pk", flat=True)
        random_pk = choice(pks)
        nomor = Bidan.objects.get(pk=random_pk).get_whatsapp_number()

    if not nomor:
        return "6285275379343"
    else:
        return nomor


def get_eligible_imuns_count():
    """baca total dosis imunisasi yang bisa diberikan dari file."""
    eligible_imuns_count_file = settings.BASE_DIR / "eligible_imuns_count.txt"
    try:
        with open(eligible_imuns_count_file, "r") as txtfile:
            return txtfile.read()
    except:
        return 0
