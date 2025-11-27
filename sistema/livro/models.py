from datetime import datetime
from django.db import models
from livro.consts import OPCOES_GENERO, OPCOES_AUTORES, OPCOES_EDITORAS

# Create your models here.
class Livro(models.Model):
    genero = models.SmallIntegerField(choices=OPCOES_GENERO)
    titulo = models.CharField(max_length=200)
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