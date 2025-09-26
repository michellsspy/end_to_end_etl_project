import csv
import random
from datetime import datetime, timedelta
import names
from faker import Faker

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

# Lista de países (hotelaria tem mais clientes internacionais)
paises = ['Brasil'] * 120 + ['Portugal', 'Argentina', 'Estados Unidos', 'Espanha', 
                           'Itália', 'França', 'Alemanha', 'Reino Unido', 'Canadá', 
                           'Chile', 'Uruguai', 'Paraguai', 'Japão', 'China', 'Austrália'] * 5

# Tipos de documentos internacionais
documentos_internacionais = ['Passaporte', 'Documento de Identidade Estrangeiro', 'Carteira de Motorista Internacional']

def gerar_cpf():
    """Gera um CPF válido formatado"""
    cpf = [random.randint(0, 9) for _ in range(9)]
    
    for _ in range(2):
        valor = sum([cpf[i] * (10 - i) for i in range(len(cpf))]) % 11
        cpf.append(11 - valor if valor > 1 else 0)
    
    return f"{''.join(map(str, cpf[:3]))}.{''.join(map(str, cpf[3:6]))}.{''.join(map(str, cpf[6:9]))}-{''.join(map(str, cpf[9:]))}"

def gerar_passaporte():
    """Gera um número de passaporte"""
    letras = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=2))
    numeros = ''.join(random.choices('0123456789', k=7))
    return f"{letras}{numeros}"

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

def gerar_data_ultima_hospedagem():
    """Gera data da última hospedagem"""
    dias = random.randint(1, 730)  # Últimos 2 anos
    data = datetime.now() - timedelta(days=dias)
    return data.strftime('%d/%m/%Y')

def gerar_data_proxima_reserva():
    """Gera data para próxima reserva (apenas para alguns clientes)"""
    if random.random() > 0.7:  # 30% dos clientes têm próxima reserva
        dias = random.randint(1, 180)  # Próximos 6 meses
        data = datetime.now() + timedelta(days=dias)
        return data.strftime('%d/%m/%Y')
    return ''

def gerar_cep_internacional():
    """Gera um CEP/ZIP code internacional"""
    return ''.join([str(random.randint(0, 9)) for _ in range(5)])

# Dados específicos de hotelaria
tipos_quarto = ['Standard', 'Luxo', 'Suíte Junior', 'Suíte Master', 'Suíte Presidencial']
preferencias_hospedagem = ['Cama de Casal', 'Camas Separadas', 'Andar Alto', 'Andar Baixo', 'Fumante', 'Não Fumante']
meios_transporte = ['Avião', 'Carro Próprio', 'Ônibus', 'Táxi', 'Uber', 'Trem']
motivos_viagem = ['Lazer', 'Negócios', 'Evento Familiar', 'Congresso', 'Turismo', 'Trânsito']
companhias_aereas = ['LATAM', 'GOL', 'Azul', 'American Airlines', 'Delta', 'Air France', 'Lufthansa']

# Gerar dados dos clientes do hotel
clientes_hotel = []

