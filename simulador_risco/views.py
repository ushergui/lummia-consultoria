# simulador_risco/views.py

from django.shortcuts import render
from django.http import JsonResponse
from .models import CNAE, ClassificacaoAmbiental
import requests 
import json
from django.db.models import Q 
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

# --- View Principal ---
def pagina_simulador(request):
    """Renderiza a página principal do simulador e passa a chave pública do reCAPTCHA."""
    return render(request, 'simulador_risco/simulador.html', {'RECAPTCHA_PUBLIC_KEY': settings.RECAPTCHA_PUBLIC_KEY})

# --- Função Auxiliar de Validação ---
def _is_recaptcha_valid(recaptcha_response, min_score=0.5):
    """Função auxiliar para validar o token do reCAPTCHA v3 junto à API do Google."""
    if not recaptcha_response:
        return False
    
    data = {
        'secret': settings.RECAPTCHA_PRIVATE_KEY,
        'response': recaptcha_response
    }
    try:
        r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data, timeout=5)
        r.raise_for_status()
        result = r.json()
        
        # Para reCAPTCHA v3, verificamos o score de confiança
        if result.get('success', False) and result.get('score', 0) >= min_score:
            return True
        return False
    except requests.RequestException:
        return False

# --- Views da API ---
def api_consultar_cnpj(request, cnpj):
    """API para consultar os CNAEs de um CNPJ, com validação reCAPTCHA."""
    if request.method != 'GET':
        return JsonResponse({'erro': 'Método não permitido'}, status=405)

    recaptcha_response = request.GET.get('g-recaptcha-response')
    if not _is_recaptcha_valid(recaptcha_response):
        return JsonResponse({'erro': 'Falha na verificação de segurança. Sua ação pareceu automatizada.'}, status=403)

    cnpj_limpo = ''.join(filter(str.isdigit, cnpj))
    try:
        response = requests.get(f"https://brasilapi.com.br/api/cnpj/v1/{cnpj_limpo}", timeout=10)
        response.raise_for_status() 
        data = response.json()

        cnaes_codes = []
        if data.get('cnae_fiscal'):
            cnaes_codes.append(str(data['cnae_fiscal']))
        if data.get('cnaes_secundarios'):
            for cnae_sec in data.get('cnaes_secundarios', []):
                cnaes_codes.append(str(cnae_sec.get('codigo')))

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
        return JsonResponse({'erro': f'Falha ao consultar API externa: {str(e)}'}, status=500)

@csrf_exempt
def api_consultar_cnaes(request):
    """API principal que recebe a lista de CNAEs e retorna a análise de risco, com validação reCAPTCHA."""
    if request.method != 'POST':
        return JsonResponse({'erro': 'Método não permitido'}, status=405)

    try:
        data = json.loads(request.body)
        
        recaptcha_response = data.get('g-recaptcha-response')
        if not _is_recaptcha_valid(recaptcha_response):
            return JsonResponse({'erro': 'Falha na verificação de segurança. Sua ação pareceu automatizada.'}, status=403)

        cnaes_codigos = data.get('cnaes', [])
        cnaes_codigos_limpos = [''.join(filter(str.isdigit, c)) for c in cnaes_codigos]

        RISCO_MAP = {'NA': 0, 'I': 1, 'II': 2, 'III': 3, 'P': 4}
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
                        'cnae_origem_descricao': cnae.descricao
                    }
                    if pergunta.numero not in [p['numero'] for p in resultado_final['perguntas_necessarias']]:
                        resultado_final['perguntas_necessarias'].append(pergunta_data)
                    perguntas_do_cnae.append(pergunta.numero)
            
            tooltip_text = RISCO_TOOLTIPS.get(cnae.risco_base, '')
            if cnae.risco_base == 'III' and not cnae.dispensado_de_projeto:
                tooltip_text = 'Nível de Risco III com exigência de projeto arquitetônico aprovado'
            
            resultado_final['cnaes_processados'].append({
                'codigo': cnae.codigo, 'codigo_formatado': formatar_cnae(cnae.codigo),
                'descricao': cnae.descricao, 'risco_base': cnae.risco_base,
                'cor': RISCO_CORES.get(cnae.risco_base, 'dark'), 'tooltip': tooltip_text, 
                'perguntas_nums': perguntas_do_cnae, 'ordem': RISCO_MAP.get(cnae.risco_base, -1),
                'dispensado_projeto': cnae.dispensado_de_projeto,
            })
        
        for codigo in cnaes_codigos_limpos:
            if codigo not in codigos_encontrados:
                resultado_final['cnaes_processados'].append({
                    'codigo': codigo, 'codigo_formatado': formatar_cnae(codigo), 
                    'descricao': 'CNAE não encontrado na base da Resolução.', 'risco_base': 'N/A', 
                    'cor': 'light', 'tooltip': RISCO_TOOLTIPS.get('N/A', ''), 
                    'perguntas_nums': [], 'ordem': -1
                })
        
        return JsonResponse(resultado_final)
    except Exception as e:
        return JsonResponse({'erro': str(e)}, status=500)

