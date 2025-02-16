from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from API.models import peminjaman, detail_pinjam, inventaris
from API.serializers.peminjaman_serializer import PeminjamanDetailSerializer

class PeminjamanPengembalianView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        try:
            peminjaman_instance = peminjaman.objects.get(pk=pk, id_pegawai=request.user.id)
            if peminjaman_instance.status_peminjaman == "Dikembalikan":
                return Response({'error': 'Peminjaman sudah dikembalikan'}, status=status.HTTP_400_BAD_REQUEST)

            # Update status peminjaman
            peminjaman_instance.status_peminjaman = "Dikembalikan"
            peminjaman_instance.status_approval = "pending"  # Atau 'diterima' jika langsung diterima
            peminjaman_instance.save()

            # Update kondisi barang
            details_data = request.data.get('details', [])
            for detail_data in details_data:
                detail = detail_pinjam.objects.get(peminjaman=peminjaman_instance, id_inventaris=detail_data['id_inventaris'])
                detail.kondisi = detail_data.get('kondisi', detail.kondisi)
                detail.save()

                inventaris_instance = inventaris.objects.get(id=detail.id_inventaris.id)
                if detail.kondisi == 'baik':
                    inventaris_instance.jumlah += detail_data['jumlah']
                elif detail.kondisi == 'rusak':
                    rusak_inventaris, created = inventaris.objects.get_or_create(
                        nama=inventaris_instance.nama,
                        kondisi='rusak',
                        defaults={
                            'kode_inventaris': inventaris_instance.kode_inventaris,
                            'keterangan': 'Barang rusak',
                            'jumlah': 0,
                            'id_jenis': inventaris_instance.id_jenis,
                            'id_ruang': inventaris_instance.id_ruang,
                            'id_petugas': inventaris_instance.id_petugas,
                            'tanggal_register': inventaris_instance.tanggal_register
                        }
                    )
                    rusak_inventaris.jumlah += detail_data['jumlah']
                    rusak_inventaris.save()
                elif detail.kondisi == 'hilang':
                    hilang_inventaris, created = inventaris.objects.get_or_create(
                        nama=inventaris_instance.nama,
                        kondisi='hilang',
                        defaults={
                            'kode_inventaris': inventaris_instance.kode_inventaris,
                            'keterangan': 'Barang hilang',
                            'jumlah': 0,
                            'id_jenis': inventaris_instance.id_jenis,
                            'id_ruang': inventaris_instance.id_ruang,
                            'id_petugas': inventaris_instance.id_petugas,
                            'tanggal_register': inventaris_instance.tanggal_register
                        }
                    )
                    hilang_inventaris.jumlah += detail_data['jumlah']
                    hilang_inventaris.save()

                inventaris_instance.save()

            serializer = PeminjamanDetailSerializer(peminjaman_instance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except peminjaman.DoesNotExist:
            return Response({'error': 'Peminjaman tidak ditemukan'}, status=status.HTTP_404_NOT_FOUND) 