from django.urls import path
from . import views

app_name = 'inventory'

urlpatterns = [
    path('', views.ProdutoListView.as_view(), name='list'),
    path('novo/', views.ProdutoCreateView.as_view(), name='create'),
    path('editar/<int:pk>/', views.ProdutoUpdateView.as_view(), name='update'),
    path('excluir/<int:pk>/', views.ProdutoDeleteView.as_view(), name='delete'),
    path('estoque/', views.EstoqueListView.as_view(), name='estoque'),
]