def api_buscar_cnae(request):
    """View para a busca com autocompletar de CNAEs (não precisa de CAPTCHA)."""
    termo = request.GET.get('termo', '').strip()
    if len(termo) < 3:
        return JsonResponse([], safe=False)
    termo_limpo = ''.join(filter(str.isdigit, termo))
    query = Q(descricao__icontains=termo)
    if termo_limpo:
        query |= Q(codigo__icontains=termo_limpo)
    cnaes = CNAE.objects.filter(query)[:10]
    resultados = [{'id': cnae.codigo, 'text': f"{formatar_cnae(cnae.codigo)} - {cnae.descricao}"} for cnae in cnaes]
    return JsonResponse(resultados, safe=False)

def formatar_cnae(codigo):
    """Helper para formatar o código CNAE de 7 dígitos."""
    if codigo and len(codigo) == 7:
        return f"{codigo[0:4]}-{codigo[4]}/{codigo[5:]}"
    return codigo

def simulador_ambiental(request):
    resultado = None
    risco_geral = "Não Classificado"
    cor_risco = "secondary" # cinza padrão
    mensagem_resultado = "Insira os CNAEs para verificar a classificação."
    cnaes_encontrados = []
    cnaes_nao_encontrados = []

    if request.method == 'POST':
        # Pega o input do usuário (CNPJ ou Lista de CNAEs)
        # Aqui focamos na lista de CNAEs. Se tiver lógica de API de CNPJ pronta, 
        # você pode adaptar para preencher a lista 'cnaes_input' automaticamente.
        cnaes_input = request.POST.get('cnaes', '')
        
        # Limpa e separa os códigos (aceita vírgula, ponto e vírgula, quebra de linha)
        # Exemplo: "0111-3/01, 0111302" vira ['0111301', '0111302']
        codigos_limpos = re.findall(r'\d+', cnaes_input)
        
        # Lista para guardar objetos de ClassificacaoAmbiental encontrados
        classificacoes = []
        
        for codigo in codigos_limpos:
            # Tenta buscar CNAE base
            try:
                cnae_obj = CNAE.objects.get(codigo=codigo)
                
                # Busca as classificações ambientais vinculadas a este CNAE
                # Um CNAE pode ter mais de uma classificação (ex: riscos diferentes dependendo do porte/detalhe)
                itens_ambientais = ClassificacaoAmbiental.objects.filter(cnae=cnae_obj)
                
                if itens_ambientais.exists():
                    for item in itens_ambientais:
                        classificacoes.append(item)
                        cnaes_encontrados.append(codigo)
                else:
                    # CNAE existe na base IBGE, mas não tem classificação específica no Decreto Municipal
                    # Pode ser tratado como "Não Listada" ou "Risco I" dependendo da regra.
                    # Vamos marcar como "Sem classificação específica encontrada"
                    cnaes_nao_encontrados.append(f"{codigo} (Sem classificação ambiental)")
                    
            except CNAE.DoesNotExist:
                cnaes_nao_encontrados.append(codigo)

        # Lógica de Cálculo do Risco Geral (Hierarquia: III > II > I)
        if classificacoes:
            riscos = [c.nivel_risco for c in classificacoes if c.nivel_risco]
            
            if 'III' in riscos:
                risco_geral = 'III'
                cor_risco = 'danger' # Vermelho
                mensagem_resultado = "ATIVIDADE DE ALTO RISCO AMBIENTAL"
            elif 'II' in riscos:
                risco_geral = 'II'
                cor_risco = 'warning' # Amarelo/Laranja
                mensagem_resultado = "ATIVIDADE DE MÉDIO RISCO AMBIENTAL"
            elif 'I' in riscos:
                risco_geral = 'I'
                cor_risco = 'success' # Verde
                mensagem_resultado = "ATIVIDADE DE BAIXO RISCO AMBIENTAL (Dispensado de Licenciamento)"
            else:
                risco_geral = "Não Definido"
        elif cnaes_input:
             mensagem_resultado = "Nenhuma classificação ambiental encontrada para os códigos informados."

        resultado = {
            'classificacoes': classificacoes,
            'risco_geral': risco_geral,
            'cor_risco': cor_risco,
            'mensagem': mensagem_resultado,
            'nao_encontrados': cnaes_nao_encontrados
        }

    return render(request, 'simulador_risco/simulador_ambiental.html', {'resultado': resultado})


