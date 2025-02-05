from rest_framework import serializers
from API.models import inventaris

class InventarisSerializer(serializers.ModelSerializer):
    nama_jenis = serializers.CharField(source='id_jenis.nama_jenis', read_only=True)
    nama_ruang = serializers.CharField(source='id_ruang.nama_ruang', read_only=True)

    class Meta:
        model = inventaris
        fields = '__all__'
        extra_fields = ['nama_jenis', 'nama_ruang']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['nama_jenis'] = instance.id_jenis.nama_jenis
        representation['nama_ruang'] = instance.id_ruang.nama_ruang
        return representation
