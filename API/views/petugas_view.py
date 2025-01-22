from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from ..models import petugas
from ..serializers.petugas_serializer import petugas_serializer
from ..serializers.petugas_login_serializer import petugas_login_serializer
from rest_framework_simplejwt.tokens import RefreshToken

class petugas_login_view(APIView):
    def post(self, request):
        serializer = petugas_login_serializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class petugas_list_view(APIView):
    def get(self, request):
        petugas_list = petugas.objects.all()
        serializer = petugas_serializer(petugas_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = petugas_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class petugas_detail_view(APIView):
    def get(self, request, pk):
        try:
            petugas_obj = petugas.objects.get(pk=pk)
            serializer = petugas_serializer(petugas_obj)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except petugas.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        try:
            petugas_obj = petugas.objects.get(pk=pk)
            serializer = petugas_serializer(petugas_obj, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except petugas.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            petugas_obj = petugas.objects.get(pk=pk)
            petugas_obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except petugas.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

class logout_view(APIView):
    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


