from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password
from ..models import petugas

class petugas_login_serializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        try:
            petugas_obj = petugas.objects.get(username=username)
        except petugas.DoesNotExist:
            raise serializers.ValidationError('Petugas username does not exist')

        if not check_password(password, petugas_obj.password):
            raise serializers.ValidationError('Petugas password incorrect')

        refresh = RefreshToken.for_user(petugas_obj)

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'petugas': {
                'id': petugas_obj.id,
                'username': petugas_obj.username,
                'nama_petugas': petugas_obj.nama_petugas,
                'level': petugas_obj.id_level.nama_level,
            }
        }