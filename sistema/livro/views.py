# -*- coding: utf-8 -*-
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from livro.forms import FormularioLivro
from livro.models import Livro
from django.views.generic import View
from django.http import FileResponse, Http404
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from livro.serializers import SerializadorLivro
from rest_framework.generics import ListAPIView
from rest_framework.authentication import TokenAuthentication
from rest_framework import permissions 

class Listarlivros(LoginRequiredMixin, ListView):
    """
    View para listar livros cadastrados.
    """
    model = Livro
    context_object_name = 'listar_livro'
    template_name = 'livro/listar.html'

    def get_queryset(self):
        return Livro.objects.all()
    
class CriarLivro(LoginRequiredMixin, CreateView):

    model = Livro
    form_class = FormularioLivro
    template_name = 'livro/novo.html'
    success_url = reverse_lazy('listar_livro')

class LivroFoto(View):

    def get(self, request, arquivo):
        try:
            livro = Livro.objects.get(foto='livro/fotos/{}'.format(arquivo))
            return FileResponse(livro.foto)
        except ObjectDoesNotExist:
            raise Http404("Foto não encontrada ou acesso não permitido.")
        except Exception as exception:
            raise exception
        
class EditarLivro(LoginRequiredMixin, UpdateView):

    model = Livro
    form_class = FormularioLivro
    template_name = 'livro/editar.html'
    success_url = reverse_lazy('listar_livro')

class DeletarLivro(LoginRequiredMixin, DeleteView):

    model = Livro
    template_name = 'livro/deletar.html'
    success_url = reverse_lazy('listar_livro')

class APIListarLivros(ListAPIView):

    serializer_class = SerializadorLivro
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Livro.objects.all()