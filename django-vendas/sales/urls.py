from django.urls import path
from . import views

app_name = 'sales'

urlpatterns = [
    path('', views.VendaListView.as_view(), name='list'),
    path('nova/', views.VendaCreateView.as_view(), name='create'),
    path('detalhes/<int:pk>/', views.VendaDetailView.as_view(), name='detail'),
    path('excluir/<int:pk>/', views.VendaDeleteView.as_view(), name='delete'),
    path('total/', views.TotalVendaView.as_view(), name='total'),
]
