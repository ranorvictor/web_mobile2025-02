from rest_framework import serializers
from livro.models import Livro, Review

class SerializadorLivro(serializers.ModelSerializer):
    """
    Serializador para o modelo Livro
    """
    class Meta:
        model = Livro
        exclude = []


class SerializadorReview(serializers.ModelSerializer):
    usuario = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = [
            'id', 'livro', 'usuario', 'nota', 'texto', 'data_criacao'
        ]