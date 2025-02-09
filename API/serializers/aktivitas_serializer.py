from rest_framework import serializers
from API.models import peminjaman, detail_pinjam

class AktivitasSerializer(serializers.ModelSerializer):
    nama_peminjam = serializers.CharField(source='id_pegawai.nama_pegawai', read_only=True)
    barang_dipinjam = serializers.SerializerMethodField()
    tanggal_peminjaman = serializers.DateField(source='tanggal_pinjam', format="%Y-%m-%d", read_only=True)

    class Meta:
        model = peminjaman
        fields = ['id', 'nama_peminjam', 'barang_dipinjam', 'tanggal_peminjaman']

    def get_barang_dipinjam(self, obj):
        details = detail_pinjam.objects.filter(peminjaman=obj)
        return [{'nama_barang': detail.id_inventaris.nama, 'jumlah': detail.jumlah} for detail in details]

class AktivitasDetailSerializer(serializers.ModelSerializer):
    id_inventaris = serializers.IntegerField(source='id_inventaris.id', read_only=True)
    nama_barang = serializers.CharField(source='id_inventaris.nama', read_only=True)
    jenis_barang = serializers.CharField(source='id_inventaris.id_jenis.nama_jenis', read_only=True)
    ruang = serializers.CharField(source='id_inventaris.id_ruang.nama_ruang', read_only=True)
    jumlah_barang = serializers.IntegerField(source='jumlah', read_only=True)

    class Meta:
        model = detail_pinjam
        fields = ['id_inventaris', 'nama_barang', 'jenis_barang', 'ruang', 'jumlah_barang'] 