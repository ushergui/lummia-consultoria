from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import JsonResponse, Http404
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView, DetailView
from .models import (
    Ala, AvaliacaoFugulin, Quarto, Leito, Paciente, AreaCorporal, 
    AreaEspecifica, AchadoClinico, DiagnosticoNANDA, ResultadoNOC, 
    IntervencaoNIC, AtividadeNIC, AvaliacaoSAE, PlanoCuidado, TipoExame,
)
from .forms import (
    AlaForm, QuartoForm, LeitoForm, PacienteForm, 
    AvaliacaoFugulinForm, AvaliacaoSAEForm, TipoExameForm, AreaEspecificaForm, AreaCorporalForm, AchadoClinicoForm, DiagnosticoNANDAForm, ResultadoNOCForm, IntervencaoNICForm, AtividadeNICFormSet
)
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.utils import timezone
import json
from django.db import transaction
from django.views.decorators.csrf import csrf_exempt
# Este Mixin agora serve apenas para verificar a permissão do usuário.

class AdministradorRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """ Garante que o usuário logado é o Administrador da plataforma. """
    def test_func(self):
        return self.request.user.tipo_perfil == 'ADMINISTRADOR'

class AdminClienteRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.tipo_perfil in ['ADMIN_CLIENTE', 'ADMINISTRADOR']
    

class IntervencaoNICListView(AdminClienteRequiredMixin, ListView):
    model = IntervencaoNIC
    template_name = 'gestao_hospitalar/nic_list.html'
    context_object_name = 'intervencoes_nic'
    def get_queryset(self):
        return IntervencaoNIC.objects.filter(empresa=self.request.user.empresa)

class IntervencaoNICCreateView(AdminClienteRequiredMixin, CreateView):
    model = IntervencaoNIC
    form_class = IntervencaoNICForm
    template_name = 'gestao_hospitalar/nic_form.html'
    success_url = reverse_lazy('gestao_hospitalar:nic_list')
    
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['atividades_formset'] = AtividadeNICFormSet(self.request.POST)
        else:
            data['atividades_formset'] = AtividadeNICFormSet()
        data['titulo'] = "Adicionar Nova Intervenção (NIC)"
        data['cancel_url'] = reverse_lazy('gestao_hospitalar:nic_list')
        return data

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs(); kwargs['empresa'] = self.request.user.empresa; return kwargs

    def form_valid(self, form):
        context = self.get_context_data()
        atividades_formset = context['atividades_formset']
        with transaction.atomic():
            form.instance.empresa = self.request.user.empresa
            self.object = form.save()
            if atividades_formset.is_valid():
                atividades_formset.instance = self.object
                atividades_formset.save()
        return super().form_valid(form)

class IntervencaoNICUpdateView(AdminClienteRequiredMixin, UpdateView):
    model = IntervencaoNIC
    form_class = IntervencaoNICForm
    template_name = 'gestao_hospitalar/nic_form.html'
    success_url = reverse_lazy('gestao_hospitalar:nic_list')

    def get_queryset(self):
        return IntervencaoNIC.objects.filter(empresa=self.request.user.empresa)
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs(); kwargs['empresa'] = self.request.user.empresa; return kwargs

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['atividades_formset'] = AtividadeNICFormSet(self.request.POST, instance=self.object)
        else:
            data['atividades_formset'] = AtividadeNICFormSet(instance=self.object)
        data['titulo'] = "Editar Intervenção (NIC)"
        data['cancel_url'] = reverse_lazy('gestao_hospitalar:nic_list')
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        atividades_formset = context['atividades_formset']
        if atividades_formset.is_valid():
            with transaction.atomic():
                self.object = form.save()
                atividades_formset.instance = self.object
                atividades_formset.save()
            return super().form_valid(form)
        else:
            return self.form_invalid(form)

class IntervencaoNICDeleteView(AdminClienteRequiredMixin, DeleteView):
    model = IntervencaoNIC
    template_name = 'gestao_hospitalar/confirm_delete_template.html'
    success_url = reverse_lazy('gestao_hospitalar:nic_list')
    def get_queryset(self):
        return IntervencaoNIC.objects.filter(empresa=self.request.user.empresa)
    
