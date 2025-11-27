# -*- coding: utf-8 -*-
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View
from django.shortcuts import render, redirect
from rest_framework.authtoken.views import ObtainAuthToken as obtainAuthToken
from rest_framework.authtoken.models import Token   
from rest_framework.response import Response
from livro.models import Perfil

class Login(View):

    def get(self, request):
        contexto = {}
        if request.user.is_authenticated:
            return redirect('listar_livro') 
        else:
            return render(request, 'autenticacao.html', contexto)
    
    def post(self, request):
        usuario = request.POST.get('usuario', None)
        senha = request.POST.get('senha', None)

        user = authenticate(request, username=usuario, password=senha)
        
        if user is not None:
            if user.is_active:
                login(request, user)
                
                try:
                    p = user.perfil
                except Perfil.DoesNotExist: 
                    Perfil.objects.create(usuario=user)
                # ---------------------

                return redirect('listar_livro') 
        
        return render(request, 'autenticacao.html', {'mensagem' : "Usuário ou senha incorretos!"})
class Logout(View):

    def get(self, request):
        logout(request)
        return redirect('/')
    
class LoginAPI(obtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data,
            context={'request': request}
        )

        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'id' : user.id,
            'nome': user.first_name,
            'email': user.email,
            'token': token.key
        })