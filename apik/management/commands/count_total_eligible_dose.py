from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import timezone

from dateutil.relativedelta import relativedelta

from ...models import Bayi, Imunisasi


class Command(BaseCommand):
    help = "Hitung total dosis imunisasi yang bisa diberikan."

    def handle(self, *args, **options):
        print("Hitung total dosis imunisasi yang bisa diberikan...")
        eligible_imuns_count_file = settings.BASE_DIR / "eligible_imuns_count.txt"
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
            for eligible_imun in eligible_imuns:
                if eligible_imun.maksimum_usia:
                    if balita.get_usia_bulan() < eligible_imun.maksimum_usia:
                        eligible_imuns_count += 1
                else:
                    eligible_imuns_count += 1
            print(f"selesai 1 balita: eligible {eligible_imuns_count} imunisasi")
        print(f"Total {eligible_imuns_count} dosis imunisasi bisa diberikan")

        try:
            with open(eligible_imuns_count_file, "w") as txtfile:
                txtfile.write(f"{eligible_imuns_count}")
        except:
            pass