class ResultadoNOCListView(AdminClienteRequiredMixin, ListView):
    model = ResultadoNOC
    template_name = 'gestao_hospitalar/noc_list.html'
    context_object_name = 'resultados_noc'
    def get_queryset(self):
        return ResultadoNOC.objects.filter(empresa=self.request.user.empresa)

class ResultadoNOCCreateView(AdminClienteRequiredMixin, CreateView):
    model = ResultadoNOC
    form_class = ResultadoNOCForm
    template_name = 'gestao_hospitalar/form_template.html'
    success_url = reverse_lazy('gestao_hospitalar:noc_list')
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs(); kwargs['empresa'] = self.request.user.empresa; return kwargs
    def form_valid(self, form):
        form.instance.empresa = self.request.user.empresa
        return super().form_valid(form)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Adicionar Novo Resultado (NOC)"
        context['cancel_url'] = reverse_lazy('gestao_hospitalar:noc_list')
        return context

class ResultadoNOCUpdateView(AdminClienteRequiredMixin, UpdateView):
    model = ResultadoNOC
    form_class = ResultadoNOCForm
    template_name = 'gestao_hospitalar/form_template.html'
    success_url = reverse_lazy('gestao_hospitalar:noc_list')
    def get_queryset(self):
        return ResultadoNOC.objects.filter(empresa=self.request.user.empresa)
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs(); kwargs['empresa'] = self.request.user.empresa; return kwargs
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Editar Resultado (NOC)"
        context['cancel_url'] = reverse_lazy('gestao_hospitalar:noc_list')
        return context

class ResultadoNOCDeleteView(AdminClienteRequiredMixin, DeleteView):
    model = ResultadoNOC
    template_name = 'gestao_hospitalar/confirm_delete_template.html'
    success_url = reverse_lazy('gestao_hospitalar:noc_list')
    def get_queryset(self):
        return ResultadoNOC.objects.filter(empresa=self.request.user.empresa)

class DiagnosticoNANDAListView(AdminClienteRequiredMixin, ListView):
    model = DiagnosticoNANDA
    template_name = 'gestao_hospitalar/nanda_list.html'
    context_object_name = 'diagnosticos'
    def get_queryset(self):
        return DiagnosticoNANDA.objects.filter(empresa=self.request.user.empresa)

class DiagnosticoNANDACreateView(AdminClienteRequiredMixin, CreateView):
    model = DiagnosticoNANDA
    form_class = DiagnosticoNANDAForm
    template_name = 'gestao_hospitalar/form_template.html'
    success_url = reverse_lazy('gestao_hospitalar:nanda_list')
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['empresa'] = self.request.user.empresa
        return kwargs
    def form_valid(self, form):
        form.instance.empresa = self.request.user.empresa
        return super().form_valid(form)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Adicionar Novo Diagnóstico (NANDA-I)"
        context['cancel_url'] = reverse_lazy('gestao_hospitalar:nanda_list')
        return context

class DiagnosticoNANDAUpdateView(AdminClienteRequiredMixin, UpdateView):
    model = DiagnosticoNANDA
    form_class = DiagnosticoNANDAForm
    template_name = 'gestao_hospitalar/form_template.html'
    success_url = reverse_lazy('gestao_hospitalar:nanda_list')
    def get_queryset(self):
        return DiagnosticoNANDA.objects.filter(empresa=self.request.user.empresa)
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['empresa'] = self.request.user.empresa
        return kwargs
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Editar Diagnóstico (NANDA-I)"
        context['cancel_url'] = reverse_lazy('gestao_hospitalar:nanda_list')
        return context

class DiagnosticoNANDADeleteView(AdminClienteRequiredMixin, DeleteView):
    model = DiagnosticoNANDA
    template_name = 'gestao_hospitalar/confirm_delete_template.html'
    success_url = reverse_lazy('gestao_hospitalar:nanda_list')
    def get_queryset(self):
        return DiagnosticoNANDA.objects.filter(empresa=self.request.user.empresa)    

class AchadoClinicoListView(AdminClienteRequiredMixin, ListView):
    model = AchadoClinico
    template_name = 'gestao_hospitalar/achado_clinico_list.html'
    context_object_name = 'achados_clinicos'

    def get_queryset(self):
        return AchadoClinico.objects.filter(empresa=self.request.user.empresa).select_related('area_especifica', 'tipo_exame')

