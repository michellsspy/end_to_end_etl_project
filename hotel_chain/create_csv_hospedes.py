import csv
import random
from datetime import datetime, timedelta
import names
from faker import Faker

# Configurar Faker
fake = Faker()

# Lista de nacionalidades para hotelaria
nacionalidades = [
    'Brasil', 'Portugal', 'Argentina', 'Estados Unidos', 'Espanha', 
    'Itália', 'França', 'Alemanha', 'Reino Unido', 'Canadá', 
    'Japão', 'China', 'Austrália', 'Chile', 'Uruguai', 'Índia',
    'México', 'Colômbia', 'Peru', 'Rússia', 'África do Sul'
]

# Tipos de cliente para hotelaria
tipos_cliente = ['Recorrente', 'Novo', 'VIP', 'Premium', 'Corporativo']

def gerar_data_nascimento():
    """Gera uma data de nascimento entre 18 e 80 anos atrás"""
    anos = random.randint(18, 80)
    dias = random.randint(0, 365)
    data_nasc = datetime.now() - timedelta(days=anos*365 + dias)
    return data_nasc.strftime('%Y-%m-%d')

def gerar_telefone(nacionalidade):
    """Gera telefone no formato internacional baseado na nacionalidade"""
    codigos_paises = {
        'Brasil': ('+55', '(XX) 9XXXX-XXXX'),
        'Portugal': ('+351', 'XXXXX XXXX'),
        'Argentina': ('+54', '(XX) XXXX-XXXX'),
        'Estados Unidos': ('+1', '(XXX) XXX-XXXX'),
        'Espanha': ('+34', 'XXX XXX XXX'),
        'Itália': ('+39', 'XXX XXX XXXX'),
        'França': ('+33', 'X XX XX XX XX'),
        'Alemanha': ('+49', 'XXXX XXXX'),
        'Reino Unido': ('+44', 'XXXX XXX XXX'),
        'Canadá': ('+1', '(XXX) XXX-XXXX'),
        'Japão': ('+81', 'XX XXXX XXXX'),
        'China': ('+86', 'XXX XXXX XXXX'),
        'Austrália': ('+61', 'X XXXX XXXX'),
        'Chile': ('+56', 'X XXXX XXXX'),
        'Uruguai': ('+598', 'X XXX XX XX'),
        'Índia': ('+91', 'XXXXX XXXXX'),
        'México': ('+52', 'XXX XXX XXXX'),
        'Colômbia': ('+57', 'XXX XXX XXXX'),
        'Peru': ('+51', 'XXX XXX XXX'),
        'Rússia': ('+7', 'XXX XXX-XX-XX'),
        'África do Sul': ('+27', 'XX XXX XXXX')
    }
    
    codigo, formato = codigos_paises.get(nacionalidade, ('+55', '(XX) 9XXXX-XXXX'))
    
    # Gerar números aleatórios baseado no formato
    numero = ''.join([str(random.randint(0, 9)) if c == 'X' else c for c in formato])
    return f"{codigo} {numero}"

def gerar_email(nome, nacionalidade):
    """Gera email baseado no nome e nacionalidade"""
    nome_formatado = nome.lower().replace(' ', '.')
    dominios = {
        'Brasil': ['gmail.com', 'hotmail.com', 'outlook.com', 'yahoo.com.br'],
        'Portugal': ['gmail.com', 'sapo.pt', 'mail.pt', 'outlook.pt'],
        'Estados Unidos': ['gmail.com', 'yahoo.com', 'outlook.com', 'aol.com'],
        'Espanha': ['gmail.com', 'hotmail.es', 'outlook.es', 'yahoo.es'],
        'França': ['gmail.com', 'orange.fr', 'outlook.fr', 'yahoo.fr'],
        'Alemanha': ['gmail.com', 'web.de', 'outlook.de', 'yahoo.de'],
        'Reino Unido': ['gmail.com', 'outlook.com', 'yahoo.co.uk', 'aol.com'],
        'Japão': ['gmail.com', 'yahoo.co.jp', 'outlook.jp', 'docomo.ne.jp'],
        'China': ['gmail.com', 'qq.com', '163.com', 'sina.com']
    }
    
    dominio = random.choice(dominios.get(nacionalidade, ['gmail.com', 'outlook.com', 'yahoo.com']))
    return f"{nome_formatado}@{dominio}"

# Gerar dados dos hóspedes
hospedes = []

for i in range(200):
    sexo = random.choice(['M', 'F'])
    nacionalidade = random.choice(nacionalidades)
    
    # Gerar nome apropriado para a nacionalidade
    if nacionalidade == 'Brasil':
        nome = fake.name_male() if sexo == 'M' else fake.name_female()
    elif nacionalidade == 'Portugal':
        nomes_m = ['João', 'Pedro', 'Carlos', 'Miguel', 'António']
        nomes_f = ['Maria', 'Ana', 'Sofia', 'Inês', 'Catarina']
        sobrenomes = ['Silva', 'Santos', 'Ferreira', 'Oliveira', 'Costa']
        nome = f"{random.choice(nomes_m if sexo == 'M' else nomes_f)} {random.choice(sobrenomes)}"
    elif nacionalidade == 'Índia':
        nomes_m = ['Raj', 'Amit', 'Sanjay', 'Vikram', 'Arjun']
        nomes_f = ['Priya', 'Anita', 'Sunita', 'Meera', 'Kavita']
        sobrenomes = ['Sharma', 'Patel', 'Kumar', 'Singh', 'Gupta']
        nome = f"{random.choice(nomes_m if sexo == 'M' else nomes_f)} {random.choice(sobrenomes)}"
    else:
        nome = names.get_full_name(gender='male' if sexo == 'M' else 'female')
    
    hospede = {
        'hóspede_id': i + 1,
        'nome': nome,
        'data_nascimento': gerar_data_nascimento(),
        'sexo': sexo,
        'nacionalidade': nacionalidade,
        'tipo_cliente': random.choice(tipos_cliente),
        'email': gerar_email(nome, nacionalidade),
        'telefone': gerar_telefone(nacionalidade)
    }
    
    hospedes.append(hospede)

# Criar arquivo CSV
with open(r'hotel_chain\staging\hospedes.csv', 'w', newline='', encoding='utf-8') as arquivo:
    campos = ['hóspede_id', 'nome', 'data_nascimento', 'sexo', 'nacionalidade', 'tipo_cliente', 'email', 'telefone']
    
    writer = csv.DictWriter(arquivo, fieldnames=campos)
    writer.writeheader()
    writer.writerows(hospedes)

print("Arquivo 'hospedes.csv' criado com sucesso!")
print(f"Total de registros: {len(hospedes)}")

# Mostrar primeiros registros como exemplo
print("\nPrimeiros 5 registros:")
print("hóspede_id\tnome\t\tdata_nascimento\tsexo\tnacionalidade\ttipo_cliente\temail\ttelefone")
for i in range(5):
    h = hospedes[i]
    print(f"{h['hóspede_id']}\t\t{h['nome']}\t{h['data_nascimento']}\t{h['sexo']}\t{h['nacionalidade']}\t{h['tipo_cliente']}\t{h['email']}\t{h['telefone']}")