from django.forms import ModelForm
from anuncio.models import Anuncio

class FormularioAnuncio(ModelForm):
    class Meta:
        model = Anuncio
        exclude = []
        