# -*- coding: utf-8 -*-
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from django.http import FileResponse, Http404
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth import login # Importante para o cadastro
from django.shortcuts import redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import UserUpdateForm, PerfilUpdateForm
from django.db.models import Q
from .models import Perfil

# Seus Imports Locais
from livro.models import Livro, Review
from livro.forms import FormularioLivro, FormularioReview, FormularioCadastro
from livro.serializers import SerializadorLivro, SerializadorReview

# Rest Framework Imports
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import permissions

# --- VIEWS DE LIVRO ---

class Listarlivros(LoginRequiredMixin, ListView):
    model = Livro
    context_object_name = 'listar_livro'
    template_name = 'livro/listar.html'

    def get_queryset(self):
        # Pega todos os livros inicialmente
        queryset = super().get_queryset()
        
        # Pega o termo que o usuário digitou na barra de busca
        termo_busca = self.request.GET.get('busca')
        
        if termo_busca:
            # Filtra onde o Título contém o termo OU o Ano contém o termo
            # icontains = Case Insensitive (ignora maiúsculas/minúsculas)
            queryset = queryset.filter(
                Q(titulo__icontains=termo_busca) | 
                Q(ano__icontains=termo_busca)
            )
            
        return queryset
    
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
        
class EditarLivro(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Livro
    form_class = FormularioLivro
    template_name = 'livro/editar.html'
    success_url = reverse_lazy('listar_livro')

    # SEGURANÇA: Só retorna True se for Admin
    def test_func(self):
        return self.request.user.is_superuser

class DeletarLivro(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Livro
    template_name = 'livro/deletar.html'
    success_url = reverse_lazy('listar_livro')

    # SEGURANÇA: Só retorna True se for Admin
    def test_func(self):
        return self.request.user.is_superuser
class APIListarLivros(ListAPIView):
    serializer_class = SerializadorLivro
    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        return Livro.objects.all()

class LivroViewSet(ModelViewSet):
    queryset = Livro.objects.all()
    serializer_class = SerializadorLivro
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.select_related('livro', 'usuario').all()
    serializer_class = SerializadorReview
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)

    @action(detail=False, methods=['get'])
    def meus(self, request):
        qs = Review.objects.filter(usuario=request.user).order_by('-data_criacao')
        return Response(SerializadorReview(qs, many=True).data)

class CadastroUsuario(CreateView):
    template_name = 'livro/cadastro_usuario.html'
    form_class = FormularioCadastro
    success_url = reverse_lazy('listar_livro')

    def form_valid(self, form):
        print(">>> SUCESSO! Salvando usuário...")
        valid = super().form_valid(form)
        login(self.request, self.object)
        return valid

    # ADICIONE ISSO AQUI PARA DESCOBRIR O ERRO:
    def form_invalid(self, form):
        print(">>> ERRO: O formulário é inválido!")
        print(form.errors) # Isso vai mostrar no terminal o porquê
        return super().form_invalid(form)

class CriarReview(LoginRequiredMixin, CreateView):
    model = Review
    form_class = FormularioReview
    template_name = 'livro/novo_review.html'
    success_url = reverse_lazy('listar_livro')

    def get_initial(self):
        # 1. Pega os dados iniciais padrão do formulário
        initial = super().get_initial()
        
        # 2. Tenta pegar o parâmetro 'livro' da URL (ex: ?livro=5)
        livro_id = self.request.GET.get('livro')
        
        # 3. Se existir um ID na URL, define ele como valor inicial do campo 'livro'
        if livro_id:
            initial['livro'] = livro_id
            
        return initial

    def form_valid(self, form):
        # Vincula o review ao usuário logado antes de salvar
        form.instance.usuario = self.request.user
        return super().form_valid(form)
    

class MeusReviews(LoginRequiredMixin, ListView):
    model = Review
    context_object_name = 'reviews'
    template_name = 'livro/meus_reviews.html'

    def get_queryset(self):
        # O PULO DO GATO: Filtra apenas os reviews do usuário logado
        return Review.objects.filter(usuario=self.request.user).order_by('-data_criacao')
    
class EditarReview(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Review
    form_class = FormularioReview
    template_name = 'livro/editar_review.html'
    success_url = reverse_lazy('meus_reviews') # Volta para a lista de reviews do usuário

    # Essa função garante que só o dono pode editar
    def test_func(self):
        review = self.get_object() # Pega o review que está tentando editar
        return self.request.user == review.usuario # Retorna True se for o dono
    

class DeletarReview(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Review
    template_name = 'livro/deletar_review.html'
    success_url = reverse_lazy('meus_reviews')

    # Segurança: Só o dono deleta
    def test_func(self):
        review = self.get_object()
        return self.request.user == review.usuario
    
class MeuPerfil(LoginRequiredMixin, View):
    template_name = 'livro/perfil.html'

    def get(self, request):
        # SEGURANÇA: Se o perfil não existir (usuário antigo), cria agora.
        perfil, created = Perfil.objects.get_or_create(usuario=request.user)

        u_form = UserUpdateForm(instance=request.user)
        p_form = PerfilUpdateForm(instance=perfil) # Usa a variável 'perfil' segura
        
        context = {
            'u_form': u_form,
            'p_form': p_form
        }
        return render(request, self.template_name, context)

    def post(self, request):
        # SEGURANÇA: Garante que o perfil existe antes de salvar
        perfil, created = Perfil.objects.get_or_create(usuario=request.user)

        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = PerfilUpdateForm(request.POST, instance=perfil)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect('meu_perfil')

        context = {'u_form': u_form, 'p_form': p_form}
        return render(request, self.template_name, context)