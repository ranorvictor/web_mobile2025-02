from django.urls import path
from anuncio.views import *

urlpatterns = [

    path('', ListarAnuncio.as_view(), name = 'listar_anuncio'),
    path('novo', CriarAnuncio.as_view(), name = 'criar_anuncio'),
    path('editar/<int:pk>', EditarAnuncio.as_view(), name = 'editar_anuncio'),
    path('deletar/<int:pk>', DeletarAnuncio.as_view(), name = 'deletar_anuncio'),

]