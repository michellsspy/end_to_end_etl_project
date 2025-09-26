import csv
import random

# Dados dos hotéis
hoteis = [
    {'hotel_id': 1, 'nome': 'Hotel Praia Dourada', 'cidade': 'Rio de Janeiro', 'andares': 8, 'quartos_por_andar': 20},
    {'hotel_id': 2, 'nome': 'Hotel Business Center', 'cidade': 'São Paulo', 'andares': 12, 'quartos_por_andar': 15},
    {'hotel_id': 3, 'nome': 'Mountain Resort', 'cidade': 'Gramado', 'andares': 4, 'quartos_por_andar': 25},
    {'hotel_id': 4, 'nome': 'Beach Paradise', 'cidade': 'Florianópolis', 'andares': 6, 'quartos_por_andar': 18},
    {'hotel_id': 5, 'nome': 'Capital Suites', 'cidade': 'Brasília', 'andares': 10, 'quartos_por_andar': 12}
]

# Tipos de quarto com suas características
tipos_quarto = {
    'Standard': {
        'capacidade': [1, 2],
        'faixa_preco': [250.00, 400.00],
        'descricao': 'Quarto padrão com cama de casal ou duas camas de solteiro'
    },
    'Luxo': {
        'capacidade': [2, 3],
        'faixa_preco': [450.00, 650.00],
        'descricao': 'Quarto espaçoso com amenities premium'
    },
    'Suíte': {
        'capacidade': [2, 4],
        'faixa_preco': [600.00, 900.00],
        'descricao': 'Suíte com área de estar separada'
    },
    'Suíte Master': {
        'capacidade': [3, 4],
        'faixa_preco': [800.00, 1200.00],
        'descricao': 'Suíte master com hidromassagem'
    },
    'Suíte Presidencial': {
        'capacidade': [4, 6],
        'faixa_preco': [1500.00, 3000.00],
        'descricao': 'Suíte presidencial com todos os luxos'
    }
}

# Status possíveis para os quartos
status_quarto = ['Disponível', 'Ocupado', 'Manutenção', 'Limpeza', 'Reservado']

# Características especiais por andar
caracteristicas_andar = {
    1: ['Vista jardim', 'Acesso fácil'],
    2: ['Vista lateral', 'Silencioso'],
    3: ['Vista parcial', 'Andar intermediário'],
    4: ['Vista boa', 'Localização central'],
    5: ['Vista excelente', 'Andar alto'],
    6: ['Vista panorâmica', 'Privacidade'],
    7: ['Vista premium', 'Andar executivo'],
    8: ['Vista superior', 'Andar topo'],
    9: ['Vista cidade', 'Andar corporativo'],
    10: ['Vista completa', 'Andar premium'],
    11: ['Vista espetacular', 'Andar VIP'],
    12: ['Vista 360°', 'Andar presidencial']
}

