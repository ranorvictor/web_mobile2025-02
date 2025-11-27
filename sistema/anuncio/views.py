# -*- coding: utf-8 -*-
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from anuncio.forms import FormularioAnuncio
from anuncio.models import Anuncio
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

class ListarAnuncio(LoginRequiredMixin, ListView):
    """
    View para listar anuncios cadastrados.
    """
    model = Anuncio
    context_object_name = 'listar_anuncio'
    template_name = 'anuncio/listar.html'

    def get_queryset(self):
        return Anuncio.objects.all()
    
class CriarAnuncio(LoginRequiredMixin, CreateView):
    model = Anuncio
    form_class = FormularioAnuncio
    template_name = 'anuncio/novo.html'
    success_url = reverse_lazy('listar_anuncio')

    def form_valid(self, form):
        # Define o usuário logado como o criador do anúncio
        form.instance.usuario = self.request.user
        return super().form_valid(form)

    def form_invalid(self, form):
        # Exibe os erros do formulário no terminal para depuração
        print(form.errors)
        return super().form_invalid(form)
        
class EditarAnuncio(LoginRequiredMixin, UpdateView):

    model = Anuncio
    form_class = FormularioAnuncio
    template_name = 'anuncio/editar.html'
    success_url = reverse_lazy('listar_anuncio')

class DeletarAnuncio(LoginRequiredMixin, DeleteView):

    model = Anuncio
    template_name = 'anuncio/deletar.html'
    success_url = reverse_lazy('listar_anuncio')