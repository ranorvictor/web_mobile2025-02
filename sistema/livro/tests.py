# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse
from datetime import datetime
from livro.models import *
from livro.forms import *

class TestesModelLivro(TestCase):

    def setUp(self):
        self.instancia = Livro(
            genero=1,
            titulo="Teste de Livro",
            ano=datetime.now().year,
            autor=1,
            editora=1
        )

    def test_livro_novo(self):
        self.assertTrue(self.instancia.livro_novo)
        self.instancia.ano = datetime.now().year - 1
        self.assertFalse(self.instancia.livro_novo)

    def test_anos_de_uso(self):
        self.instancia.ano = datetime.now().year - 10
        self.assertEqual(self.instancia.anos_de_uso(), 10)

class TestesViewListarLivro(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_login(self.user)
        self.url = reverse('listar_livro')
        Livro(
            genero=1,
            titulo="Livro Teste 1",
            ano=2020,
            autor=1,
            editora=1
        )

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context.get('listar_livro')), 0)

class TestesViewCriarLivro(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_login(self.user)
        self.url = reverse('criar_livro')

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context.get('form'), FormularioLivro)

    def test_post(self):
        dados = {
            'genero': 1,
            'titulo': 'Livro Teste',
            'ano': 2021,
            'autor': 1,
            'editora': 1
        }
        response = self.client.post(self.url, dados)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('listar_livro'))
        self.assertEqual(Livro.objects.count(), 1)
        self.assertEqual(Livro.objects.first().titulo, 'Livro Teste')

class TestesViewEditarLivro(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_login(self.user)
        self.instancia = Livro(
            genero=1,
            titulo="Livro Teste 1",
            ano=2020,
            autor=1,
            editora=1
        )
        self.url = reverse('editar_livro', kwargs={'pk': self.instancia.pk})

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context.get('object'), Livro)
        self.assertIsInstance(response.context.get('form'), FormularioLivro)
        self.assertEqual(response.context.get('object').pk, self.instancia.pk)
        self.assertEqual(response.context.get('object').titulo, 'Livro Teste 1')

    def test_post(self):
        data = {
            'genero': 2,
            'titulo': 'Livro Teste Editado',
            'ano': 2021,
            'autor': 2,
            'editora': 2
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('listar_livro'))
        self.assertEqual(Livro.objects.count(), 1)
        self.assertEqual(Livro.objects.first().titulo, 'Livro Teste Editado')
        self.assertEqual(Livro.objects.first().pk, self.instancia.pk)

class TestesViewDeletarLivro(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_login(self.user)
        self.instancia = Livro(
            genero=1,
            titulo="Livro Teste 1",
            ano=2020,
            autor=1,
            editora=1
        )
        self.url = reverse('deletar_livro', kwargs={'pk': self.instancia.pk})

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('listar_livro'))
        self.assertEqual(Livro.objects.count(), 0)

    def test_post(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('listar_livro'))
        self.assertEqual(Livro.objects.count(), 0)