import datetime

from django.db import models

nik_help_text = 'Nomor Induk Kependudukan'


class Ibu(models.Model):
    """
    Model representasi ibu dari balita. Ibu dapat diganti ayah atau wali tergantung sikon.
    """
    nik = models.CharField(verbose_name='NIK', max_length=16,
                           unique=True, help_text=nik_help_text)
    nama = models.CharField(max_length=255)
    alamat = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name_plural = 'ibu'

    def __str__(self):
        return self.nama


class Bidan(models.Model):
    """Model representasi bidan."""
    nik = models.CharField(verbose_name='NIK', max_length=16,
                           unique=True, help_text=nik_help_text)
    nama = models.CharField(max_length=255)
    str_help_text = 'Surat Tanda Registrasi bidan - jika ada'
    str = models.CharField(verbose_name='STR', max_length=255,
                           default='0', help_text=str_help_text)

    class Meta:
        verbose_name_plural = 'bidan'

    def __str__(self):
        return self.nama


class Bayi(models.Model):
    """Model representasi anak/balita/bayi."""
    nik = models.CharField(verbose_name='NIK', max_length=16,
                           blank=True, null=True, unique=True, help_text=nik_help_text)
    nama = models.CharField(max_length=255)
    ibu = models.ForeignKey(
        to='Ibu', on_delete=models.SET_NULL, null=True, related_name='bayis')
    # bidan2 yg menangani anak ini
    bidans = models.ManyToManyField(
        to='Bidan', related_name='bayis', blank=True)
    tanggal_lahir = models.DateField()
    alamat = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.nama

    class Meta:
        verbose_name = 'balita'
        verbose_name_plural = 'balita'

    def get_usia_bulan(self):
        # today = datetime.date.today()
        # tanggal_lahir = self.tanggal_lahir
        # return (today.year - tanggal_lahir.year) * 12 + (today.month - tanggal_lahir.month)

        # https://stackoverflow.com/a/68997918
        tanggal_lahir = self.tanggal_lahir
        today = datetime.date.today()
        time_difference = today - tanggal_lahir
        days = time_difference.days
        return int((days/365)*12)


class Imunisasi(models.Model):
    """Model repr imunisasi dengan nomor urut dosis, misal Polio I atau DPT-HB II."""
    help_text_nama_imunisasi = 'lengkap dengan nomor urut dosis'
    help_text_syarat_usia = 'dalam bulan'
    help_text_maksimum_usia = 'dalam bulan. Hapus dan kosongkan jika tidak ada.'
    help_text_penyakit = 'Imunisasi ini mencegah penyakit apa saja?'

    nama_imunisasi = models.CharField(
        max_length=255, unique=True, help_text=help_text_nama_imunisasi)
    syarat_usia = models.IntegerField(
        verbose_name='Syarat usia', default=1, help_text=help_text_syarat_usia)
    maksimum_usia = models.IntegerField(blank=True, null=True, help_text=help_text_maksimum_usia)
    manfaat = models.TextField(null=True, blank=True)
    jika_tidak = models.TextField(null=True, blank=True)
    penyakits = models.ManyToManyField(
        to='Penyakit', verbose_name='penyakit', help_text=help_text_penyakit)
    bayis = models.ManyToManyField(to='Bayi', through='ImunisasiDiberikan')

    def __str__(self):
        return self.nama_imunisasi

    class Meta:
        verbose_name_plural = 'imunisasi'
        ordering = ('syarat_usia', )


class ImunisasiDiberikan(models.Model):
    """Model perantara m2m bayi dan imunisasi."""
    tanggal_pemberian = models.DateField()
    # jam pencatatan utk melengkapi tanggal setelah ada permintaan dari manusia2 aneh
    jam_pencatatan = models.TimeField(null=True, blank=True, verbose_name='jam pencatatan (WIB)')
    # bidan yg menginput
    bidan = models.ForeignKey(
        to='Bidan', on_delete=models.SET_NULL, null=True, related_name='imunisasi_dilakukan')
    bayi = models.ForeignKey(
        to='Bayi', on_delete=models.CASCADE, related_name='imunisasi_diberikan')
    imunisasi = models.ForeignKey(
        to='Imunisasi', on_delete=models.SET_NULL, null=True, related_name='bayi_diberikan')

    def __str__(self):
        return f'{self.tanggal_pemberian} {self.imunisasi} - {self.bayi}'
    
    def save(self, *args, **kwargs):
        if self.jam_pencatatan is None:
            # lihat juga fungsi view tambah_imunisasi
            self.jam_pencatatan = datetime.datetime.now()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'imunisasi-balita'
        verbose_name_plural = 'imunisasi-balita'
        ordering = ('-tanggal_pemberian', 'jam_pencatatan')


class Penyakit(models.Model):
    nama_penyakit = models.CharField(max_length=255)
    # file will be uploaded to MEDIA_ROOT/path
    ilustrasi = models.ImageField(
        upload_to="ilustrasi_penyakit/", blank=True, null=True)
    deskripsi = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.nama_penyakit

    class Meta:
        verbose_name_plural = 'penyakit'
        ordering = ('nama_penyakit', )
