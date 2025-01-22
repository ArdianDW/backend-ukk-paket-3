from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from ..serializers.jenis_serializer import JenisSerializer
from ..models import jenis

class JenisListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        jenis_list = jenis.objects.all()
        serializer = JenisSerializer(jenis_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = JenisSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class JenisDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            jenis_obj = jenis.objects.get(pk=pk)
            serializer = JenisSerializer(jenis_obj)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except jenis.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        try:
            jenis_obj = jenis.objects.get(pk=pk)
            serializer = JenisSerializer(jenis_obj, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except jenis.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            jenis_obj = jenis.objects.get(pk=pk)
            jenis_obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except jenis.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
