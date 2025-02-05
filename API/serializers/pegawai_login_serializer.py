# from rest_framework import serializers
# from rest_framework_simplejwt.tokens import RefreshToken
# from django.contrib.auth.hashers import check_password
# from ..models import pegawai
#
# class pegawai_login_serializer(serializers.Serializer):
#     nip = serializers.CharField(required=True)
#     password = serializers.CharField(required=True, write_only=True)
#
#     def validate(self, data):
#         nip = data.get('nip')
#         password = data.get('password')
#
#         try:
#             pegawai_obj = pegawai.objects.get(nip=nip)
#         except pegawai.DoesNotExist:
#             raise serializers.ValidationError('NIP salah!')
#
#         if not check_password(password, pegawai_obj.password):
#             raise serializers.ValidationError('Kata sandi salah!')
#
#         refresh = RefreshToken.for_user(pegawai_obj)
#
#         return {
#             'refresh': str(refresh),
#             'access': str(refresh.access_token),
#             'pegawai': {
#                 'id': pegawai_obj.id,
#                 'nip': pegawai_obj.nip,
#                 'nama_pegawai': pegawai_obj.nama_pegawai,
#             }
#         }
