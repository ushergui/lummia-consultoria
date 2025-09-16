from django import forms
from .models import Ala, Quarto, Leito, Paciente
from django_select2.forms import Select2Widget, Select2MultipleWidget
from .models import AvaliacaoFugulin

class AvaliacaoFugulinForm(forms.ModelForm):
    # 1. Estado Mental
    estado_mental = forms.ChoiceField(
        label="Estado Mental",
        choices=[(1, 'Orientado no tempo e no espaço'), (2, 'Períodos de desorientação'), (3, 'Períodos de inconsciência'), (4, 'Inconsciente')],
        widget=forms.RadioSelect, required=True
    )
    # 2. Oxigenação
    oxigenacao = forms.ChoiceField(
        label="Oxigenação",
        choices=[(1, 'Não depende de O₂'), (2, 'Uso intermitente de O₂'), (3, 'Uso contínuo de O₂'), (4, 'Ventilação mecânica')],
        widget=forms.RadioSelect, required=True
    )
    # 3. Sinais Vitais
    sinais_vitais = forms.ChoiceField(
        label="Sinais Vitais",
        choices=[(1, 'Controle de rotina (8h)'), (2, 'Controle a cada 6h'), (3, 'Controle a cada 4h'), (4, 'Controle a cada ≤ 2h')],
        widget=forms.RadioSelect, required=True
    )
    # 4. Motilidade
    motilidade = forms.ChoiceField(
        label="Motilidade",
        choices=[(1, 'Movimenta todos os segmentos'), (2, 'Limitação de movimentos'), (3, 'Dificuldade para movimentar'), (4, 'Incapaz de movimentar')],
        widget=forms.RadioSelect, required=True
    )
    # 5. Deambulação
    deambulacao = forms.ChoiceField(
        label="Deambulação",
        choices=[(1, 'Ambulante'), (2, 'Necessita de auxílio'), (3, 'Cadeira de rodas'), (4, 'Restrito ao leito')],
        widget=forms.RadioSelect, required=True
    )
    # 6. Alimentação
    alimentacao = forms.ChoiceField(
        label="Alimentação",
        choices=[(1, 'Auto-suficiente'), (2, 'Por boca com auxílio'), (3, 'Via Sonda Nasogástrica'), (4, 'Via Cateter Central')],
        widget=forms.RadioSelect, required=True
    )
    # 7. Cuidado Corporal
    cuidado_corporal = forms.ChoiceField(
        label="Cuidado Corporal",
        choices=[(1, 'Auto-suficiente'), (2, 'Auxílio no banho'), (3, 'Banho pela enfermagem'), (4, 'Banho no leito')],
        widget=forms.RadioSelect, required=True
    )
    # 8. Eliminação
    eliminacao = forms.ChoiceField(
        label="Eliminação",
        choices=[(1, 'Auto-suficiente'), (2, 'Vaso com auxílio'), (3, 'Uso de comadre'), (4, 'Sonda Vesical')],
        widget=forms.RadioSelect, required=True
    )
    # 9. Terapêutica
    terapeutica = forms.ChoiceField(
        label="Terapêutica",
        choices=[(1, 'IM ou VO'), (2, 'EV Intermitente'), (3, 'EV Contínua / SNG'), (4, 'Drogas Vasoativas')],
        widget=forms.RadioSelect, required=True
    )

    class Meta:
        model = AvaliacaoFugulin
        fields = [
            'estado_mental', 'oxigenacao', 'sinais_vitais', 'motilidade', 
            'deambulacao', 'alimentacao', 'cuidado_corporal', 'eliminacao', 'terapeutica'
        ]


class AlaForm(forms.ModelForm):
    class Meta:
        model = Ala
        fields = ['nome']

class QuartoForm(forms.ModelForm):
    class Meta:
        model = Quarto
        fields = ['numero', 'ala']

    def __init__(self, *args, **kwargs):
        empresa = kwargs.pop('empresa', None)
        super().__init__(*args, **kwargs)
        if empresa:
            self.fields['ala'].queryset = Ala.objects.filter(empresa=empresa)
            self.fields['ala'].empty_label = "Selecione uma ala"

class LeitoForm(forms.ModelForm):
    class Meta:
        model = Leito
        fields = ['numero', 'quarto']

    def __init__(self, *args, **kwargs):
        empresa = kwargs.pop('empresa', None)
        super().__init__(*args, **kwargs)
        if empresa:
            self.fields['quarto'].queryset = Quarto.objects.filter(ala__empresa=empresa).select_related('ala')
            self.fields['quarto'].empty_label = "Selecione um quarto"

class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = ['nome', 'data_nascimento', 'leito', 'hipotese_diagnostica_principal', 'diagnosticos_complementares']
        widgets = {
            'data_nascimento': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'hipotese_diagnostica_principal': Select2Widget,
            'diagnosticos_complementares': Select2MultipleWidget,
            # Adicionando classes para consistência visual
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'leito': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        empresa = kwargs.pop('empresa', None)
        super().__init__(*args, **kwargs)
        
        # Define o rótulo vazio para o campo de leito
        self.fields['leito'].empty_label = "Nenhum leito (Paciente sem alocação)"

        if empresa:
            # Pega os leitos já ocupados pela empresa atual
            leitos_ocupados_ids = Paciente.objects.filter(
                empresa=empresa, leito__isnull=False
            ).values_list('leito__id', flat=True)
            
            # Se estiver editando um paciente que já tem leito, o leito dele deve aparecer na lista
            if self.instance and self.instance.pk and self.instance.leito:
                leitos_ocupados_ids = list(leitos_ocupados_ids)
                leitos_ocupados_ids.remove(self.instance.leito.id)

            # Filtra o queryset para mostrar apenas leitos vagos da empresa do usuário
            self.fields['leito'].queryset = Leito.objects.filter(
                quarto__ala__empresa=empresa
            ).exclude(id__in=leitos_ocupados_ids).select_related('quarto', 'quarto__ala')