class AchadoClinicoCreateView(AdminClienteRequiredMixin, CreateView):
    model = AchadoClinico
    form_class = AchadoClinicoForm
    template_name = 'gestao_hospitalar/form_template.html'
    success_url = reverse_lazy('gestao_hospitalar:achado_clinico_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['empresa'] = self.request.user.empresa
        return kwargs
    
    def form_valid(self, form):
        form.instance.empresa = self.request.user.empresa
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Adicionar Novo Achado Clínico"
        context['cancel_url'] = reverse_lazy('gestao_hospitalar:achado_clinico_list')
        return context

class AchadoClinicoUpdateView(AdminClienteRequiredMixin, UpdateView):
    model = AchadoClinico
    form_class = AchadoClinicoForm
    template_name = 'gestao_hospitalar/form_template.html'
    success_url = reverse_lazy('gestao_hospitalar:achado_clinico_list')
    
    def get_queryset(self):
        return AchadoClinico.objects.filter(empresa=self.request.user.empresa)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['empresa'] = self.request.user.empresa
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Editar Achado Clínico"
        context['cancel_url'] = reverse_lazy('gestao_hospitalar:achado_clinico_list')
        return context

class AchadoClinicoDeleteView(AdminClienteRequiredMixin, DeleteView):
    model = AchadoClinico
    template_name = 'gestao_hospitalar/confirm_delete_template.html'
    success_url = reverse_lazy('gestao_hospitalar:achado_clinico_list')
    
    def get_queryset(self):
        return AchadoClinico.objects.filter(empresa=self.request.user.empresa)



class AreaCorporalListView(AdministradorRequiredMixin, ListView):
    model = AreaCorporal
    template_name = 'gestao_hospitalar/area_corporal_list.html'
    context_object_name = 'areas_corporais'

class AreaCorporalCreateView(AdministradorRequiredMixin, CreateView):
    model = AreaCorporal
    form_class = AreaCorporalForm
    template_name = 'gestao_hospitalar/form_template.html'
    success_url = reverse_lazy('gestao_hospitalar:area_corporal_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Adicionar Nova Área Corporal"
        context['cancel_url'] = reverse_lazy('gestao_hospitalar:area_corporal_list')
        return context

class AreaCorporalUpdateView(AdministradorRequiredMixin, UpdateView):
    model = AreaCorporal
    form_class = AreaCorporalForm
    template_name = 'gestao_hospitalar/form_template.html'
    success_url = reverse_lazy('gestao_hospitalar:area_corporal_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Editar Área Corporal"
        context['cancel_url'] = reverse_lazy('gestao_hospitalar:area_corporal_list')
        return context

class AreaCorporalDeleteView(AdministradorRequiredMixin, DeleteView):
    model = AreaCorporal
    template_name = 'gestao_hospitalar/confirm_delete_template.html'
    success_url = reverse_lazy('gestao_hospitalar:area_corporal_list')
        
class SAEParametrizacaoView(AdminClienteRequiredMixin, TemplateView):
    template_name = 'gestao_hospitalar/sae_parametrizacao.html'


class SAEDashboardView(AdminClienteRequiredMixin, ListView):
    model = Paciente
    template_name = 'gestao_hospitalar/sae_dashboard.html'
    context_object_name = 'pacientes'
    def get_queryset(self):
        return Paciente.objects.filter(empresa=self.request.user.empresa, leito__isnull=False).select_related('leito', 'leito__quarto', 'leito__quarto__ala').order_by('nome')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for paciente in context['pacientes']:
            paciente.ultima_sae = paciente.avaliacoes_sae.order_by('-data_avaliacao').first()
        return context



# ==========================================================
# API INTERNA (VIEWS QUE RETORNAM JSON PARA O FRONTEND)
# ==========================================================

def get_areas_especificas_json(request, area_corporal_id):
    """ Retorna as áreas específicas de uma área corporal (Ex: Crânio, Face para Cabeça) """
    areas = AreaEspecifica.objects.filter(area_corporal_id=area_corporal_id).values('id', 'nome')
    return JsonResponse(list(areas), safe=False)

def get_achados_clinicos_json(request, area_especifica_id, tipo_exame):
    """ Retorna os achados clínicos para uma área e tipo de exame """
    
    # A busca com __iexact (case-insensitive exact) garante que 'INSPECAO' encontre 'Inspeção' ou 'inspeção', etc.
    # Esta é a linha que torna o sistema robusto a diferenças de capitalização.
    tipo_exame_obj = get_object_or_404(TipoExame, nome__iexact=tipo_exame, empresa=request.user.empresa)

    achados = AchadoClinico.objects.filter(
        empresa=request.user.empresa,
        area_especifica_id=area_especifica_id,
        tipo_exame=tipo_exame_obj # Agora filtra pelo objeto, não pelo texto
    ).values('id', 'descricao')
    
    return JsonResponse(list(achados), safe=False)

def sugerir_nanda_json(request):
    """ 
    Recebe uma lista de IDs de achados e sugere os diagnósticos NANDA.
    O frontend enviará os IDs dos checkboxes marcados.
    """
    if request.method == 'POST':
        achados_ids = request.POST.getlist('achados_ids[]')
        if not achados_ids:
            return JsonResponse([], safe=False)

        # Busca diagnósticos distintos associados a QUALQUER um dos achados selecionados
        diagnosticos = DiagnosticoNANDA.objects.filter(
            achados_relacionados__id__in=achados_ids
        ).distinct().values('id', 'codigo', 'titulo', 'definicao')
        
        return JsonResponse(list(diagnosticos), safe=False)
    return JsonResponse({'error': 'Método inválido'}, status=400)

def get_plano_cuidados_json(request, nanda_id):
    """
    Para um NANDA selecionado, retorna os NOCs e NICs (com suas atividades) associados.
    """
    diagnostico = get_object_or_404(DiagnosticoNANDA, pk=nanda_id)
    
    plano = []
    # Itera sobre os resultados (NOC) ligados ao diagnóstico NANDA
    for noc in diagnostico.resultados_noc.all():
        noc_data = {
            'id': noc.id,
            'titulo': noc.titulo,
            'definicao': noc.definicao,
            'intervencoes_nic': []
        }
        # Para cada NOC, itera sobre as intervenções (NIC) ligadas a ele
        for nic in noc.intervencoes_nic.all():
            nic_data = {
                'id': nic.id,
                'titulo': nic.titulo,
                'atividades': list(nic.atividades.all().values('id', 'descricao'))
            }
            noc_data['intervencoes_nic'].append(nic_data)
        plano.append(noc_data)
        
    return JsonResponse(plano, safe=False)

# === Dashboard ===
class HospitalDashboardView(AdminClienteRequiredMixin, TemplateView):
    template_name = 'gestao_hospitalar/dashboard.html'

# === Views para Ala ===
class AlaListView(AdminClienteRequiredMixin, ListView):
    model = Ala
    template_name = 'gestao_hospitalar/ala_list.html'
    context_object_name = 'alas'

    def get_queryset(self):
        # Filtra as alas pela empresa do usuário logado.
        return Ala.objects.filter(empresa=self.request.user.empresa)

class AlaCreateView(AdminClienteRequiredMixin, CreateView):
    model = Ala
    form_class = AlaForm
    template_name = 'gestao_hospitalar/form_template.html'
    success_url = reverse_lazy('gestao_hospitalar:ala_list')

    def form_valid(self, form):
        # Associa a empresa do usuário à nova ala ANTES de salvar.
        form.instance.empresa = self.request.user.empresa
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Adicionar Nova Ala"
        context['cancel_url'] = reverse_lazy('gestao_hospitalar:ala_list')
        return context

class AlaUpdateView(AdminClienteRequiredMixin, UpdateView):
    model = Ala
    form_class = AlaForm
    template_name = 'gestao_hospitalar/form_template.html'
    success_url = reverse_lazy('gestao_hospitalar:ala_list')
    queryset = Ala.objects.all() # O queryset será filtrado no dispatch
    
    def get_queryset(self):
        # Garante que o usuário só possa editar alas da sua própria empresa.
        return Ala.objects.filter(empresa=self.request.user.empresa)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Editar Ala"
        context['cancel_url'] = reverse_lazy('gestao_hospitalar:ala_list')
        return context

class AlaDeleteView(AdminClienteRequiredMixin, DeleteView):
    model = Ala
    template_name = 'gestao_hospitalar/confirm_delete_template.html'
    success_url = reverse_lazy('gestao_hospitalar:ala_list')
    
    def get_queryset(self):
        return Ala.objects.filter(empresa=self.request.user.empresa)

# === Views para Quarto ===
class QuartoListView(AdminClienteRequiredMixin, ListView):
    model = Quarto
    template_name = 'gestao_hospitalar/quarto_list.html'
    context_object_name = 'quartos'

    def get_queryset(self):
        return Quarto.objects.filter(ala__empresa=self.request.user.empresa).select_related('ala')

class QuartoCreateView(AdminClienteRequiredMixin, CreateView):
    model = Quarto
    form_class = QuartoForm
    template_name = 'gestao_hospitalar/form_template.html'
    success_url = reverse_lazy('gestao_hospitalar:quarto_list')
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['empresa'] = self.request.user.empresa
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Adicionar Novo Quarto"
        context['cancel_url'] = reverse_lazy('gestao_hospitalar:quarto_list')
        return context

class QuartoUpdateView(AdminClienteRequiredMixin, UpdateView):
    model = Quarto
    form_class = QuartoForm
    template_name = 'gestao_hospitalar/form_template.html'
    success_url = reverse_lazy('gestao_hospitalar:quarto_list')

    def get_queryset(self):
        return Quarto.objects.filter(ala__empresa=self.request.user.empresa)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['empresa'] = self.request.user.empresa
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Editar Quarto"
        context['cancel_url'] = reverse_lazy('gestao_hospitalar:quarto_list')
        return context

class QuartoDeleteView(AdminClienteRequiredMixin, DeleteView):
    model = Quarto
    template_name = 'gestao_hospitalar/confirm_delete_template.html'
    success_url = reverse_lazy('gestao_hospitalar:quarto_list')

    def get_queryset(self):
        return Quarto.objects.filter(ala__empresa=self.request.user.empresa)

# === Views para Leito ===
class LeitoListView(AdminClienteRequiredMixin, ListView):
    model = Leito
    template_name = 'gestao_hospitalar/leito_list.html'
    context_object_name = 'leitos'

    def get_queryset(self):
        return Leito.objects.filter(quarto__ala__empresa=self.request.user.empresa).select_related('quarto', 'quarto__ala')

class LeitoCreateView(AdminClienteRequiredMixin, CreateView):
    model = Leito
    form_class = LeitoForm
    template_name = 'gestao_hospitalar/form_template.html'
    success_url = reverse_lazy('gestao_hospitalar:leito_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['empresa'] = self.request.user.empresa
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Adicionar Novo Leito"
        context['cancel_url'] = reverse_lazy('gestao_hospitalar:leito_list')
        return context

class LeitoUpdateView(AdminClienteRequiredMixin, UpdateView):
    model = Leito
    form_class = LeitoForm
    template_name = 'gestao_hospitalar/form_template.html'
    success_url = reverse_lazy('gestao_hospitalar:leito_list')

    def get_queryset(self):
        return Leito.objects.filter(quarto__ala__empresa=self.request.user.empresa)
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['empresa'] = self.request.user.empresa
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Editar Leito"
        context['cancel_url'] = reverse_lazy('gestao_hospitalar:leito_list')
        return context

class LeitoDeleteView(AdminClienteRequiredMixin, DeleteView):
    model = Leito
    template_name = 'gestao_hospitalar/confirm_delete_template.html'
    success_url = reverse_lazy('gestao_hospitalar:leito_list')
    
    def get_queryset(self):
        return Leito.objects.filter(quarto__ala__empresa=self.request.user.empresa)

# === Views para Paciente ===
class PacienteListView(AdminClienteRequiredMixin, ListView):
    model = Paciente
    template_name = 'gestao_hospitalar/paciente_list.html'
    context_object_name = 'pacientes'

    def get_queryset(self):
        return Paciente.objects.filter(empresa=self.request.user.empresa)

class PacienteCreateView(AdminClienteRequiredMixin, CreateView):
    model = Paciente
    form_class = PacienteForm
    template_name = 'gestao_hospitalar/form_template.html'
    success_url = reverse_lazy('gestao_hospitalar:paciente_list')
    
    def form_valid(self, form):
        form.instance.empresa = self.request.user.empresa
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['empresa'] = self.request.user.empresa
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Adicionar Novo Paciente"
        context['cancel_url'] = reverse_lazy('gestao_hospitalar:paciente_list')
        return context

class PacienteUpdateView(AdminClienteRequiredMixin, UpdateView):
    model = Paciente
    form_class = PacienteForm
    template_name = 'gestao_hospitalar/form_template.html'
    success_url = reverse_lazy('gestao_hospitalar:paciente_list')

    def get_queryset(self):
        return Paciente.objects.filter(empresa=self.request.user.empresa)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['empresa'] = self.request.user.empresa
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Editar Paciente"
        context['cancel_url'] = reverse_lazy('gestao_hospitalar:paciente_list')
        return context

class PacienteDeleteView(AdminClienteRequiredMixin, DeleteView):
    model = Paciente
    template_name = 'gestao_hospitalar/confirm_delete_template.html'
    success_url = reverse_lazy('gestao_hospitalar:paciente_list')

    def get_queryset(self):
        return Paciente.objects.filter(empresa=self.request.user.empresa)
    
class ListaPacientesParaAvaliacaoView(AdminClienteRequiredMixin, ListView):
    model = Paciente
    template_name = 'gestao_hospitalar/paciente_avaliacao_list.html'
    context_object_name = 'pacientes'

    def get_queryset(self):
        # Mostra apenas pacientes que estão atualmente em um leito (internados)
        return Paciente.objects.filter(
            empresa=self.request.user.empresa, 
            leito__isnull=False
        ).select_related('leito', 'leito__quarto').order_by('leito__quarto__ala__nome', 'leito__quarto__numero', 'leito__numero')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        hoje = timezone.now().date()
        # Adiciona a última avaliação de cada paciente para fácil visualização
        for paciente in context['pacientes']:
            paciente.ultima_avaliacao = paciente.avaliacoes_fugulin.order_by('-data_avaliacao').first()
            # Verifica se a avaliação de hoje já foi feita
            paciente.avaliacao_hoje_feita = paciente.avaliacoes_fugulin.filter(data_avaliacao=hoje).exists()
        return context

class AvaliarPacienteView(AdminClienteRequiredMixin, View):
    form_class = AvaliacaoFugulinForm
    template_name = 'gestao_hospitalar/avaliacao_fugulin_form.html'

    def get_object(self):
        # Tenta pegar a avaliação de HOJE para este paciente
        paciente = get_object_or_404(Paciente, pk=self.kwargs['pk'], empresa=self.request.user.empresa)
        avaliacao = AvaliacaoFugulin.objects.filter(paciente=paciente, data_avaliacao=timezone.now().date()).first()
        return paciente, avaliacao

    def get(self, request, *args, **kwargs):
        paciente, avaliacao = self.get_object()
        form = self.form_class(instance=avaliacao)
        return render(request, self.template_name, {'form': form, 'paciente': paciente})

    def post(self, request, *args, **kwargs):
        paciente, avaliacao = self.get_object()
        form = self.form_class(request.POST, instance=avaliacao)
        if form.is_valid():
            nova_avaliacao = form.save(commit=False)
            nova_avaliacao.paciente = paciente
            nova_avaliacao.avaliador = request.user
            nova_avaliacao.data_avaliacao = timezone.now().date()
            nova_avaliacao.save()
            return redirect('gestao_hospitalar:paciente_avaliacao_list')
        return render(request, self.template_name, {'form': form, 'paciente': paciente})

class PacienteAltaView(AdminClienteRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        paciente = get_object_or_404(Paciente, pk=kwargs['pk'], empresa=request.user.empresa)
        return render(request, 'gestao_hospitalar/paciente_alta_confirm.html', {'paciente': paciente})

    def post(self, request, *args, **kwargs):
        paciente = get_object_or_404(Paciente, pk=kwargs['pk'], empresa=request.user.empresa)
        paciente.leito = None  # Desvincula o paciente do leito
        paciente.save()
        return redirect('gestao_hospitalar:paciente_avaliacao_list')
    
class SAEWizardView(AdminClienteRequiredMixin, View):
    
    def get(self, request, paciente_pk):
        paciente = get_object_or_404(Paciente, pk=paciente_pk, empresa=request.user.empresa)
        if not paciente.leito:
            raise Http404("Este paciente não está internado e não pode ser avaliado.")
        
        areas_corporais = AreaCorporal.objects.all().order_by('id')
        context = {
            'paciente': paciente,
            'areas_corporais': areas_corporais
        }
        return render(request, 'gestao_hospitalar/sae_wizard_form.html', context)

    @transaction.atomic
    def post(self, request, paciente_pk):
        paciente = get_object_or_404(Paciente, pk=paciente_pk, empresa=request.user.empresa)
        data = json.loads(request.body)

        avaliacao = AvaliacaoSAE.objects.create(
            paciente=paciente,
            avaliador=request.user,
            diagnostico_nanda_selecionado_id=data.get('selectedNANDA_id'),
            is_finalizada=True
        )
        
        achados_ids = data.get('selectedAchadosIds', [])
        if achados_ids:
            avaliacao.achados_selecionados.set(achados_ids)

        plano_de_cuidados_data = data.get('carePlanProgress', {})
        for nic_id, progresso in plano_de_cuidados_data.items():
            PlanoCuidado.objects.create(
                avaliacao=avaliacao,
                intervencao_nic_id=nic_id,
                progresso_atividades=progresso
            )

        # Retorna a URL para a página de detalhes da avaliação recém-criada
        detail_url = reverse_lazy('gestao_hospitalar:sae_avaliacao_detail', kwargs={'pk': avaliacao.pk})
        return JsonResponse({'status': 'success', 'redirect_url': str(detail_url)})

    
class SAEHistoricoView(AdminClienteRequiredMixin, DetailView):
    model = Paciente
    template_name = 'gestao_hospitalar/sae_historico_paciente.html'
    context_object_name = 'paciente'
    pk_url_kwarg = 'paciente_pk' # Informa ao Django que o ID na URL é 'paciente_pk'

    def get_queryset(self):
        return Paciente.objects.filter(empresa=self.request.user.empresa)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paciente = self.object
        context['avaliacoes'] = paciente.avaliacoes_sae.all().select_related('avaliador', 'diagnostico_nanda_selecionado')
        return context

class SAEAvaliacaoDetailView(AdminClienteRequiredMixin, DetailView):
    model = AvaliacaoSAE
    template_name = 'gestao_hospitalar/sae_avaliacao_detail.html'
    context_object_name = 'avaliacao'

    def get_queryset(self):
        return AvaliacaoSAE.objects.select_related(
            'paciente', 'avaliador', 'diagnostico_nanda_selecionado'
        ).filter(paciente__empresa=self.request.user.empresa)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        avaliacao = self.object
        nanda = avaliacao.diagnostico_nanda_selecionado
        
        plan_json = []
        if nanda:
            # Busca os NOCs ligados ao NANDA da avaliação
            nocs = nanda.resultados_noc.prefetch_related('intervencoes_nic__atividades').all()

            for noc in nocs:
                nic_list = []
                for nic in noc.intervencoes_nic.all():
                    # Para cada NIC, busca ou cria o registro de progresso
                    plano, _ = PlanoCuidado.objects.get_or_create(
                        avaliacao=avaliacao,
                        intervencao_nic=nic
                    )
                    
                    nic_list.append({
                        'id': nic.id,
                        'codigo': nic.codigo,
                        'titulo': nic.titulo,
                        'atividades': list(nic.atividades.values_list('descricao', flat=True)),
                        'plano_id': plano.id,
                        # Pega o progresso já salvo no banco
                        'checked': plano.progresso_atividades.get('checked', []) 
                    })
                
                plan_json.append({
                    'id': noc.id,
                    'codigo': noc.codigo,
                    'titulo': noc.titulo,
                    'intervencoes': nic_list
                })

        context['plan_json'] = plan_json
        return context

@csrf_exempt
def toggle_plano_atividade(request, plano_id):
    if request.method == 'POST':
        plano = get_object_or_404(PlanoCuidado, pk=plano_id)
        # Garante que o usuário só pode modificar planos da sua empresa
        if plano.avaliacao.paciente.empresa != request.user.empresa:
            return JsonResponse({'status': 'error', 'message': 'Permissão negada.'}, status=403)
        
        data = json.loads(request.body)
        idx = data.get('idx')
        checked = data.get('checked')

        progresso = plano.progresso_atividades or {'checked': []}
        
        if checked:
            if idx not in progresso['checked']:
                progresso['checked'].append(idx)
        else:
            if idx in progresso['checked']:
                progresso['checked'].remove(idx)

        plano.progresso_atividades = progresso
        plano.save()
        
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error', 'message': 'Método inválido.'}, status=400)



# === Views para Tipo de Exame ===

class TipoExameListView(AdminClienteRequiredMixin, ListView):
    model = TipoExame
    template_name = 'gestao_hospitalar/tipo_exame_list.html'
    context_object_name = 'tipos_exame'

    def get_queryset(self):
        return TipoExame.objects.filter(empresa=self.request.user.empresa)

class TipoExameCreateView(AdminClienteRequiredMixin, CreateView):
    model = TipoExame
    form_class = TipoExameForm
    template_name = 'gestao_hospitalar/form_template.html'
    success_url = reverse_lazy('gestao_hospitalar:tipo_exame_list')

    def form_valid(self, form):
        form.instance.empresa = self.request.user.empresa
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Adicionar Novo Tipo de Exame"
        context['cancel_url'] = reverse_lazy('gestao_hospitalar:tipo_exame_list')
        return context

class TipoExameUpdateView(AdminClienteRequiredMixin, UpdateView):
    model = TipoExame
    form_class = TipoExameForm
    template_name = 'gestao_hospitalar/form_template.html'
    success_url = reverse_lazy('gestao_hospitalar:tipo_exame_list')

    def get_queryset(self):
        return TipoExame.objects.filter(empresa=self.request.user.empresa)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Editar Tipo de Exame"
        context['cancel_url'] = reverse_lazy('gestao_hospitalar:tipo_exame_list')
        return context

class TipoExameDeleteView(AdminClienteRequiredMixin, DeleteView):
    model = TipoExame
    template_name = 'gestao_hospitalar/confirm_delete_template.html'
    success_url = reverse_lazy('gestao_hospitalar:tipo_exame_list')
    
    def get_queryset(self):
        return TipoExame.objects.filter(empresa=self.request.user.empresa)
    

class AreaEspecificaListView(AdminClienteRequiredMixin, ListView):
    model = AreaEspecifica
    template_name = 'gestao_hospitalar/area_especifica_list.html'
    context_object_name = 'areas_especificas'

    def get_queryset(self):
        return AreaEspecifica.objects.filter(empresa=self.request.user.empresa).select_related('area_corporal')

class AreaEspecificaCreateView(AdminClienteRequiredMixin, CreateView):
    model = AreaEspecifica
    form_class = AreaEspecificaForm
    template_name = 'gestao_hospitalar/form_template.html'
    success_url = reverse_lazy('gestao_hospitalar:area_especifica_list')

    def form_valid(self, form):
        form.instance.empresa = self.request.user.empresa
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Adicionar Nova Área Específica"
        context['cancel_url'] = reverse_lazy('gestao_hospitalar:area_especifica_list')
        return context

class AreaEspecificaUpdateView(AdminClienteRequiredMixin, UpdateView):
    model = AreaEspecifica
    form_class = AreaEspecificaForm
    template_name = 'gestao_hospitalar/form_template.html'
    success_url = reverse_lazy('gestao_hospitalar:area_especifica_list')
    
    def get_queryset(self):
        return AreaEspecifica.objects.filter(empresa=self.request.user.empresa)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Editar Área Específica"
        context['cancel_url'] = reverse_lazy('gestao_hospitalar:area_especifica_list')
        return context

class AreaEspecificaDeleteView(AdminClienteRequiredMixin, DeleteView):
    model = AreaEspecifica
    template_name = 'gestao_hospitalar/confirm_delete_template.html'
    success_url = reverse_lazy('gestao_hospitalar:area_especifica_list')
    
    def get_queryset(self):
        return AreaEspecifica.objects.filter(empresa=self.request.user.empresa)