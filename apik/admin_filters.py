from django.contrib import admin
from django.utils import timezone

from dateutil.relativedelta import relativedelta


class AgeFilter(admin.SimpleListFilter):
    title = "usia"  # Filter title
    parameter_name = "usia"  # URL parameter name

    def lookups(self, request, model_admin):
        return (("lte5", "Di bawah 5 tahun"),)

    def queryset(self, request, queryset):
        if self.value() == "lte5":
            date_59_months_ago = timezone.now().date() - relativedelta(months=59)
            return queryset.filter(tanggal_lahir__gte=date_59_months_ago)