def gerar_quartos():
    """Gera a lista de quartos para todos os hotéis"""
    quartos = []
    quarto_id_counter = 100  # Começa a numeração a partir de 100
    
    for hotel in hoteis:
        hotel_id = hotel['hotel_id']
        andares = hotel['andares']
        quartos_por_andar = hotel['quartos_por_andar']
        
        # Distribuição dos tipos de quarto por andar
        distribuicao_tipos = {
            'Standard': 0.50,  # 50% dos quartos
            'Luxo': 0.25,      # 25% dos quartos
            'Suíte': 0.15,     # 15% dos quartos
            'Suíte Master': 0.07,  # 7% dos quartos
            'Suíte Presidencial': 0.03  # 3% dos quartos
        }
        
        quarto_numero = 1
        
        for andar in range(1, andares + 1):
            quartos_no_andar = []
            
            # Determinar quantos quartos de cada tipo neste andar
            total_quartos_andar = quartos_por_andar
            quartos_standard = int(total_quartos_andar * distribuicao_tipos['Standard'])
            quartos_luxo = int(total_quartos_andar * distribuicao_tipos['Luxo'])
            quartos_suite = int(total_quartos_andar * distribuicao_tipos['Suíte'])
            quartos_master = int(total_quartos_andar * distribuicao_tipos['Suíte Master'])
            quartos_presidencial = int(total_quartos_andar * distribuicao_tipos['Suíte Presidencial'])
            
            # Ajustar para totalizar o número correto
            total_atual = quartos_standard + quartos_luxo + quartos_suite + quartos_master + quartos_presidencial
            if total_atual < total_quartos_andar:
                quartos_standard += total_quartos_andar - total_atual
            
            # Adicionar quartos Standard
            for _ in range(quartos_standard):
                quartos_no_andar.append('Standard')
            
            # Adicionar quartos Luxo (andares mais altos têm mais quartos luxo)
            if andar >= 3:
                for _ in range(quartos_luxo):
                    quartos_no_andar.append('Luxo')
            
            # Adicionar Suítes (andares mais altos)
            if andar >= 5:
                for _ in range(quartos_suite):
                    quartos_no_andar.append('Suíte')
            
            # Adicionar Suítes Master (andares altos)
            if andar >= 7:
                for _ in range(quartos_master):
                    quartos_no_andar.append('Suíte Master')
            
            # Adicionar Suítes Presidenciais (últimos andares)
            if andar >= andares - 1:
                for _ in range(quartos_presidencial):
                    quartos_no_andar.append('Suíte Presidencial')
            
            # Embaralhar a distribuição no andar
            random.shuffle(quartos_no_andar)
            
            # Criar quartos para este andar
            for tipo in quartos_no_andar:
                quarto_id = andar * 100 + quarto_numero
                quarto_numero += 1
                
                # Capacidade baseada no tipo
                capacidade_min, capacidade_max = tipos_quarto[tipo]['capacidade']
                capacidade = random.randint(capacidade_min, capacidade_max)
                
                # Preço base baseado no tipo e andar (andares mais altos são mais caros)
                preco_min, preco_max = tipos_quarto[tipo]['faixa_preco']
                preco_base = random.uniform(preco_min, preco_max)
                preco_base += (andar - 1) * 10  # Acréscimo por andar
                
                # Status do quarto (maior probabilidade de disponível)
                pesos_status = [70, 15, 8, 5, 2]  # Probabilidades relativas
                status = random.choices(status_quarto, weights=pesos_status)[0]
                
                quarto = {
                    'quarto_id': quarto_id,
                    'hotel_id': hotel_id,
                    'tipo_quarto': tipo,
                    'capacidade': capacidade,
                    'andar': andar,
                    'status_quarto': status,
                    'preco_base': f"{preco_base:.2f}"
                }
                
                quartos.append(quarto)
    
    return quartos

# Gerar os quartos
quartos = gerar_quartos()

# Criar arquivo CSV
with open(r'hotel_chain\staging\quartos.csv', 'w', newline='', encoding='utf-8') as arquivo:
    campos = ['quarto_id', 'hotel_id', 'tipo_quarto', 'capacidade', 'andar', 'status_quarto', 'preco_base']
    
    writer = csv.DictWriter(arquivo, fieldnames=campos)
    writer.writeheader()
    writer.writerows(quartos)

print("Arquivo 'quartos.csv' criado com sucesso!")
print(f"Total de quartos: {len(quartos)}")

# Estatísticas
print(f"\nEstatísticas dos quartos:")
for hotel in hoteis:
    quartos_hotel = [q for q in quartos if q['hotel_id'] == hotel['hotel_id']]
    print(f"\n{hotel['nome']} ({hotel['cidade']}):")
    print(f"  Total de quartos: {len(quartos_hotel)}")
    
    # Contar por tipo
    tipos_count = {}
    for quarto in quartos_hotel:
        tipo = quarto['tipo_quarto']
        tipos_count[tipo] = tipos_count.get(tipo, 0) + 1
    
    for tipo, count in tipos_count.items():
        print(f"  {tipo}: {count} quartos")

# Mostrar primeiros registros como exemplo
print("\nPrimeiros 10 registros:")
print("quarto_id | hotel_id | tipo_quarto | capacidade | andar | status_quarto | preco_base")
for i in range(min(10, len(quartos))):
    q = quartos[i]
    print(f"{q['quarto_id']} | {q['hotel_id']} | {q['tipo_quarto']} | {q['capacidade']} | {q['andar']} | {q['status_quarto']} | {q['preco_base']}")

# Mostrar alguns quartos de exemplo de cada tipo
print("\nExemplos de quartos por tipo:")
tipos_exibidos = set()
for quarto in quartos:
    if quarto['tipo_quarto'] not in tipos_exibidos:
        print(f"Quarto {quarto['quarto_id']} - {quarto['tipo_quarto']} (Hotel {quarto['hotel_id']}, Andar {quarto['andar']}): R$ {quarto['preco_base']} - {quarto['status_quarto']}")
        tipos_exibidos.add(quarto['tipo_quarto'])
    if len(tipos_exibidos) == len(tipos_quarto):
        break