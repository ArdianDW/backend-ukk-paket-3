from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum
from ..models import petugas, pegawai, inventaris, ruang, RiwayatPeminjaman, detail_pinjam
from ..serializers.riwayat_serializer import RiwayatPeminjamanSerializer

class DashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        total_petugas = petugas.objects.filter(id_level__id__in=[1, 2]).count()
        total_pegawai = pegawai.objects.count()
        total_ruang = ruang.objects.count()

        barang_dipinjam_ids = detail_pinjam.objects.filter(peminjaman__status_peminjaman='Dipinjam').values_list('id_inventaris', flat=True)
        barang_tersedia = inventaris.objects.filter(kondisi='baik').exclude(id__in=barang_dipinjam_ids).aggregate(total=Sum('jumlah'))['total'] or 0

        barang_rusak_dan_hilang = inventaris.objects.filter(kondisi__in=['rusak', 'hilang']).aggregate(total=Sum('jumlah'))['total'] or 0
        total_inventaris = barang_tersedia + barang_rusak_dan_hilang

        barang_dipinjam = detail_pinjam.objects.filter(peminjaman__status_peminjaman='Dipinjam').aggregate(total=Sum('jumlah'))['total'] or 0
        total_barang = total_inventaris + barang_dipinjam
        riwayat_terbaru = RiwayatPeminjaman.objects.order_by('-tanggal_riwayat')[:5]
        riwayat_serializer = RiwayatPeminjamanSerializer(riwayat_terbaru, many=True)

        data = {
            'total_petugas': total_petugas,
            'total_pegawai': total_pegawai,
            'total_inventaris': total_barang,
            'total_ruang': total_ruang,
            'barang_tersedia': barang_tersedia,
            'barang_rusak_dan_hilang': barang_rusak_dan_hilang,
            'barang_dipinjam': barang_dipinjam,
            'riwayat_terbaru': riwayat_serializer.data
        }

        return Response(data)