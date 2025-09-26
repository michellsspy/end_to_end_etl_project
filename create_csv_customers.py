import csv
import random
from datetime import datetime, timedelta
import names
from faker import Faker

# pip install Faker names

# Configurar Faker para dados em português Brasil
fake = Faker('pt_BR')
fake_internacional = Faker()  # Faker internacional

# Lista de estados brasileiros e suas cidades
estados_cidades = {
    'AC': ['Rio Branco', 'Cruzeiro do Sul', 'Sena Madureira'],
    'AL': ['Maceió', 'Arapiraca', 'Rio Largo'],
    'AP': ['Macapá', 'Santana', 'Laranjal do Jari'],
    'AM': ['Manaus', 'Parintins', 'Itacoatiara'],
    'BA': ['Salvador', 'Feira de Santana', 'Vitória da Conquista'],
    'CE': ['Fortaleza', 'Caucaia', 'Juazeiro do Norte'],
    'DF': ['Brasília'],
    'ES': ['Vitória', 'Vila Velha', 'Cariacica'],
    'GO': ['Goiânia', 'Aparecida de Goiânia', 'Anápolis'],
    'MA': ['São Luís', 'Imperatriz', 'Timon'],
    'MT': ['Cuiabá', 'Várzea Grande', 'Rondonópolis'],
    'MS': ['Campo Grande', 'Dourados', 'Três Lagoas'],
    'MG': ['Belo Horizonte', 'Uberlândia', 'Contagem'],
    'PA': ['Belém', 'Ananindeua', 'Santarém'],
    'PB': ['João Pessoa', 'Campina Grande', 'Santa Rita'],
    'PR': ['Curitiba', 'Londrina', 'Maringá'],
    'PE': ['Recife', 'Jaboatão dos Guararapes', 'Olinda'],
    'PI': ['Teresina', 'Parnaíba', 'Picos'],
    'RJ': ['Rio de Janeiro', 'São Gonçalo', 'Duque de Caxias'],
    'RN': ['Natal', 'Mossoró', 'Parnamirim'],
    'RS': ['Porto Alegre', 'Caxias do Sul', 'Pelotas'],
    'RO': ['Porto Velho', 'Ji-Paraná', 'Ariquemes'],
    'RR': ['Boa Vista', 'Rorainópolis', 'Caracaraí'],
    'SC': ['Florianópolis', 'Joinville', 'Blumenau'],
    'SP': ['São Paulo', 'Guarulhos', 'Campinas'],
    'SE': ['Aracaju', 'Nossa Senhora do Socorro', 'Lagarto'],
    'TO': ['Palmas', 'Araguaína', 'Gurupi']
}

# Lista de países (com maioria brasileira)
paises = ['Brasil'] * 180 + ['Portugal', 'Argentina', 'Estados Unidos', 'Espanha', 
                           'Itália', 'Japão', 'China', 'Chile', 'Uruguai', 'Paraguai',
                           'Alemanha', 'França', 'Reino Unido', 'Canadá', 'Austrália']

# Lista de domínios de email
dominios = ['gmail.com', 'hotmail.com', 'yahoo.com.br', 'outlook.com', 'bol.com.br']

def gerar_cpf():
    """Gera um CPF válido formatado"""
    cpf = [random.randint(0, 9) for _ in range(9)]
    
    for _ in range(2):
        valor = sum([cpf[i] * (10 - i) for i in range(len(cpf))]) % 11
        cpf.append(11 - valor if valor > 1 else 0)
    
    return f"{''.join(map(str, cpf[:3]))}.{''.join(map(str, cpf[3:6]))}.{''.join(map(str, cpf[6:9]))}-{''.join(map(str, cpf[9:]))}"

def gerar_rg():
    """Gera um RG formatado"""
    rg = ''.join([str(random.randint(0, 9)) for _ in range(9)])
    return f"{rg[:2]}.{rg[2:5]}.{rg[5:8]}-{rg[8:]}"

def gerar_telefone():
    """Gera um telefone brasileiro"""
    ddd = random.choice(['11', '21', '31', '41', '51', '61', '71', '81', '91'])
    numero = ''.join([str(random.randint(0, 9)) for _ in range(8)])
    return f"({ddd}) 9{numero[:4]}-{numero[4:]}"

def gerar_telefone_internacional():
    """Gera um telefone internacional"""
    return fake_internacional.phone_number()

def gerar_data_nascimento():
    """Gera uma data de nascimento entre 18 e 80 anos atrás"""
    anos = random.randint(18, 80)
    dias = random.randint(0, 365)
    data_nasc = datetime.now() - timedelta(days=anos*365 + dias)
    return data_nasc.strftime('%d/%m/%Y')

