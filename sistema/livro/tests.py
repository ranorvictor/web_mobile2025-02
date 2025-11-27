from django.test import TestCase
from django.contrib.auth.models import User
from datetime import datetime
from .models import Livro, Review, Perfil

class LivroModelTest(TestCase):
    
    def setUp(self):
        self.ano_atual = datetime.now().year
        self.livro = Livro.objects.create(
            titulo="Livro de Teste",
            genero=1,
            ano=self.ano_atual,
            autor=1,
            editora=1,
            sinopse="Uma sinopse de teste."
        )

    def test_livro_criacao(self):
        """Testa se o livro foi criado corretamente"""
        self.assertEqual(self.livro.titulo, "Livro de Teste")
        self.assertEqual(self.livro.sinopse, "Uma sinopse de teste.")

    def test_string_representation(self):
        """Testa se o __str__ retorna o título"""
        self.assertEqual(str(self.livro), "Livro de Teste")

    def test_metodo_livro_novo_verdadeiro(self):
        """Testa se a property livro_novo retorna True para ano atual"""
        self.assertTrue(self.livro.livro_novo)

    def test_metodo_livro_novo_falso(self):
        """Testa se a property livro_novo retorna False para ano antigo"""
        livro_velho = Livro.objects.create(
            titulo="Livro Velho",
            genero=1,
            ano=1990,
            autor=1,
            editora=1
        )
        self.assertFalse(livro_velho.livro_novo)

    def test_metodo_anos_de_uso(self):
        """Testa o cálculo de anos de uso"""
        livro_velho = Livro.objects.create(
            titulo="Livro Velho",
            genero=1,
            ano=2000,
            autor=1,
            editora=1
        )
        esperado = self.ano_atual - 2000
        self.assertEqual(livro_velho.anos_de_uso(), esperado)


class ReviewModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='leitor', password='123')
        self.livro = Livro.objects.create(
            titulo="Dom Casmurro",
            genero=1, ano=1899, autor=1, editora=1
        )
        self.review = Review.objects.create(
            livro=self.livro,
            usuario=self.user,
            nota=5,
            texto="Excelente!"
        )

    def test_review_criacao(self):
        """Testa se o review liga o usuário ao livro certo"""
        self.assertEqual(self.review.nota, 5)
        self.assertEqual(self.review.usuario.username, 'leitor')

    def test_string_representation(self):
        """Testa se o __str__ retorna 'Titulo - Nota'"""
        esperado = "Dom Casmurro - 5"
        self.assertEqual(str(self.review), esperado)


class PerfilSignalTest(TestCase):
    
    def test_criar_perfil_automaticamente(self):
        """
        O teste mais importante: Verifica se o SINAL (post_save)
        criou o perfil sozinho ao criar um User.
        """
        novo_usuario = User.objects.create_user(username='novato', password='123')
        
        existe_perfil = Perfil.objects.filter(usuario=novo_usuario).exists()
        self.assertTrue(existe_perfil)
        
    def test_perfil_padrao(self):
        """Verifica se o perfil nasce com o ícone padrão"""
        novo_usuario = User.objects.create_user(username='padrao', password='123')
        self.assertEqual(novo_usuario.perfil.icone, 'avatar1.jpg')