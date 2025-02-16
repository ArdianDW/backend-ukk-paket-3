from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from API.models import peminjaman
from API.serializers.peminjaman_serializer import PeminjamanDetailSerializer

class PeminjamanUserListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        peminjaman_list = peminjaman.objects.filter(id_pegawai=user_id)
        serializer = PeminjamanDetailSerializer(peminjaman_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK) 