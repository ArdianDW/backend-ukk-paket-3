from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from API.models import petugas

class petugas_serializer(serializers.ModelSerializer):
    class Meta:
        model = petugas
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True},  # Password hanya dapat ditulis, tidak ditampilkan
        }

    def create(self, validated_data):
        # Hash password sebelum menyimpan data
        if 'password' in validated_data:
            validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # Hash password jika di-update
        if 'password' in validated_data:
            validated_data['password'] = make_password(validated_data['password'])
        return super().update(instance, validated_data)
