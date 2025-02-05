from rest_framework import serializers
from API.models import level

class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = level
        fields = '__all__'
