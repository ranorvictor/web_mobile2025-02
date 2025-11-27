from django.urls import path
from livro.views import *

urlpatterns = [
    path('', Listarlivros.as_view(), name = 'listar_livro'),
    path('novo', CriarLivro.as_view(), name = 'criar_livro'),
    path('editar/<int:pk>', EditarLivro.as_view(), name = 'editar_livro'),
    path('deletar/<int:pk>', DeletarLivro.as_view(), name = 'deletar_livro'),
    path('fotos/<str:arquivo>/', LivroFoto.as_view(), name='foto_livro'),
    path('api/', APIListarLivros.as_view(), name='api-listar-livro'),
    path('avaliar/', CriarReview.as_view(), name='criar_review'),
    path('meus-reviews/', MeusReviews.as_view(), name='meus_reviews'),
    path('review/editar/<int:pk>/', EditarReview.as_view(), name='editar_review'),
    path('review/deletar/<int:pk>/', DeletarReview.as_view(), name='deletar_review'),
    path('perfil/', MeuPerfil.as_view(), name='meu_perfil'),
]