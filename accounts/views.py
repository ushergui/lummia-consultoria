# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from .forms import CustomUserCreationForm

class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    # Redireciona para o dashboard após o login bem-sucedido
    default_redirect_url = '/dashboard/' 
    
    def get_success_url(self):
        return self.default_redirect_url

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Loga o usuário automaticamente após o registro
            login(request, user)
            return redirect('dashboard')
    else:
        form = CustomUserCreationForm()
    
    context = {'form': form}
    return render(request, 'accounts/register.html', context)

class CustomLogoutView(LogoutView):
    # Redireciona para a página inicial após o logout
    next_page = '/'

@login_required
def dashboard_view(request):
    """
    Página principal que o usuário vê após o login.
    """
    context = {}
    return render(request, 'dashboard.html', context)
