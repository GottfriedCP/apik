# Generated by Django 4.2.8 on 2024-01-03 02:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apik', '0006_imunisasi_maksimum_usia'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='imunisasidiberikan',
            options={'ordering': ('-tanggal_pemberian', 'jam_pencatatan'), 'verbose_name': 'imunisasi-balita', 'verbose_name_plural': 'imunisasi-balita'},
        ),
        migrations.AddField(
            model_name='imunisasidiberikan',
            name='jam_pencatatan',
            field=models.TimeField(null=True),
        ),
        migrations.AlterField(
            model_name='imunisasi',
            name='maksimum_usia',
            field=models.IntegerField(blank=True, help_text='dalam bulan. Hapus dan kosongkan jika tidak ada.', null=True),
        ),
    ]
