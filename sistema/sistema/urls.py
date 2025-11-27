
from django.contrib import admin
from django.urls import path, include
from sistema.views import Login, Logout, LoginAPI

urlpatterns = [
    path('admin/', admin.site.urls),
    path('logout/', Logout.as_view(), name='logout'),
    path('', Login.as_view(), name='login'),
    path('livro/', include('livro.urls'), name='livro'),
    path('anuncio/', include('anuncio.urls'), name='anuncio'),
    path('autenticacao-api/', LoginAPI.as_view()),
]
