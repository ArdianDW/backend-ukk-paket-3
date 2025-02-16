from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from API.models import inventaris
from API.serializers.inventaris_serializer import InventarisSerializer
from django.utils import timezone

class LaporanView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        laporan_type = request.query_params.get('type', 'all')

        if laporan_type == 'all':
            inventaris_list = inventaris.objects.all()
        elif laporan_type == 'recent':
            now = timezone.now()
            inventaris_list = inventaris.objects.filter(
                tanggal_register__year=now.year,
                tanggal_register__month=now.month
            )
        elif laporan_type == 'rusak':
            inventaris_list = inventaris.objects.filter(kondisi='rusak')
        elif laporan_type == 'hilang':
            inventaris_list = inventaris.objects.filter(kondisi='hilang')
        else:
            return Response({'error': 'Invalid report type'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = InventarisSerializer(inventaris_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK) 