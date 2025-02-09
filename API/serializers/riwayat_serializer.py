from rest_framework import serializers
from API.models import RiwayatPeminjaman

class RiwayatPeminjamanSerializer(serializers.ModelSerializer):
    nama_peminjam = serializers.CharField(source='peminjaman.id_pegawai.nama_pegawai', read_only=True)
    jenis_barang = serializers.CharField(source='peminjaman.detail_pinjam_set.first.id_inventaris.id_jenis.nama_jenis', read_only=True)
    nama_barang = serializers.CharField(source='peminjaman.detail_pinjam_set.first.id_inventaris.nama', read_only=True)
    jumlah_barang = serializers.IntegerField(source='peminjaman.detail_pinjam_set.first.jumlah', read_only=True)
    ruang = serializers.CharField(source='peminjaman.detail_pinjam_set.first.id_inventaris.id_ruang.nama_ruang', read_only=True)
    tanggal_peminjaman = serializers.DateField(source='peminjaman.tanggal_pinjam', format="%Y-%m-%d", read_only=True)

    class Meta:
        model = RiwayatPeminjaman
        fields = ['id', 'nama_peminjam', 'jenis_barang', 'nama_barang', 'jumlah_barang', 'ruang', 'tanggal_peminjaman', 'status', 'keterangan'] 