from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from API.models import peminjaman
from API.serializers.transaksi_serializer import PeminjamanSerializer

class PeminjamanViewSet(viewsets.ModelViewSet):
    queryset = peminjaman.objects.all()
    serializer_class = PeminjamanSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)
