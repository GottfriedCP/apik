from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import timezone

from dateutil.relativedelta import relativedelta

from ...models import Bayi, Imunisasi


class Command(BaseCommand):
    help = "Hitung total dosis imunisasi yang bisa diberikan."

    def handle(self, *args, **options):
        print("OK")
        eligible_imuns_count_file = settings.BASE_DIR / "eligible_imuns_count.txt"
        # exclude anak di atas 5 tahun
        date_59_months_ago = timezone.now().date() - relativedelta(months=59)
        balitas = Bayi.objects.filter(tanggal_lahir__gte=date_59_months_ago)

        eligible_imuns_count = 0

        for balita in balitas:
            # imunisasi yg bisa diberikan ke anak ini
            eligible_imuns = Imunisasi.objects.filter(
                syarat_usia__lte=balita.get_usia_bulan()
            )
            #{% if imun_e.maksimum_usia and balita.get_usia_bulan >= imun_e.maksimum_usia %}
            eligible_imuns = eligible_imuns.exclude(bayis__in=(balita,))
            for eligible_imun in eligible_imuns:
                if eligible_imun.maksimum_usia:
                    if balita.get_usia_bulan() < eligible_imun.maksimum_usia:
                        eligible_imuns_count += 1
                else:
                    eligible_imuns_count += 1

        try:
            with open(eligible_imuns_count_file, "w") as txtfile:
                txtfile.write(f"{eligible_imuns_count}")
        except:
            pass
