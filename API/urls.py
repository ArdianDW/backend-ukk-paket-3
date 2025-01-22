from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views.petugas_view import petugas_login_view, petugas_list_view, petugas_detail_view, logout_view
from .views.pegawai_view import PegawaiListView, PegawaiDetailView
from .views.jenis_view import JenisListView, JenisDetailView
from .views.ruang_view import RuangListView, RuangDetailView

urlpatterns = [
    path('petugas/login/', petugas_login_view.as_view(), name='petugas-login'),
    path('petugas/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('petugas/logout/', logout_view.as_view(), name='petugas-logout'),
    path('petugas/', petugas_list_view.as_view(), name='petugas-list'),
    path('petugas/<int:pk>/', petugas_detail_view.as_view(), name='petugas-detail'),
    path('pegawai/', PegawaiListView.as_view(), name='pegawai-list'),
    path('pegawai/<int:pk>/', PegawaiDetailView.as_view(), name='pegawai-detail'),
    path('jenis/', JenisListView.as_view(), name='jenis-list'),
    path('jenis/<int:pk>/', JenisDetailView.as_view(), name='jenis-detail'),
    path('ruang/', RuangListView.as_view(), name='ruang-list'),
    path('ruang/<int:pk>/', RuangDetailView.as_view(), name='ruang-detail'),
]