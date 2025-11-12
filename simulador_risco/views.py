from django.shortcuts import render
from django.http import JsonResponse
from .models import CNAE
import requests # Lembre-se de instalar
import json
from django.db.models import Q 
from django.views.decorators.csrf import csrf_exempt

def pagina_simulador(request):
    # View principal que renderiza o HTML da ferramenta
    return render(request, 'simulador_risco/simulador.html')

def api_consultar_cnpj(request, cnpj):
    # Remove formatação do CNPJ
    cnpj = ''.join(filter(str.isdigit, cnpj))

    # Tenta a BrasilAPI
    try:
        response = requests.get(f"https://brasilapi.com.br/api/cnpj/v1/{cnpj}")
        response.raise_for_status() 
        data = response.json()

        # Coleta os CNAEs
        cnaes_codes = []
        if data.get('cnae_fiscal'):
            cnaes_codes.append(str(data['cnae_fiscal']))
        if data.get('cnaes_secundarios'):
            for cnae_sec in data['cnaes_secundarios']:
                cnaes_codes.append(str(cnae_sec['codigo']))

        # Monta a resposta final incluindo os dados da empresa e os CNAEs
        resposta_final = {
            'empresa_data': {
                'razao_social': data.get('razao_social'),
                'nome_fantasia': data.get('nome_fantasia'),
                'situacao_cadastral': data.get('descricao_situacao_cadastral'),
            },
            'cnaes': cnaes_codes
        }

        return JsonResponse(resposta_final)

    except requests.RequestException as e:
        return JsonResponse({'erro': f'Falha ao consultar API: {str(e)}'}, status=500)


def formatar_cnae(codigo):
    """Helper para formatar o código CNAE de 7 dígitos."""
    if len(codigo) == 7:
        return f"{codigo[0:4]}-{codigo[4]}/{codigo[5:]}"
    return codigo

@csrf_exempt
def api_consultar_cnaes(request):
    if request.method != 'POST':
        return JsonResponse({'erro': 'Metodo nao permitido'}, status=405)

    try:
        data = json.loads(request.body)
        cnaes_codigos = data.get('cnaes', [])
        cnaes_codigos_limpos = [''.join(filter(str.isdigit, c)) for c in cnaes_codigos]

        RISCO_MAP = {'NA': 0, 'I': 1, 'II': 2, 'III': 3, 'P': 4} # 'P' agora é o mais alto para ordenação
        RISCO_CORES = {'NA': 'info', 'I': 'success', 'II': 'warning', 'III': 'danger', 'P': 'secondary'}
        RISCO_TOOLTIPS = {
            'NA': 'Não se Aplica - Dispensado de alvará sanitário para esta atividade.',
            'I': 'Nível de Risco I - Baixo Risco',
            'II': 'Nível de Risco II - Médio Risco',
            'III': 'Nível de Risco III - Alto Risco',
            'P': 'Responder a pergunta para classificar o risco',
            'N/A': 'CNAE não encontrado na base da Resolução SES/MG.'
        }

        resultado_final = {'cnaes_processados': [], 'perguntas_necessarias': []}
        risco_max = 0

        cnaes_encontrados = CNAE.objects.filter(codigo__in=cnaes_codigos_limpos)
        codigos_encontrados = {c.codigo for c in cnaes_encontrados}

        for cnae in cnaes_encontrados:
            perguntas_do_cnae = []
            if cnae.risco_base == 'P':
                for pergunta in cnae.perguntas.all().prefetch_related('opcoes'):
                    opcoes_data = [{'texto': op.texto, 'risco': op.risco_resultante} for op in pergunta.opcoes.all()]
                    pergunta_data = {
                        'numero': pergunta.numero, 'texto': pergunta.texto, 'opcoes': opcoes_data,
                        'cnae_origem_codigo': cnae.codigo,
                        'cnae_origem_descricao': cnae.descricao # <<-- NOVIDADE
                    }
                    if pergunta.numero not in [p['numero'] for p in resultado_final['perguntas_necessarias']]:
                        resultado_final['perguntas_necessarias'].append(pergunta_data)
                    perguntas_do_cnae.append(pergunta.numero)
            
            tooltip_text = RISCO_TOOLTIPS.get(cnae.risco_base, '')
            if cnae.risco_base == 'III' and not cnae.dispensado_de_projeto:
                tooltip_text = 'Nível de Risco III com exigência de projeto arquitetônico aprovado'
            
            resultado_final['cnaes_processados'].append({
                'codigo': cnae.codigo,
                'codigo_formatado': formatar_cnae(cnae.codigo), # <<-- NOVIDADE
                'descricao': cnae.descricao,
                'risco_base': cnae.risco_base,
                'cor': RISCO_CORES.get(cnae.risco_base, 'dark'),
                'tooltip': tooltip_text, 
                'perguntas_nums': perguntas_do_cnae,
                'ordem': RISCO_MAP.get(cnae.risco_base, -1), # <<-- NOVIDADE para ordenação
                'dispensado_projeto': cnae.dispensado_de_projeto,
            })

            if cnae.risco_base != 'P':
                risco_max = max(risco_max, RISCO_MAP.get(cnae.risco_base, 0))
        
        for codigo in cnaes_codigos_limpos:
            if codigo not in codigos_encontrados:
                resultado_final['cnaes_processados'].append({
                    'codigo': codigo, 'codigo_formatado': formatar_cnae(codigo), 'descricao': 'CNAE não encontrado na base da Resolução.',
                    'risco_base': 'N/A', 'cor': 'light', 'tooltip': RISCO_TOOLTIPS.get('N/A', ''), 'perguntas_nums': [], 'ordem': -1
                })
        
        resultado_final['risco_final_empresa'] = next((k for k, v in RISCO_MAP.items() if v == risco_max), 'NA')
        return JsonResponse(resultado_final)

    except Exception as e:
        return JsonResponse({'erro': str(e)}, status=500)
    
def api_buscar_cnae(request):
    """View para a busca com autocompletar de CNAEs."""
    termo = request.GET.get('termo', '').strip()
    
    if len(termo) < 3:
        return JsonResponse([], safe=False)

    termo_limpo = ''.join(filter(str.isdigit, termo))
    
    # Inicia a query buscando sempre pela descrição com o termo original
    query = Q(descricao__icontains=termo)
    
    # Se o termo limpo (só com números) não for vazio, adiciona a busca por código
    if termo_limpo:
        query |= Q(codigo__icontains=termo_limpo)
    
    cnaes = CNAE.objects.filter(query)[:10]

    resultados = [
        {
            'id': cnae.codigo,
            'text': f"{formatar_cnae(cnae.codigo)} - {cnae.descricao}"
        }
        for cnae in cnaes
    ]
    
    return JsonResponse(resultados, safe=False)