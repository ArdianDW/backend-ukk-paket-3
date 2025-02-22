from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views.petugas_view import petugas_login_view, petugas_list_view, petugas_detail_view, logout_view
from .views.pegawai_view import PegawaiListView, PegawaiDetailView, PegawaiDetailByPetugasView
from .views.jenis_view import JenisListView, JenisDetailView
from .views.ruang_view import RuangListView, RuangDetailView
from .views.dashboard_view import DashboardView
from .views.inventaris_view import InventarisListView, InventarisDetailView, InventarisBaikListView
from .views.level_view import LevelListView, LevelDetailView
from .views.transaksi_view import PeminjamanViewSet
from .views.peminjaman_view import PeminjamanListView, PeminjamanApprovalView
from .views.riwayat_view import RiwayatPeminjamanListView
from .views.aktivitas_view import AktivitasListView, AktivitasDetailView, AktivitasPendingView, AktivitasUserView
from .views.riwayat_aktivitas_view import RiwayatAktivitasListView, RiwayatAktivitasUserView
from .views.laporan_view import LaporanView
from .views.me_view import MeView
from .views.change_password_view import ChangePasswordView
from .views.export_laporan_view import ExportLaporanView
from .views.peminjaman_pegawai_view import PeminjamanPegawaiView, PeminjamanPengajuanListView
from .views.register_view import RegisterPegawaiView
from .views.peminjaman_approval_view import PeminjamanApprovalView
from .views.peminjaman_pending_view import PeminjamanPendingListView
from .views.peminjaman_user_view import PeminjamanUserListView
from .views.peminjaman_pengembalian_view import PeminjamanPengembalianView
from .views.laporan_peminjaman_pengembalian_view import LaporanPeminjamanPengembalianView
from .views.export_laporan_peminjaman_pengembalian_view import ExportLaporanPeminjamanPengembalianView

urlpatterns = [
    path('petugas/login/', petugas_login_view.as_view(), name='petugas-login'),
    path('petugas/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('petugas/logout/', logout_view.as_view(), name='petugas-logout'),
    path('petugas/', petugas_list_view.as_view(), name='petugas-list'),
    path('petugas/<int:pk>/', petugas_detail_view.as_view(), name='petugas-detail'),
    path('pegawai/', PegawaiListView.as_view(), name='pegawai-list'),
    path('pegawai/<int:pk>/', PegawaiDetailView.as_view(), name='pegawai-detail'),
    path('pegawai/petugas/<str:petugas_id>/', PegawaiDetailByPetugasView.as_view(), name='pegawai-detail-by-petugas'),
    path('jenis/', JenisListView.as_view(), name='jenis-list'),
    path('jenis/<int:pk>/', JenisDetailView.as_view(), name='jenis-detail'),
    path('ruang/', RuangListView.as_view(), name='ruang-list'),
    path('ruang/<int:pk>/', RuangDetailView.as_view(), name='ruang-detail'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('inventaris/', InventarisListView.as_view(), name='inventaris-list'),
    path('inventaris/<int:pk>/', InventarisDetailView.as_view(), name='inventaris-detail'),
    path('inventaris/baik/', InventarisBaikListView.as_view(), name='inventaris-baik-list'),
    path('level/', LevelListView.as_view(), name='level-list'),
    path('level/<int:pk>/', LevelDetailView.as_view(), name='level-detail'),
    path('peminjaman/', PeminjamanViewSet.as_view({'get': 'list', 'post': 'create'}), name='peminjaman-list'),
    path('peminjaman/<int:pk>/', PeminjamanViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='peminjaman-detail'),
    path('peminjaman/active/', PeminjamanListView.as_view(), name='peminjaman-active'),
    path('peminjaman/approve/<int:pk>/', PeminjamanApprovalView.as_view(), name='peminjaman-approve'),
    path('aktivitas/', AktivitasListView.as_view(), name='aktivitas-list'),
    path('aktivitas/pending/', AktivitasPendingView.as_view(), name='aktivitas-pending'),
    path('aktivitas/<int:pk>/', AktivitasDetailView.as_view(), name='aktivitas-detail'),
    path('aktivitas/user/<int:user_id>/', AktivitasUserView.as_view(), name='aktivitas-user'),
    path('riwayat/', RiwayatPeminjamanListView.as_view(), name='riwayat-list'),
    path('riwayat-aktivitas/', RiwayatAktivitasListView.as_view(), name='riwayat-aktivitas-list'),
    path('riwayat-aktivitas/user/<int:user_id>/', RiwayatAktivitasUserView.as_view(), name='riwayat-aktivitas-user'),
    path('laporan/', LaporanView.as_view(), name='laporan'),
    path('laporan/export/', ExportLaporanView.as_view(), name='export-laporan'),
    path('me/', MeView.as_view(), name='me'),
    path('me/change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('peminjaman/pegawai/', PeminjamanPegawaiView.as_view(), name='peminjaman-pegawai-create'),
    path('peminjaman/pegawai/<int:pk>/', PeminjamanPegawaiView.as_view(), name='peminjaman-pegawai'),
    path('register/pegawai/', RegisterPegawaiView.as_view(), name='register-pegawai'),
    path('peminjaman/pengajuan/', PeminjamanPengajuanListView.as_view(), name='peminjaman-pengajuan-list'),
    path('peminjaman/pending/', PeminjamanPendingListView.as_view(), name='peminjaman-pending-list'),
    path('peminjaman/user/<int:user_id>/', PeminjamanUserListView.as_view(), name='peminjaman-user-list'),
    path('peminjaman/pengembalian/<int:pk>/', PeminjamanPengembalianView.as_view(), name='peminjaman-pengembalian'),
    path('laporan/peminjaman-pengembalian/', LaporanPeminjamanPengembalianView.as_view(), name='laporan-peminjaman-pengembalian'),
    path('laporan/export-peminjaman-pengembalian/', ExportLaporanPeminjamanPengembalianView.as_view(), name='export-laporan-peminjaman-pengembalian'),
]