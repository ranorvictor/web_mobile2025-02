from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm # Já vem pronto do Django
from django.contrib.auth.models import User
from livro.models import Livro, Review, Perfil
class FormularioLivro(ModelForm):
    class Meta:
        model = Livro
        exclude = []
        widgets = {
            'sinopse': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

class FormularioReview(ModelForm):
    class Meta:
        model = Review
        fields = ['livro', 'nota', 'texto']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
 
class FormularioCadastro(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email'] # Deixamos username de fora por segurança

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

class PerfilUpdateForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ['icone', 'bio']
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            # O campo icone vamos manipular no HTML para ser visual
        }