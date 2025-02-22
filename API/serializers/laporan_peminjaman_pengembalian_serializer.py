from rest_framework import serializers
from API.models import RiwayatPeminjaman, detail_pinjam

class LaporanPeminjamanPengembalianSerializer(serializers.ModelSerializer):
    nama_peminjam = serializers.CharField(source='peminjaman.id_pegawai.nama_pegawai', read_only=True)
    barang_dipinjam = serializers.SerializerMethodField()
    jumlah_total = serializers.IntegerField(source='peminjaman.jumlah_total', read_only=True)
    tanggal = serializers.SerializerMethodField()

    class Meta:
        model = RiwayatPeminjaman
        fields = ['id', 'nama_peminjam', 'barang_dipinjam', 'jumlah_total', 'tanggal']

    def get_barang_dipinjam(self, obj):
        details = detail_pinjam.objects.filter(peminjaman=obj.peminjaman)
        return [{'nama_barang': detail.id_inventaris.nama, 'jumlah': detail.jumlah} for detail in details]

    def get_tanggal(self, obj):
        request = self.context.get('request')
        laporan_type = request.query_params.get('type', 'peminjaman')
        if laporan_type == 'peminjaman':
            return obj.peminjaman.tanggal_pinjam
        elif laporan_type == 'pengembalian':
            return obj.peminjaman.tanggal_kembali
        return None 