from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from ..serializers.inventaris_serializer import InventarisSerializer
from ..models import inventaris

class InventarisListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        inventaris_list = inventaris.objects.all()  
        serializer = InventarisSerializer(inventaris_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = InventarisSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class InventarisDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            inventaris_obj = inventaris.objects.get(pk=pk)
            serializer = InventarisSerializer(inventaris_obj)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except inventaris.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        try:
            inventaris_obj = inventaris.objects.get(pk=pk)
            serializer = InventarisSerializer(inventaris_obj, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except inventaris.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            inventaris_obj = inventaris.objects.get(pk=pk)
            inventaris_obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except inventaris.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

class InventarisBaikListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Filter inventaris yang kondisinya baik dan jumlahnya lebih dari 0
        inventaris_list = inventaris.objects.filter(kondisi='baik', jumlah__gt=0)
        serializer = InventarisSerializer(inventaris_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
