from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from livro.consts import OPCOES_GENERO, OPCOES_AUTORES, OPCOES_EDITORAS, OPCOES_ICONES
from django.db.models.signals import post_save
from django.dispatch import receiver

class Livro(models.Model):
    genero = models.SmallIntegerField(choices=OPCOES_GENERO)
    titulo = models.CharField(max_length=200)
    sinopse = models.TextField(max_length=1500, blank=True, verbose_name="Sinopse")
    ano = models.IntegerField()
    autor = models.SmallIntegerField(choices=OPCOES_AUTORES)
    editora = models.SmallIntegerField(choices=OPCOES_EDITORAS)
    foto = models.ImageField(upload_to='livro/fotos/', blank=True, null=True)

    def __str__(self):
        return self.titulo
    
    @property
    def livro_novo(self):
      return self.ano == datetime.now().year

    def anos_de_uso(self):
        return datetime.now().year - self.ano
    
class Review(models.Model):
    livro = models.ForeignKey(Livro, on_delete=models.CASCADE, related_name='reviews')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    nota = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    texto = models.TextField()
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.livro.titulo} - {self.nota}"
    
class Perfil(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    icone = models.CharField(max_length=50, choices=OPCOES_ICONES, default='avatar1.png')
    bio = models.TextField(max_length=500, blank=True, verbose_name="Sobre mim")

    def __str__(self):
        return f"Perfil de {self.usuario.username}"


@receiver(post_save, sender=User)
def criar_perfil(sender, instance, created, **kwargs):
    if created:
        Perfil.objects.create(usuario=instance)

@receiver(post_save, sender=User)
def salvar_perfil(sender, instance, **kwargs):
    try:
        perfil = instance.perfil
    except Perfil.DoesNotExist:
        perfil = Perfil.objects.create(usuario=instance)
    perfil.save()