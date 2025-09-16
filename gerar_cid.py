import csv

# Lista de códigos CID-10 (amostra robusta para desenvolvimento)
cid_data = [
    ('A000', 'Cólera devida a Vibrio cholerae 01, biótipo cholerae'),
    ('A010', 'Febre tifóide'),
    ('A020', 'Septicemia por salmonela'),
    ('A150', 'Tuberculose pulmonar, com confirmação bacteriológica e histológica'),
    ('B24', 'Doença pelo vírus da imunodeficiência humana [HIV] não especificada'),
    ('C15', 'Neoplasia maligna do esôfago'),
    ('C34', 'Neoplasia maligna dos brônquios e dos pulmões'),
    ('D500', 'Anemia por deficiência de ferro secundária a perda de sangue (crônica)'),
    ('E10', 'Diabetes mellitus insulino-dependente'),
    ('E11', 'Diabetes mellitus não-insulino-dependente'),
    ('F10', 'Transtornos mentais e comportamentais devidos ao uso de álcool'),
    ('F20', 'Esquizofrenia'),
    ('F32', 'Episódios depressivos'),
    ('G40', 'Epilepsia'),
    ('G43', 'Enxaqueca'),
    ('I10', 'Hipertensão essencial (primária)'),
    ('I21', 'Infarto agudo do miocárdio'),
    ('I25', 'Doença isquêmica crônica do coração'),
    ('I500', 'Insuficiência cardíaca congestiva'),
    ('I64', 'Acidente vascular cerebral, não especificado como hemorrágico ou isquêmico'),
    ('J18', 'Pneumonia por microorganismo não especificado'),
    ('J44', 'Outras doenças pulmonares obstrutivas crônicas'),
    ('J45', 'Asma'),
    ('K25', 'Úlcera gástrica'),
    ('K74', 'Fibrose e cirrose hepáticas'),
    ('L03', 'Celulite'),
    ('M545', 'Dor lombar baixa'),
    ('N18', 'Doença renal crônica'),
    ('O80', 'Parto único espontâneo'),
    ('P07', 'Transtornos relacionados com a gestação de curta duração e com baixo peso ao nascer'),
    ('Q210', 'Defeito do septo ventricular'),
    ('R05', 'Tosse'),
    ('R509', 'Febre, não especificada'),
    ('S060', 'Concussão'),
    ('T20', 'Queimadura e corrosão da cabeça e do pescoço'),
    ('Z380', 'Recém-nascido único, nascido em hospital'),
    # Adicione mais códigos aqui se necessário
]

file_path = 'cid10.csv'
try:
    with open(file_path, mode='w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['codigo', 'descricao'])  # Escreve o cabeçalho
        writer.writerows(cid_data)
    print(f"Arquivo '{file_path}' criado com sucesso com {len(cid_data)} códigos.")
except Exception as e:
    print(f"Ocorreu um erro ao gerar o arquivo: {e}")