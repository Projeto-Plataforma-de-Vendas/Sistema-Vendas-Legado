from django.urls import path
from . import views

app_name = 'customers'

urlpatterns = [
    path('', views.ClienteListView.as_view(), name='list'),
    path('novo/', views.ClienteCreateView.as_view(), name='create'),
    path('editar/<int:pk>/', views.ClienteUpdateView.as_view(), name='update'),
    path('excluir/<int:pk>/', views.ClienteDeleteView.as_view(), name='delete'),
    path('buscar-cep/', views.BuscarCepView.as_view(), name='buscar_cep'),
]
