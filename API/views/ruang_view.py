from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from ..serializers.ruang_serializer import RuangSerializer
from ..models import ruang

class RuangListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        ruang_list = ruang.objects.all()
        serializer = RuangSerializer(ruang_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = RuangSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RuangDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            ruang_obj = ruang.objects.get(pk=pk)
            serializer = RuangSerializer(ruang_obj)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ruang.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        try:
            ruang_obj = ruang.objects.get(pk=pk)
            serializer = RuangSerializer(ruang_obj, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ruang.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            ruang_obj = ruang.objects.get(pk=pk)
            ruang_obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ruang.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
