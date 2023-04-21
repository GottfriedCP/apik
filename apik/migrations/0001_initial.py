# Generated by Django 4.2 on 2023-04-21 06:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bayi',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nik', models.CharField(blank=True, help_text='Nomor Induk Kependudukan', max_length=16, null=True, unique=True, verbose_name='NIK')),
                ('nama', models.CharField(max_length=255)),
                ('tanggal_lahir', models.DateField()),
                ('alamat', models.TextField(blank=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'bayi',
            },
        ),
        migrations.CreateModel(
            name='Bidan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nik', models.CharField(help_text='Nomor Induk Kependudukan', max_length=16, unique=True, verbose_name='NIK')),
                ('nama', models.CharField(max_length=255)),
                ('str', models.CharField(default='0', help_text='Surat Tanda Registrasi bidan - jika ada', max_length=255, verbose_name='STR')),
            ],
            options={
                'verbose_name_plural': 'bidan',
            },
        ),
        migrations.CreateModel(
            name='Ibu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nik', models.CharField(help_text='Nomor Induk Kependudukan', max_length=16, unique=True, verbose_name='NIK')),
                ('nama', models.CharField(max_length=255)),
                ('alamat', models.TextField(blank=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'ibu',
            },
        ),
        migrations.CreateModel(
            name='Imunisasi',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama_imunisasi', models.CharField(help_text='lengkap dengan nomor urut dosis', max_length=255, unique=True)),
                ('syarat_usia', models.IntegerField(default=1, help_text='dalam bulan', verbose_name='Syarat usia')),
                ('manfaat', models.TextField(blank=True, null=True)),
                ('jika_tidak', models.TextField(blank=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'imunisasi',
                'ordering': ('syarat_usia',),
            },
        ),
        migrations.CreateModel(
            name='Penyakit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama_penyakit', models.CharField(max_length=255)),
                ('ilustrasi', models.ImageField(upload_to='ilustrasi_penyakit/')),
                ('deskripsi', models.TextField(blank=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'penyakit',
                'ordering': ('nama_penyakit',),
            },
        ),
        migrations.CreateModel(
            name='ImunisasiDiberikan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tanggal_pemberian', models.DateField()),
                ('bayi', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='imunisasi_diberikan', to='apik.bayi')),
                ('imunisasi', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='bayi_diberikan', to='apik.imunisasi')),
            ],
            options={
                'verbose_name_plural': 'imunisasi diberikan',
                'ordering': ('tanggal_pemberian',),
            },
        ),
        migrations.AddField(
            model_name='imunisasi',
            name='bayis',
            field=models.ManyToManyField(through='apik.ImunisasiDiberikan', to='apik.bayi'),
        ),
        migrations.AddField(
            model_name='imunisasi',
            name='penyakit',
            field=models.ManyToManyField(to='apik.penyakit'),
        ),
        migrations.AddField(
            model_name='bayi',
            name='bidans',
            field=models.ManyToManyField(blank=True, related_name='bayis', to='apik.bidan'),
        ),
        migrations.AddField(
            model_name='bayi',
            name='ibu',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='bayis', to='apik.ibu'),
        ),
    ]