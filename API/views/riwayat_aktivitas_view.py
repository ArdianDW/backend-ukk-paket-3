from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from API.models import RiwayatPeminjaman
from API.serializers.riwayat_aktivitas_serializer import RiwayatAktivitasSerializer

class RiwayatAktivitasListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        riwayat_aktivitas_list = RiwayatPeminjaman.objects.all().order_by('-tanggal_riwayat')
        serializer = RiwayatAktivitasSerializer(riwayat_aktivitas_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK) 