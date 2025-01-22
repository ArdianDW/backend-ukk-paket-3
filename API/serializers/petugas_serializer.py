from rest_framework import serializers
from API.models import petugas

class pegawai_serializer(serializers.ModelSerializer):
    class Meta:
        model = petugas
        fields = '__all__'
