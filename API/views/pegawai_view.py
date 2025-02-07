from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from ..serializers.pegawai_serializer import PegawaiSerializer
from ..models import pegawai
# from ..serializers.pegawai_login_serializer import pegawai_login_serializer

class PegawaiListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        pegawai_list = pegawai.objects.all()  # Mengambil semua data pegawai
        serializer = PegawaiSerializer(pegawai_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = PegawaiSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PegawaiDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            pegawai_obj = pegawai.objects.get(pk=pk)
            serializer = PegawaiSerializer(pegawai_obj)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except pegawai.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        try:
            pegawai_obj = pegawai.objects.get(pk=pk)
            serializer = PegawaiSerializer(pegawai_obj, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except pegawai.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            pegawai_obj = pegawai.objects.get(pk=pk)
            pegawai_obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except pegawai.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

# class PegawaiLoginView(APIView):
#     permission_classes = [AllowAny]

#     def post(self, request, *args, **kwargs):
#         serializer = pegawai_login_serializer(data=request.data)
#         if serializer.is_valid():
#             return Response(serializer.validated_data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
