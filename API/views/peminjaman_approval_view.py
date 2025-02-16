from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from API.models import peminjaman
from API.serializers.peminjaman_serializer import PeminjamanDetailSerializer

class PeminjamanApprovalView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        try:
            peminjaman_obj = peminjaman.objects.get(pk=pk)
            status_approval = request.data.get('status_approval')
            if status_approval not in ['diterima', 'ditolak']:
                return Response({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)

            peminjaman_obj.status_approval = status_approval
            peminjaman_obj.save()
            serializer = PeminjamanDetailSerializer(peminjaman_obj)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except peminjaman.DoesNotExist:
            return Response({'error': 'Peminjaman not found'}, status=status.HTTP_404_NOT_FOUND) 