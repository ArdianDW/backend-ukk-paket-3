from rest_framework import serializers
from API.models import RiwayatPeminjaman, detail_pinjam

class RiwayatAktivitasSerializer(serializers.ModelSerializer):
    nama_peminjam = serializers.CharField(source='peminjaman.id_pegawai.nama_pegawai', read_only=True)
    barang_dipinjam = serializers.SerializerMethodField()
    tanggal_meminjam = serializers.DateField(source='peminjaman.tanggal_pinjam', format="%Y-%m-%d", read_only=True)
    tanggal_mengembalikan = serializers.DateField(source='peminjaman.tanggal_kembali', format="%Y-%m-%d", read_only=True, allow_null=True)
    status = serializers.CharField(read_only=True)
    keterangan = serializers.CharField(read_only=True)

    class Meta:
        model = RiwayatPeminjaman
        fields = ['id', 'nama_peminjam', 'barang_dipinjam', 'tanggal_meminjam', 'tanggal_mengembalikan', 'status', 'keterangan']

    def get_barang_dipinjam(self, obj):
        details = detail_pinjam.objects.filter(peminjaman=obj.peminjaman)
        return [{'nama_barang': detail.id_inventaris.nama, 'jumlah': detail.jumlah} for detail in details] 