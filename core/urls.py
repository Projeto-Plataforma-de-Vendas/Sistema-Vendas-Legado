from django.urls import path
from . import views
from accounts import views as accounts_views

app_name = 'core'

urlpatterns = [
    path('', accounts_views.register, name='register'), #rota inicial
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
]
