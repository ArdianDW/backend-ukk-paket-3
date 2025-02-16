from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from API.models import peminjaman, detail_pinjam
from API.serializers.aktivitas_serializer import AktivitasSerializer, AktivitasDetailSerializer

class AktivitasListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Filter peminjaman yang statusnya 'Dipinjam' dan disetujui
        aktivitas_list = peminjaman.objects.filter(status_peminjaman='Dipinjam', status_approval='diterima')
        serializer = AktivitasSerializer(aktivitas_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class AktivitasPendingView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        aktivitas_list = peminjaman.objects.filter(
            status_peminjaman__in=['Dipinjam', 'Dikembalikan'],
            status_approval='pending'
        )
        serializer = AktivitasSerializer(aktivitas_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class AktivitasDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            peminjaman_instance = peminjaman.objects.get(pk=pk)
            details = detail_pinjam.objects.filter(peminjaman=peminjaman_instance)
            serializer = AktivitasDetailSerializer(details, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except peminjaman.DoesNotExist:
            return Response({'error': 'Peminjaman not found'}, status=status.HTTP_404_NOT_FOUND)

class AktivitasUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        aktivitas_list = peminjaman.objects.filter(
            id_pegawai__id=user_id,
            status_peminjaman='Dipinjam',
            status_approval='diterima'
        )
        serializer = AktivitasSerializer(aktivitas_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK) 