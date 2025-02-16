from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from API.models import peminjaman
from API.serializers.peminjaman_serializer import PeminjamanDetailSerializer, PeminjamanCreateSerializer

class PeminjamanListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        peminjaman_list = peminjaman.objects.all()
        serializer = PeminjamanDetailSerializer(peminjaman_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = PeminjamanCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PeminjamanApprovalView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            peminjaman_instance = peminjaman.objects.get(pk=pk)
        except peminjaman.DoesNotExist:
            return Response({'error': 'Peminjaman not found'}, status=status.HTTP_404_NOT_FOUND)

        if peminjaman_instance.is_approved:
            return Response({'error': 'Peminjaman already approved'}, status=status.HTTP_400_BAD_REQUEST)

        peminjaman_instance.is_approved = True
        peminjaman_instance.save()

        output_serializer = PeminjamanDetailSerializer(peminjaman_instance)
        return Response(output_serializer.data, status=status.HTTP_200_OK)