from django.db import models
from livro.models import Livro
from django.contrib.auth.models import User

class Anuncio(models.Model):

    data = models.DateTimeField(auto_now_add=True)
    descricao = models.CharField(max_length=200)
    preco = models.DecimalField(decimal_places=2, max_digits=10)

    livro = models.ForeignKey(Livro , related_name="anuncio", on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, related_name="anuncio_realizado", on_delete=models.CASCADE)



