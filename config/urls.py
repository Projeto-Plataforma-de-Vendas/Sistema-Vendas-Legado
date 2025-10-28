from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),

    # Rota inicial: registro de usuário
    path('', RedirectView.as_view(pattern_name='accounts:register', permanent=False)),

    # URLs dos apps
    path('accounts/', include('accounts.urls')),
    path('core/', include('core.urls')), 
    path('clientes/', include('customers.urls')),
    path('fornecedores/', include('suppliers.urls')),
    path('produtos/', include('inventory.urls')),
    path('vendas/', include('sales.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Admin customization
admin.site.site_header = "Sistema de Vendas - Administração"
admin.site.site_title = "Sistema de Vendas"
admin.site.index_title = "Painel de Controle"
