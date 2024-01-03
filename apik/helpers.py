from .models import Bidan

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
