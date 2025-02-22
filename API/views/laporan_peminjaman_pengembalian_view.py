from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from API.models import RiwayatPeminjaman
from API.serializers.laporan_peminjaman_pengembalian_serializer import LaporanPeminjamanPengembalianSerializer
from django.utils import timezone

class LaporanPeminjamanPengembalianView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        laporan_type = request.query_params.get('type', 'peminjaman')
        now = timezone.now()

        if laporan_type == 'peminjaman':
            riwayat_list = RiwayatPeminjaman.objects.filter(
                peminjaman__tanggal_pinjam__year=now.year,
                peminjaman__tanggal_pinjam__month=now.month
            )
        elif laporan_type == 'pengembalian':
            riwayat_list = RiwayatPeminjaman.objects.filter(
                peminjaman__tanggal_kembali__year=now.year,
                peminjaman__tanggal_kembali__month=now.month
            )
        else:
            return Response({'error': 'Invalid report type'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = LaporanPeminjamanPengembalianSerializer(riwayat_list, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK) 