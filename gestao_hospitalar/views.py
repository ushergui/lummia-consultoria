from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView
from .models import Ala, AvaliacaoFugulin, Quarto, Leito, Paciente
from .forms import AlaForm, QuartoForm, LeitoForm, PacienteForm, AvaliacaoFugulinForm
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.utils import timezone

# Este Mixin agora serve apenas para verificar a permissão do usuário.
class AdminClienteRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.tipo_perfil in ['ADMIN_CLIENTE', 'ADMINISTRADOR']

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