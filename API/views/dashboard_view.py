from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ..models import petugas, pegawai, inventaris, ruang

class DashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        total_petugas = petugas.objects.count()
        total_pegawai = pegawai.objects.count()
        total_inventaris = inventaris.objects.count()
        total_ruang = ruang.objects.count()

        data = {
            'total_petugas': total_petugas,
            'total_pegawai': total_pegawai,
            'total_inventaris': total_inventaris,
            'total_ruang': total_ruang
        }

        return Response(data) 