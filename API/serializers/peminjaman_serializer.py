from rest_framework import serializers
from API.models import peminjaman, detail_pinjam


class PeminjamanDetailSerializer(serializers.ModelSerializer):
    nama_peminjam = serializers.CharField(source='id_pegawai.nama_pegawai', read_only=True)
    details = serializers.SerializerMethodField()
    keterangan = serializers.CharField(read_only=True)

    class Meta:
        model = peminjaman
        fields = ['id', 'nama_peminjam', 'tanggal_pinjam', 'tanggal_kembali', 'status_approval', 'keterangan', 'details']

    def get_details(self, obj):
        details = detail_pinjam.objects.filter(peminjaman=obj)
        return DetailPinjamSerializer(details, many=True).data


class DetailPinjamSerializer(serializers.ModelSerializer):
    nama_barang = serializers.CharField(source='id_inventaris.nama', read_only=True)
    jenis_barang = serializers.CharField(source='id_inventaris.id_jenis.nama_jenis', read_only=True)
    ruang = serializers.CharField(source='id_inventaris.id_ruang.nama_ruang', read_only=True)
    jumlah_barang = serializers.IntegerField(source='jumlah', read_only=True)

    class Meta:
        model = detail_pinjam
        fields = ['nama_barang', 'jenis_barang', 'ruang', 'jumlah_barang']


class DetailPinjamCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = detail_pinjam
        fields = ['id_inventaris', 'jumlah']


class PeminjamanCreateSerializer(serializers.ModelSerializer):
    details = DetailPinjamCreateSerializer(many=True)

    class Meta:
        model = peminjaman
        fields = ['id_pegawai', 'tanggal_pinjam', 'tanggal_kembali', 'keterangan', 'details']

    def create(self, validated_data):
        details_data = validated_data.pop('details')
        validated_data.pop('status_approval', None)
        peminjaman_instance = peminjaman.objects.create(status_approval='pending', **validated_data)
        for detail_data in details_data:
            detail_pinjam.objects.create(peminjaman=peminjaman_instance, **detail_data)
        return peminjaman_instance
