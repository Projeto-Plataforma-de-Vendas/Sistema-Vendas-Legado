from django.urls import path
from . import views

app_name = 'suppliers'

urlpatterns = [
    path('', views.FornecedorListView.as_view(), name='list'),
    path('novo/', views.FornecedorCreateView.as_view(), name='create'),
    path('editar/<int:pk>/', views.FornecedorUpdateView.as_view(), name='update'),
    path('excluir/<int:pk>/', views.FornecedorDeleteView.as_view(), name='delete'),
]
