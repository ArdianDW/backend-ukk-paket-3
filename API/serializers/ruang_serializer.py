from rest_framework import serializers
from API.models import ruang

class RuangSerializer(serializers.ModelSerializer):
    class Meta:
        model = ruang
        fields = '__all__'