def calcular_idade(data_nascimento):
    """Calcula idade a partir da data de nascimento"""
    nasc = datetime.strptime(data_nascimento, '%d/%m/%Y')
    hoje = datetime.now()
    return hoje.year - nasc.year - ((hoje.month, hoje.day) < (nasc.month, nasc.day))

def gerar_data_cadastro(data_nascimento):
    """Gera data de cadastro (após a maioridade)"""
    nasc = datetime.strptime(data_nascimento, '%d/%m/%Y')
    idade_cadastro = random.randint(18, calcular_idade(data_nascimento))
    dias_pos_maioridade = random.randint(0, (calcular_idade(data_nascimento) - idade_cadastro) * 365)
    data_cadastro = nasc + timedelta(days=idade_cadastro*365 + dias_pos_maioridade)
    return data_cadastro.strftime('%d/%m/%Y')

def gerar_cep_internacional():
    """Gera um CEP/ZIP code internacional"""
    # Formato básico para códigos postais internacionais
    return ''.join([str(random.randint(0, 9)) for _ in range(5)])

# Gerar dados dos clientes
clientes = []

for i in range(300):
    # Informações básicas
    sexo = random.choice(['M', 'F'])
    nome = names.get_full_name(gender='male' if sexo == 'M' else 'female')
    
    # Endereço
    pais = random.choice(paises)
    if pais == 'Brasil':
        estado = random.choice(list(estados_cidades.keys()))
        cidade = random.choice(estados_cidades[estado])
        cep = fake.postcode()
        endereco = fake.street_name()
        bairro = fake.bairro()
        telefone = gerar_telefone()
    else:
        estado = fake_internacional.state_abbr() if random.random() > 0.5 else ''
        cidade = fake_internacional.city()
        cep = gerar_cep_internacional()
        endereco = fake_internacional.street_name()
        bairro = fake_internacional.city_suffix()
        telefone = gerar_telefone_internacional()
    
    # Dados pessoais
    cpf = gerar_cpf()
    rg = gerar_rg()
    data_nascimento = gerar_data_nascimento()
    idade = calcular_idade(data_nascimento)
    data_cadastro = gerar_data_cadastro(data_nascimento)
    
    # Contato
    email = f"{nome.lower().replace(' ', '.')}@{random.choice(dominios)}"
    telefone2 = gerar_telefone() if pais == 'Brasil' and random.random() > 0.3 else gerar_telefone_internacional() if random.random() > 0.3 else ""

    cliente = {
        'id': i + 1,
        'nome_completo': nome,
        'cpf': cpf,
        'identidade': rg,
        'sexo': sexo,
        'data_nascimento': data_nascimento,
        'idade': idade,
        'email': email,
        'telefone_principal': telefone,
        'telefone_secundario': telefone2,
        'pais': pais,
        'estado': estado,
        'cidade': cidade,
        'cep': cep,
        'endereco': endereco,
        'numero': random.randint(1, 9999),
        'complemento': random.choice(['', 'Apto 101', 'Casa 2', 'Sala 303', 'Bloco B']),
        'bairro': bairro,
        'data_cadastro': data_cadastro,
        'status': random.choice(['Ativo', 'Inativo', 'Pendente']),
        'tipo_cliente': random.choice(['VIP', 'Regular', 'Premium', 'Novo']),
        'ultima_compra': fake.date_between(start_date='-2y', end_date='today').strftime('%d/%m/%Y') if random.random() > 0.2 else '',
        'valor_total_compras': round(random.uniform(0, 50000), 2),
        'categoria_favorita': random.choice(['Eletrônicos', 'Roupas', 'Casa', 'Esportes', 'Livros', 'Beleza']),
        'newsletter': random.choice(['Sim', 'Não'])
    }
    
    clientes.append(cliente)

# Criar arquivo CSV
with open('clientes.csv', 'w', newline='', encoding='utf-8') as arquivo:
    campos = [
        'id', 'nome_completo', 'cpf', 'identidade', 'sexo', 'data_nascimento', 'idade',
        'email', 'telefone_principal', 'telefone_secundario', 'pais', 'estado', 'cidade',
        'cep', 'endereco', 'numero', 'complemento', 'bairro', 'data_cadastro', 'status',
        'tipo_cliente', 'ultima_compra', 'valor_total_compras', 'categoria_favorita', 'newsletter'
    ]
    
    writer = csv.DictWriter(arquivo, fieldnames=campos)
    writer.writeheader()
    writer.writerows(clientes)

print("Arquivo 'clientes.csv' criado com sucesso!")
print(f"Total de registros: {len(clientes)}")
print("Primeiras linhas do arquivo:")
for i in range(min(3, len(clientes))):
    print(f"ID {clientes[i]['id']}: {clientes[i]['nome_completo']} - {clientes[i]['cidade']}/{clientes[i]['estado']}")