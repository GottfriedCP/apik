from openpyxl import Workbook
from django.http import HttpResponse

import datetime


def export_to_excel(modeladmin, request, queryset):
    wb = Workbook()
    ws = wb.active
    # nama2 field di baris pertama
    ws.append([field.name for field in modeladmin.model._meta.fields])
    for row in queryset:
        try:
            ws.append(
                [getattr(row, field.name) for field in modeladmin.model._meta.fields]
            )
        except:
            ws.append(
                [
                    str(getattr(row, field.name))
                    for field in modeladmin.model._meta.fields
                ]
            )
        # ws.append([field.name for field in modeladmin.model._meta.fields])
    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response[
        "Content-Disposition"
    ] = f"attachment; filename={modeladmin.model.__name__}_{str(datetime.datetime.now())}.xlsx"
    wb.save(response)
    return response


export_to_excel.short_description = "Unduh format excel"
