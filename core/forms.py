# core/forms.py
from django import forms
from .models import Noticia

class NoticiaForm(forms.ModelForm):
    class Meta:
        model = Noticia
        fields = ['titulo', 'conteudo', 'imagem']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título da notícia'}),
            'conteudo': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Escreva o conteúdo aqui...'}),
            'imagem': forms.FileInput(attrs={'class': 'form-control'}),
        }
