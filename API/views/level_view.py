from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from API.models import level
from API.serializers.level_serializer import LevelSerializer

class LevelListView(APIView):
    def get(self, request):
        levels = level.objects.filter(id__in=[1, 2])
        serializer = LevelSerializer(levels, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = LevelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LevelDetailView(APIView):
    def get(self, request, pk):
        try:
            level_obj = level.objects.get(pk=pk)
            serializer = LevelSerializer(level_obj)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except level.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        try:
            level_obj = level.objects.get(pk=pk)
            serializer = LevelSerializer(level_obj, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except level.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            level_obj = level.objects.get(pk=pk)
            level_obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except level.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
