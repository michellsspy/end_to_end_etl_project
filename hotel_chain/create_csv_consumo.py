import csv
import random
from datetime import datetime, timedelta

# Serviços disponíveis no hotel
servicos_hotel = {
    'Restaurante': {
        'itens': [
            {'descricao': 'Café da manhã', 'valor_min': 25.00, 'valor_max': 45.00},
            {'descricao': 'Almoço executivo', 'valor_min': 45.00, 'valor_max': 75.00},
            {'descricao': 'Jantar à la carte', 'valor_min': 80.00, 'valor_max': 150.00},
            {'descricao': 'Room service - jantar', 'valor_min': 60.00, 'valor_max': 120.00},
            {'descricao': 'Buffet completo', 'valor_min': 90.00, 'valor_max': 130.00}
        ]
    },
    'Bar': {
        'itens': [
            {'descricao': 'Drinks especiais', 'valor_min': 25.00, 'valor_max': 45.00},
            {'descricao': 'Vinho taça', 'valor_min': 30.00, 'valor_max': 60.00},
            {'descricao': 'Cervejas importadas', 'valor_min': 15.00, 'valor_max': 30.00},
            {'descricao': 'Coquetéis', 'valor_min': 35.00, 'valor_max': 55.00},
            {'descricao': 'Sucos naturais', 'valor_min': 12.00, 'valor_max': 20.00}
        ]
    },
    'Spa': {
        'itens': [
            {'descricao': 'Massagem relaxante', 'valor_min': 150.00, 'valor_max': 250.00},
            {'descricao': 'Tratamento facial', 'valor_min': 120.00, 'valor_max': 200.00},
            {'descricao': 'Day use spa', 'valor_min': 200.00, 'valor_max': 350.00},
            {'descricao': 'Massagem terapêutica', 'valor_min': 180.00, 'valor_max': 280.00},
            {'descricao': 'Pacote completo', 'valor_min': 300.00, 'valor_max': 500.00}
        ]
    },
    'Lavanderia': {
        'itens': [
            {'descricao': 'Lavagem roupa', 'valor_min': 40.00, 'valor_max': 80.00},
            {'descricao': 'Passagem roupa', 'valor_min': 25.00, 'valor_max': 50.00},
            {'descricao': 'Lavagem urgente', 'valor_min': 60.00, 'valor_max': 100.00},
            {'descricao': 'Lavagem a seco', 'valor_min': 35.00, 'valor_max': 70.00}
        ]
    },
    'Estacionamento': {
        'itens': [
            {'descricao': 'Diária estacionamento', 'valor_min': 30.00, 'valor_max': 50.00},
            {'descricao': 'Estacionamento por hora', 'valor_min': 10.00, 'valor_max': 15.00},
            {'descricao': 'Valet service', 'valor_min': 20.00, 'valor_max': 40.00}
        ]
    },
    'Business Center': {
        'itens': [
            {'descricao': 'Impressão página', 'valor_min': 2.00, 'valor_max': 5.00},
            {'descricao': 'Uso computador/hora', 'valor_min': 25.00, 'valor_max': 45.00},
            {'descricao': 'Reunião sala', 'valor_min': 100.00, 'valor_max': 200.00},
            {'descricao': 'Serviço secretária', 'valor_min': 50.00, 'valor_max': 100.00}
        ]
    }
}

# Períodos de consumo baseados em datas de check-in das reservas
def gerar_data_consumo(reserva_id):
    """Gera data de consumo baseada na reserva"""
    # Simula que o consumo ocorre durante a estadia
    dias_apos_checkin = random.randint(0, 7)  # Consumo em até 7 dias após check-in
    data_base = datetime.now() - timedelta(days=random.randint(1, 60))
    data_consumo = data_base + timedelta(days=dias_apos_checkin)
    return data_consumo.strftime('%Y-%m-%d')

def gerar_consumo_servico():
    """Gera um consumo de serviço aleatório"""
    tipo_servico = random.choice(list(servicos_hotel.keys()))
    item = random.choice(servicos_hotel[tipo_servico]['itens'])
    
    valor = round(random.uniform(item['valor_min'], item['valor_max']), 2)
    
    # Probabilidade de pagamento: 80% pago, 20% não pago
    pago = random.choices(['Sim', 'Não'], weights=[80, 20])[0]
    
    return tipo_servico, item['descricao'], valor, pago

