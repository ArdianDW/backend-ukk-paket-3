from rest_framework import serializers
from API.models import jenis

class JenisSerializer(serializers.ModelSerializer):
    class Meta:
        model = jenis
        fields = '__all__'
