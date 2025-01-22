from rest_framework import serializers
from API.models import pegawai

class pegawaiSerializer(serializers.ModelSerializer):
    class Meta:
        model = pegawai
        fields = '__all__'