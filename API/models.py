from django.db import models

class level(models.Model):
    nama_level = models.CharField(max_length=25)

    class Meta:
        db_table = 'level'

    def __str__(self):
        return self.nama_level

class petugas(models.Model):
    username = models.CharField(max_length = 25)
    password = models.CharField(max_length = 20)
    nama_petugas = models.CharField(max_length = 100)
    id_level = models.ForeignKey(level, on_delete=models.CASCADE)

    class Meta:
        db_table = 'petugas'

    def __str__(self):
        return self.nama_petugas

class pegawai(models.Model):
    nama_pegawai = models.CharField(max_length = 50)
    nip = models.IntegerField(unique=True)
    alamat= models.CharField(max_length = 50)

    class Meta:
        db_table = 'pegawai'

    def __str__(self):
        return self.nama_pegawai


class jenis(models.Model):
    nama_jenis = models.CharField(max_length = 50)
    kode_jenis = models.IntegerField()
    keterangan = models.CharField(max_length = 50)

    class Meta:
        db_table = 'jenis'

    def __str__(self):
        return self.nama_jenis

class ruang(models.Model):
    nama_ruang = models.CharField(max_length = 30)
    kode_ruang = models.IntegerField(unique=True)
    keterangan = models.CharField(max_length = 30)

    class Meta:
        db_table = 'ruang'

class inventaris(models.Model):
    nama = models.CharField(max_length = 50)
    kondisi = models.CharField(max_length = 50)
    keterangan = models.CharField(max_length = 50)
    jumlah = models.IntegerField
    id_jenis = models.ForeignKey(jenis, on_delete=models.CASCADE)
    tanggal_register = models.DateField()
    id_ruang = models.ForeignKey(ruang, on_delete=models.CASCADE)
    kode_inventaris = models.IntegerField(unique=True)
    id_petugas = models.ForeignKey(petugas, on_delete=models.CASCADE)

    class Meta:
        db_table = 'inventaris'

    def __str__(self):
        return self.nama

class peminjaman(models.Model):
    tanggal_pinjam = models.DateField()
    tanggal_kembali = models.DateField()
    status_peminjaman = models.CharField(max_length = 20)
    id_pegawai = models.ForeignKey(pegawai, on_delete=models.CASCADE)

    class Meta:
        db_table = 'peminjaman'

    def __str__(self):
        return f"Peminjaman oleh {self.id_pegawai.nama_pegawai} pada {self.tanggal_pinjam}"

class detail_pinjam(models.Model):
    id_invetaris = models.ForeignKey(inventaris, on_delete=models.CASCADE)
    id_peminjaman = models.ForeignKey(peminjaman, on_delete=models.CASCADE)
    jumlah = models.IntegerField()

    class Meta:
        db_table = 'detail_pinjam'

    def __str__(self):
        return f"Detail Peminjaman {self.id_peminjaman.id} - {self.id_inventaris.nama}"


