# Generated by Django 4.2 on 2023-04-21 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apik', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='imunisasi',
            name='penyakit',
        ),
        migrations.AddField(
            model_name='imunisasi',
            name='penyakits',
            field=models.ManyToManyField(help_text='Imunisasi ini mencegah penyakit apa saja?', to='apik.penyakit'),
        ),
    ]
