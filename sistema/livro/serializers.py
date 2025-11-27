from rest_framework import serializers
from livro.models import Livro

class SerializadorLivro(serializers.ModelSerializer):
    """
    Serializador para o modelo Livro
    """
    class Meta:
        model = Livro
        exclude = []