from django.urls import path
from livro.views import *

urlpatterns = [
    path('', Listarlivros.as_view(), name = 'listar_livro'),
    path('novo', CriarLivro.as_view(), name = 'criar_livro'),
    path('editar/<int:pk>', EditarLivro.as_view(), name = 'editar_livro'),
    path('deletar/<int:pk>', DeletarLivro.as_view(), name = 'deletar_livro'),
    path('fotos/<str:arquivo>/', LivroFoto.as_view(), name='foto_livro'),
    path('api/', APIListarLivros.as_view(), name='api-listar-livro'),
]