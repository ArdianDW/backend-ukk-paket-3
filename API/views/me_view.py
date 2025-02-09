from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from API.models import petugas
from API.serializers.petugas_serializer import petugas_serializer

class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        petugas_obj = request.user
        serializer = petugas_serializer(petugas_obj)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        petugas_obj = request.user
        serializer = petugas_serializer(petugas_obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 