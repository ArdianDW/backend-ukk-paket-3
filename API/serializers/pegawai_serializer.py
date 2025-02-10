from rest_framework import serializers
from API.models import pegawai, petugas

class PegawaiSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True, required=False)
    password = serializers.CharField(write_only=True, required=False)
    id_level = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = pegawai
        fields = ['id', 'nama_pegawai', 'nip', 'alamat', 'username', 'password', 'id_level']

    def create(self, validated_data):
        # Extract petugas data
        petugas_data = {
            'username': validated_data.pop('username'),
            'password': validated_data.pop('password'),
            'nama_petugas': validated_data['nama_pegawai'],  # Assuming nama_petugas is the same as nama_pegawai
            'id_level_id': validated_data.pop('id_level')
        }
        
        # Create petugas
        petugas_obj = petugas.objects.create_user(**petugas_data)

        # Create pegawai
        pegawai_data = {
            'nama_pegawai': validated_data['nama_pegawai'],
            'nip': validated_data['nip'],
            'alamat': validated_data['alamat'],
            'petugas_id': petugas_obj  
        }
        return pegawai.objects.create(**pegawai_data)

    def update(self, instance, validated_data):
        # Update pegawai fields
        instance.nama_pegawai = validated_data.get('nama_pegawai', instance.nama_pegawai)
        instance.nip = validated_data.get('nip', instance.nip)
        instance.alamat = validated_data.get('alamat', instance.alamat)
        instance.save()

        # Update related petugas fields
        petugas_obj = instance.petugas_id
        petugas_obj.username = validated_data.get('username', petugas_obj.username)
        if 'password' in validated_data:
            petugas_obj.set_password(validated_data['password'])
        petugas_obj.save()

        return instance