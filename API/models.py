from operator import truediv

from django.db import models
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class level(models.Model):
    nama_level = models.CharField(max_length=25)

    class Meta:
        db_table = 'level'

    def __str__(self):
        return self.nama_level

class PetugasManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username field must be set')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, password, **extra_fields)

class petugas(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=25, unique=True)
    password = models.CharField(max_length=128)
    nama_petugas = models.CharField(max_length=100)
    id_level = models.ForeignKey(level, on_delete=models.CASCADE)

    groups = models.ManyToManyField(
        "auth.Group",
        related_name="petugas_groups",
        blank=True
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="petugas_permissions",
        blank=True
    )

    objects = PetugasManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    class Meta:
        db_table = 'petugas'

    def __str__(self):
        return self.nama_petugas

class pegawai(models.Model):
    nama_pegawai = models.CharField(max_length=50)
    nip = models.CharField(max_length=20, unique=True)
    alamat = models.CharField(max_length=50)
    petugas_id = models.OneToOneField(petugas, on_delete=models.CASCADE)

    class Meta:
        db_table = 'pegawai'

    def __str__(self):
        return self.nama_pegawai

class jenis(models.Model):
    nama_jenis = models.CharField(max_length=50)
    kode_jenis = models.CharField(max_length=20, unique=True)
    keterangan = models.CharField(max_length=50)

    class Meta:
        db_table = 'jenis'

    def __str__(self):
        return self.nama_jenis

class ruang(models.Model):
    nama_ruang = models.CharField(max_length=30)
    kode_ruang = models.CharField(max_length=20, unique=True)
    keterangan = models.CharField(max_length=30)

    class Meta:
        db_table = 'ruang'

class inventaris(models.Model):
    nama = models.CharField(max_length=50)
    kondisi = models.CharField(max_length=50)
    keterangan = models.CharField(max_length=50)
    jumlah = models.PositiveIntegerField()
    id_jenis = models.ForeignKey(jenis, on_delete=models.CASCADE)
    tanggal_register = models.DateField()
    id_ruang = models.ForeignKey(ruang, on_delete=models.CASCADE)
    kode_inventaris = models.CharField(max_length=20)
    id_petugas = models.ForeignKey(petugas, on_delete=models.CASCADE)

    class Meta:
        db_table = 'inventaris'

    def __str__(self):
        return self.nama

class peminjaman(models.Model):
    tanggal_pinjam = models.DateField()
    tanggal_kembali = models.DateField(null=True, blank=True)
    status_peminjaman = models.CharField(max_length=20, default='Dipinjam')
    id_pegawai = models.ForeignKey(pegawai, on_delete=models.CASCADE)
    keterangan = models.TextField(null=True, blank=True)

    STATUS_APPROVAL_CHOICES = [
        ('pending', 'Pending'),
        ('diterima', 'Diterima'),
        ('ditolak', 'Ditolak'),
    ]
    status_approval = models.CharField(max_length=10, choices=STATUS_APPROVAL_CHOICES, default='pending')

    def __str__(self):
        return f"Peminjaman oleh {self.id_pegawai.nama_pegawai} pada {self.tanggal_pinjam}"

class detail_pinjam(models.Model):
    id_inventaris = models.ForeignKey(inventaris, on_delete=models.CASCADE)
    jumlah = models.IntegerField()
    peminjaman = models.ForeignKey(peminjaman, on_delete=models.CASCADE)
    kondisi = models.CharField(max_length=10, choices=[('baik', 'Baik'), ('rusak', 'Rusak'), ('hilang', 'Hilang')], null=True, blank=True)

    class Meta:
        db_table = 'detail_pinjam'

    def __str__(self):
        return f"Detail Pinjam: {self.id_inventaris.nama} - {self.jumlah}"

class RiwayatPeminjaman(models.Model):
    peminjaman = models.ForeignKey(peminjaman, on_delete=models.CASCADE)
    tanggal_riwayat = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20)
    keterangan = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'riwayat_peminjaman'

    def __str__(self):
        return f"Riwayat {self.peminjaman.id} - {self.status}"


