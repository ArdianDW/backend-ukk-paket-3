from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from API.models import petugas, pegawai, level
from API.serializers.pegawai_serializer import PegawaiSerializer

class RegisterPegawaiView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        # Set level to 'pegawai'
        try:
            pegawai_level = level.objects.get(nama_level='pegawai')
        except level.DoesNotExist:
            return Response({'error': 'Level pegawai not found'}, status=status.HTTP_400_BAD_REQUEST)

        request.data['id_level'] = pegawai_level.id

        serializer = PegawaiSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 