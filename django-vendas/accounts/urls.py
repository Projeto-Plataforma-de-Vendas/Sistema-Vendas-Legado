from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.FuncionarioListView.as_view(), name='list'),
    path('novo/', views.FuncionarioCreateView.as_view(), name='create'),
    path('editar/<int:pk>/', views.FuncionarioUpdateView.as_view(), name='update'),
    path('excluir/<int:pk>/', views.FuncionarioDeleteView.as_view(), name='delete'),
]