@csrf_exempt
def api_consultar_cnaes_ambiental(request):
    """
    API específica para o Simulador Ambiental.
    Recebe lista de CNAEs via JSON, consulta ClassificacaoAmbiental e retorna JSON estruturado.
    """
    if request.method != 'POST':
        return JsonResponse({'erro': 'Método não permitido'}, status=405)

    try:
        data = json.loads(request.body)
        
        # Validação reCAPTCHA (Reutilizando sua função _is_recaptcha_valid)
        recaptcha_response = data.get('g-recaptcha-response')
        if not _is_recaptcha_valid(recaptcha_response):
            return JsonResponse({'erro': 'Falha na verificação de segurança.'}, status=403)

        cnaes_codigos = data.get('cnaes', [])
        # Limpeza dos códigos
        cnaes_codigos_limpos = [''.join(filter(str.isdigit, str(c))) for c in cnaes_codigos]

        resultado_final = {'cnaes_processados': []}
        
        # Mapeamento de Risco para Ordenação e Cores
        RISCO_MAP = {'I': 1, 'II': 2, 'III': 3}
        RISCO_CORES = {'I': 'success', 'II': 'warning', 'III': 'danger', 'NA': 'secondary'}

        for codigo in cnaes_codigos_limpos:
            try:
                cnae_obj = CNAE.objects.get(codigo=codigo)
                
                # Busca as classificações ambientais específicas
                classificacoes = ClassificacaoAmbiental.objects.filter(cnae=cnae_obj)
                
                detalhes_ambientais = []
                risco_max_cnae = 0
                risco_texto_cnae = "NA"

                if classificacoes.exists():
                    for item in classificacoes:
                        # Determina o maior risco entre as opções deste CNAE
                        valor_risco = RISCO_MAP.get(item.nivel_risco, 0)
                        if valor_risco > risco_max_cnae:
                            risco_max_cnae = valor_risco
                            risco_texto_cnae = item.nivel_risco

                        detalhes_ambientais.append({
                            'nivel_agregacao': item.nivel_agregacao,
                            'dn_copam': item.codigo_dn_copam,
                            'descricao_especifica': item.descricao_atividade,
                            'exigencia': item.exigencia_municipal,
                            'risco': item.nivel_risco,
                            'cor': RISCO_CORES.get(item.nivel_risco, 'secondary')
                        })
                else:
                    # Se não tem classificação específica, considera risco I ou NA conforme sua regra
                    risco_texto_cnae = "I" # Assumindo padrão baixo risco se não listado
                    detalhes_ambientais.append({
                        'dn_copam': 'N/A',
                        'descricao_especifica': 'Atividade não listada especificamente no Decreto (Regra Geral)',
                        'exigencia': 'Não se aplica / Dispensa',
                        'risco': 'I',
                        'cor': 'success'
                    })

                resultado_final['cnaes_processados'].append({
                    'codigo': cnae_obj.codigo,
                    'codigo_formatado': formatar_cnae(cnae_obj.codigo),
                    'descricao': cnae_obj.descricao,
                    'itens_ambientais': detalhes_ambientais,
                    'risco_consolidado': risco_texto_cnae,
                    'cor_consolidada': RISCO_CORES.get(risco_texto_cnae, 'secondary')
                })

            except CNAE.DoesNotExist:
                # CNAE não encontrado na base
                pass

        return JsonResponse(resultado_final)

    except Exception as e:
        return JsonResponse({'erro': str(e)}, status=500)

def pagina_simulador_ambiental(request):
    """Renderiza o template do Simulador Ambiental (cópia do sanitário)."""
    return render(request, 'simulador_risco/simulador_ambiental.html', {
        'RECAPTCHA_PUBLIC_KEY': settings.RECAPTCHA_PUBLIC_KEY
    })