def gerar_consumos(total_consumos=300):
    """Gera lista de consumos dos hóspedes"""
    consumos = []
    
    # Simular hóspedes ativos (com reservas recentes)
    hospedes_ativos = list(range(1, 201))  # 200 hóspedes possíveis
    quartos_ativos = list(range(101, 500))  # Quartos possíveis
    
    for i in range(total_consumos):
        consumo_id = 5001 + i
        
        # Um hóspede pode ter múltiplos consumos
        hospede_id = random.choice(hospedes_ativos)
        quarto_id = random.choice(quartos_ativos)
        
        data_consumo = gerar_data_consumo(hospede_id)
        tipo_servico, descricao, valor, pago = gerar_consumo_servico()
        
        consumo = {
            'consumo_id': consumo_id,
            'hóspede_id': hospede_id,
            'quarto_id': quarto_id,
            'data_consumo': data_consumo,
            'tipo_servico': tipo_servico,
            'descricao': descricao,
            'valor': f"{valor:.2f}",
            'pago': pago
        }
        
        consumos.append(consumo)
    
    return consumos

# Gerar os consumos
consumos = gerar_consumos(300)

# Criar arquivo CSV
with open(r'hotel_chain\staging\consumos.csv', 'w', newline='', encoding='utf-8') as arquivo:
    campos = [
        'consumo_id', 'hóspede_id', 'quarto_id', 'data_consumo', 
        'tipo_servico', 'descricao', 'valor', 'pago'
    ]
    
    writer = csv.DictWriter(arquivo, fieldnames=campos)
    writer.writeheader()
    writer.writerows(consumos)

print("Arquivo 'consumos.csv' criado com sucesso!")
print(f"Total de consumos: {len(consumos)}")

# Estatísticas
print(f"\nEstatísticas dos consumos:")

# Por tipo de serviço
servicos_count = {}
valor_total_servicos = {}
for consumo in consumos:
    servico = consumo['tipo_servico']
    servicos_count[servico] = servicos_count.get(servico, 0) + 1
    valor_total_servicos[servico] = valor_total_servicos.get(servico, 0) + float(consumo['valor'])

print(f"\nDistribuição por tipo de serviço:")
for servico, count in servicos_count.items():
    valor_total = valor_total_servicos[servico]
    porcentagem = (count / len(consumos)) * 100
    print(f"  {servico}: {count} consumos ({porcentagem:.1f}%) - R$ {valor_total:,.2f}")

# Status de pagamento
pagos = sum(1 for c in consumos if c['pago'] == 'Sim')
nao_pagos = sum(1 for c in consumos if c['pago'] == 'Não')
valor_total_pago = sum(float(c['valor']) for c in consumos if c['pago'] == 'Sim')
valor_total_nao_pago = sum(float(c['valor']) for c in consumos if c['pago'] == 'Não')

print(f"\nStatus de pagamento:")
print(f"  Consumos pagos: {pagos} ({pagos/len(consumos)*100:.1f}%) - R$ {valor_total_pago:,.2f}")
print(f"  Consumos não pagos: {nao_pagos} ({nao_pagos/len(consumos)*100:.1f}%) - R$ {valor_total_nao_pago:,.2f}")

# Top 5 consumos mais caros
consumos_ordenados = sorted(consumos, key=lambda x: float(x['valor']), reverse=True)
print(f"\nTop 5 consumos mais caros:")
for i in range(min(5, len(consumos_ordenados))):
    c = consumos_ordenados[i]
    print(f"  Consumo {c['consumo_id']}: {c['tipo_servico']} - {c['descricao']} - R$ {c['valor']}")

# Mostrar primeiros registros como exemplo
print("\nPrimeiros 10 registros:")
print("consumo_id | hóspede_id | quarto_id | data_consumo | tipo_servico | descricao | valor | pago")
for i in range(min(10, len(consumos))):
    c = consumos[i]
    print(f"{c['consumo_id']} | {c['hóspede_id']} | {c['quarto_id']} | {c['data_consumo']} | {c['tipo_servico']} | {c['descricao']} | {c['valor']} | {c['pago']}")

# Exemplos de consumos por serviço
print("\nExemplos de consumos por tipo de serviço:")
tipos_exibidos = set()
for consumo in consumos:
    if consumo['tipo_servico'] not in tipos_exibidos:
        print(f"  {consumo['tipo_servico']}: {consumo['descricao']} - R$ {consumo['valor']} ({consumo['pago']})")
        tipos_exibidos.add(consumo['tipo_servico'])
    if len(tipos_exibidos) == len(servicos_hotel):
        break