for i in range(200):
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
        documento = gerar_cpf()
        tipo_documento = 'CPF'
    else:
        estado = fake_internacional.state_abbr() if random.random() > 0.5 else ''
        cidade = fake_internacional.city()
        cep = gerar_cep_internacional()
        endereco = fake_internacional.street_name()
        bairro = fake_internacional.city_suffix()
        telefone = gerar_telefone_internacional()
        documento = gerar_passaporte()
        tipo_documento = random.choice(documentos_internacionais)
    
    # Dados pessoais
    data_nascimento = gerar_data_nascimento()
    idade = calcular_idade(data_nascimento)
    data_cadastro = gerar_data_ultima_hospedagem()  # Cadastro na última hospedagem
    
    # Informações específicas do hotel
    total_hospedagens = random.randint(1, 20)
    data_ultima_hospedagem = gerar_data_ultima_hospedagem()
    data_proxima_reserva = gerar_data_proxima_reserva()
    nivel_fidelidade = random.choice(['Bronze', 'Prata', 'Ouro', 'Platina', 'Diamante'])
    
    cliente_hotel = {
        'id_cliente': i + 1,
        'nome_completo': nome,
        'sexo': sexo,
        'data_nascimento': data_nascimento,
        'idade': idade,
        'email': f"{nome.lower().replace(' ', '.')}@example.com",
        'telefone': telefone,
        'telefone_emergencia': gerar_telefone_internacional() if random.random() > 0.5 else '',
        
        # Documentação
        'tipo_documento': tipo_documento,
        'numero_documento': documento,
        'passaporte': gerar_passaporte() if pais != 'Brasil' else '',
        
        # Endereço
        'pais': pais,
        'estado': estado,
        'cidade': cidade,
        'cep': cep,
        'endereco': endereco,
        'numero': random.randint(1, 9999),
        'complemento': random.choice(['', 'Apto 101', 'Casa 2', 'Sala 303', 'Bloco B']),
        
        # Informações de hospedagem
        'data_cadastro_hotel': data_cadastro,
        'total_hospedagens': total_hospedagens,
        'noites_total': total_hospedagens * random.randint(1, 10),
        'data_ultima_hospedagem': data_ultima_hospedagem,
        'data_proxima_reserva': data_proxima_reserva,
        'nivel_fidelidade': nivel_fidelidade,
        
        # Preferências
        'tipo_quarto_preferido': random.choice(tipos_quarto),
        'preferencia_alimentacao': random.choice(['Vegetariano', 'Vegano', 'Sem Restrições', 'Sem Glúten', 'Low Carb']),
        'preferencia_hospedagem': random.choice(preferencias_hospedagem),
        
        # Informações da viagem
        'motivo_viagem': random.choice(motivos_viagem),
        'meio_transporte': random.choice(meios_transporte),
        'companhia_aerea': random.choice(companhias_aereas) if random.random() > 0.5 else '',
        'numero_voo': f"{random.choice(['LA', 'G3', 'AD', 'AA'])}{random.randint(1000, 9999)}" if random.random() > 0.5 else '',
        
        # Dados comerciais
        'valor_total_gasto': round(total_hospedagens * random.uniform(500, 5000), 2),
        'status_cliente': random.choice(['Ativo', 'Inativo', 'Premium', 'VIP']),
        'newsletter': random.choice(['Sim', 'Não']),
        'aceita_marketing': random.choice(['Sim', 'Não']),
        
        # Observações
        'observacoes': random.choice(['', 'Cliente preferencial', 'Alergia a frutos do mar', 'Aniversariante do mês', ''])
    }
    
    clientes_hotel.append(cliente_hotel)

# Criar arquivo CSV
with open('clientes_hotel.csv', 'w', newline='', encoding='utf-8') as arquivo:
    campos = [
        'id_cliente', 'nome_completo', 'sexo', 'data_nascimento', 'idade', 'email', 
        'telefone', 'telefone_emergencia', 'tipo_documento', 'numero_documento', 
        'passaporte', 'pais', 'estado', 'cidade', 'cep', 'endereco', 'numero', 
        'complemento', 'data_cadastro_hotel', 'total_hospedagens', 'noites_total',
        'data_ultima_hospedagem', 'data_proxima_reserva', 'nivel_fidelidade',
        'tipo_quarto_preferido', 'preferencia_alimentacao', 'preferencia_hospedagem',
        'motivo_viagem', 'meio_transporte', 'companhia_aerea', 'numero_voo',
        'valor_total_gasto', 'status_cliente', 'newsletter', 'aceita_marketing', 'observacoes'
    ]
    
    writer = csv.DictWriter(arquivo, fieldnames=campos)
    writer.writeheader()
    writer.writerows(clientes_hotel)

print("Arquivo 'clientes_hotel.csv' criado com sucesso!")
print(f"Total de registros: {len(clientes_hotel)}")
print("\nCampos específicos de hotelaria incluídos:")
print("✅ Documentação (CPF/Passaporte)")
print("✅ Histórico de hospedagens")
print("✅ Preferências de quarto e alimentação")
print("✅ Informações de viagem")
print("✅ Programa de fidelidade")
print("✅ Dados de reservas (última/próxima)")
print("✅ Observações específicas")

# Estatísticas básicas
hospedagens_total = sum(cliente['total_hospedagens'] for cliente in clientes_hotel)
clientes_internacionais = sum(1 for cliente in clientes_hotel if cliente['pais'] != 'Brasil')
clientes_com_reserva = sum(1 for cliente in clientes_hotel if cliente['data_proxima_reserva'] != '')

print(f"\nEstatísticas:")
print(f"Total de hospedagens registradas: {hospedagens_total}")
print(f"Clientes internacionais: {clientes_internacionais}")
print(f"Clientes com próxima reserva: {clientes_com_reserva}")