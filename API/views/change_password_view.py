from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.contrib.auth.hashers import check_password, make_password
from API.models import petugas

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        petugas_obj = request.user
        current_password = request.data.get('current_password')
        new_password = request.data.get('new_password')

        if not check_password(current_password, petugas_obj.password):
            return Response({'error': 'Kata sandi saat ini salah!'}, status=status.HTTP_400_BAD_REQUEST)

        petugas_obj.password = make_password(new_password)
        petugas_obj.save()
        return Response({'success': 'Kata sandi berhasil diperbarui!'}, status=status.HTTP_200_OK) 