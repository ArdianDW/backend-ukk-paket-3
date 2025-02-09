from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from API.models import inventaris, peminjaman, detail_pinjam, RiwayatPeminjaman
from django.utils import timezone

class DetailPinjamSerializer(serializers.ModelSerializer):
    class Meta:
        model = detail_pinjam
        fields = ['id_inventaris', 'jumlah', 'kondisi']

class PeminjamanSerializer(serializers.ModelSerializer):
    details = DetailPinjamSerializer(many=True, write_only=True)
    tanggal_pinjam = serializers.DateField(format="%Y-%m-%d", read_only=True)
    tanggal_kembali = serializers.DateField(format="%Y-%m-%d", required=False)

    class Meta:
        model = peminjaman
        fields = '__all__'
        read_only_fields = ['tanggal_pinjam', 'status_peminjaman']

    def create(self, validated_data):
        details_data = validated_data.pop('details')

        for detail_data in details_data:
            inventaris_instance = inventaris.objects.get(pk=detail_data['id_inventaris'].id)
            if inventaris_instance.jumlah < detail_data['jumlah']:
                raise ValidationError({
                    'detail': f"Jumlah barang {inventaris_instance.nama} tidak mencukupi. Tersedia: {inventaris_instance.jumlah}, Diminta: {detail_data['jumlah']}"
                })

        peminjaman_instance = peminjaman.objects.create(**validated_data)

        for detail_data in details_data:
            inventaris_instance = inventaris.objects.get(pk=detail_data['id_inventaris'].id)
            inventaris_instance.jumlah -= detail_data['jumlah']
            inventaris_instance.save()

            detail_pinjam.objects.create(peminjaman=peminjaman_instance, **detail_data)

        RiwayatPeminjaman.objects.create(
            peminjaman=peminjaman_instance,
            status="Dipinjam",
            keterangan="Meminjam"
        )

        return peminjaman_instance

    def update(self, instance, validated_data):
        if instance.status_peminjaman == "Dikembalikan":
            raise ValidationError("Peminjaman ini sudah dikembalikan dan tidak dapat diproses lagi.")

        instance.tanggal_kembali = timezone.now().date()
        instance.status_peminjaman = "Dikembalikan"
        instance.save()

        RiwayatPeminjaman.objects.create(
            peminjaman=instance,
            status="Dikembalikan",
            keterangan="Mengembalikan"
        )

        details_data = validated_data.pop('details', [])
        for detail_data in details_data:
            detail = detail_pinjam.objects.get(peminjaman=instance, id_inventaris=detail_data['id_inventaris'])
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

            inventaris_instance.save()

        return instance