from django.urls import path
from . import views

app_name = 'inventory'

urlpatterns = [
    # Produtos
    path('', views.ProdutoListView.as_view(), name='list'),
    path('novo/', views.ProdutoCreateView.as_view(), name='create'),
    path('editar/<int:pk>/', views.ProdutoUpdateView.as_view(), name='update'),
    path('excluir/<int:pk>/', views.ProdutoDeleteView.as_view(), name='delete'),
    
    # Estoque
    path('estoque/', views.EstoqueListView.as_view(), name='estoque'),
    path('estoque/ajuste/', views.AjusteEstoqueView.as_view(), name='ajuste_estoque'),
    path('estoque/movimentacoes/', views.MovimentacaoEstoqueListView.as_view(), name='movimentacoes'),
]