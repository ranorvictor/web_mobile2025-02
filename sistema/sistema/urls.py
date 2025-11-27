
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from sistema.views import Login, Logout, LoginAPI
from livro.views import CadastroUsuario

urlpatterns = [
    path('admin/', admin.site.urls),
    path('logout/', Logout.as_view(), name='logout'),
    path('', Login.as_view(), name='login'),
    path('cadastro/', CadastroUsuario.as_view(), name='cadastro_usuario'),
    path('livro/', include('livro.urls'), name='livro'),
    path('autenticacao-api/', LoginAPI.as_view()),
]

# Servir arquivos estáticos e de mídia em desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
