from django.forms import ModelForm
from livro.models import Livro

class FormularioLivro(ModelForm):
    class Meta:
        model = Livro
        exclude = []
        