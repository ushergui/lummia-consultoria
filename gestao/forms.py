# gestao/forms.py
from django import forms
from accounts.models import CustomUser
from .models import Empresa

# --- Formulários para o Admin da Plataforma ---

class EmpresaForm(forms.ModelForm):
    class Meta:
        model = Empresa
        fields = ['nome', 'cnpj']

class AdminCriaUsuarioForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        # O admin pode definir o perfil e a empresa
        fields = ['username', 'first_name', 'last_name', 'email', 'tipo_perfil', 'empresa', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

class AdminEditaUsuarioForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        # O admin pode editar o perfil e a empresa
        fields = ['username', 'first_name', 'last_name', 'email', 'tipo_perfil', 'empresa', 'is_active']


# --- Formulários para o Admin Cliente (já existentes) ---

class AdicionarUsuarioForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

class EditarUsuarioForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email']
