from rest_framework import serializers
from API.models import inventaris

class InventarisSerializer(serializers.ModelSerializer):
    nama_ruang = serializers.CharField(source='id_ruang.nama', read_only=True)
    nama_jenis = serializers.CharField(source='id_jenis.nama', read_only=True)

    class Meta:
        model = inventaris
        fields = ['id', 'nama', 'kondisi', 'keterangan', 'jumlah', 'id_jenis', 'tanggal_register', 'id_ruang', 'kode_inventaris', 'id_petugas', 'nama_ruang', 'nama_jenis']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['nama_jenis'] = instance.id_jenis.nama_jenis
        representation['nama_ruang'] = instance.id_ruang.nama_ruang
        return representation
