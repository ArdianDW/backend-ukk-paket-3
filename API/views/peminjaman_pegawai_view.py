from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from API.models import peminjaman, detail_pinjam, inventaris, RiwayatPeminjaman
from API.serializers.peminjaman_serializer import PeminjamanCreateSerializer, PeminjamanDetailSerializer

class PeminjamanPegawaiView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PeminjamanCreateSerializer(data=request.data)
        if serializer.is_valid():
            peminjaman_instance = serializer.save(status_approval='pending')
            
            # Simpan ke RiwayatPeminjaman
            RiwayatPeminjaman.objects.create(
                peminjaman=peminjaman_instance,
                status="Peminjaman Dibuat",
                keterangan="Meminjam"
            )
            
            output_serializer = PeminjamanDetailSerializer(peminjaman_instance)
            return Response(output_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            peminjaman_instance = peminjaman.objects.get(pk=pk)
            if peminjaman_instance.status_peminjaman == "Dikembalikan":
                return Response({'error': 'Peminjaman sudah dikembalikan'}, status=status.HTTP_400_BAD_REQUEST)

            # Update status peminjaman untuk pengajuan pengembalian
            peminjaman_instance.status_peminjaman = "Dikembalikan"
            peminjaman_instance.status_approval = "pending"
            peminjaman_instance.tanggal_kembali = timezone.now().date()  # Set tanggal_kembali ke hari ini
            peminjaman_instance.save()

            # Simpan ke RiwayatPeminjaman
            RiwayatPeminjaman.objects.create(
                peminjaman=peminjaman_instance,
                status="Dikembalikan",
                keterangan="Mengembalikan"
            )

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

class PeminjamanPengajuanListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        pegawai_id = request.user.id
        peminjaman_list = peminjaman.objects.filter(id_pegawai=pegawai_id).order_by('status_approval')
        serializer = PeminjamanDetailSerializer(peminjaman_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
