# ferramentas/views.py
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from gestao.models import Ferramenta

@login_required
def ferramenta_view(request, ferramenta_slug):
    """
    View genérica que carrega qualquer ferramenta com base no seu 'slug'.
    """
    # 1. Pega a ferramenta do banco de dados pelo slug da URL
    ferramenta = get_object_or_404(Ferramenta, slug=ferramenta_slug)
    
    # 2. Verifica se o usuário tem uma empresa associada
    if not request.user.empresa:
        raise PermissionDenied("Este usuário não está associado a nenhuma empresa.")

    # 3. Verifica se a empresa do usuário contratou esta ferramenta
    if ferramenta not in request.user.empresa.ferramentas_contratadas.all():
        raise PermissionDenied("Sua empresa não tem acesso a esta ferramenta.")

    # 4. Define o nome do template a ser renderizado com base no slug
    # Ex: Se o slug for 'dimensionamento-enfermagem', ele procurará o arquivo 'dimensionamento-enfermagem.html'
    template_name = f'ferramentas/{ferramenta_slug}.html'
    
    # Se passou por todas as verificações, renderiza a página da ferramenta
    return render(request, template_name)
