import csv
import random
from datetime import datetime, timedelta

# Carregar reservas do arquivo anterior (simulação)
# Na prática, você carregaria do CSV real
reservas_exemplo = [
    {'reserva_id': 1001, 'valor_total': '1500.00', 'status': 'Confirmada'},
    {'reserva_id': 1002, 'valor_total': '1200.00', 'status': 'Cancelada'},
    {'reserva_id': 1003, 'valor_total': '2000.00', 'status': 'Confirmada'},
    {'reserva_id': 1004, 'valor_total': '800.00', 'status': 'Pendente'},
    {'reserva_id': 1005, 'valor_total': '2700.00', 'status': 'Confirmada'}
]

# Formas de pagamento
formas_pagamento = ['Cartão crédito', 'Cartão débito', 'Pix', 'Dinheiro', 'Transferência', 'Boleto']

# Status de pagamento
status_pagamento = ['Pago', 'Não pago', 'Pendente', 'Reembolsado', 'Chargeback']

# Prefixos de notas fiscais por estado
prefixos_nf = {
    1: 'RJ',  # Rio de Janeiro
    2: 'SP',  # São Paulo
    3: 'RS',  # Rio Grande do Sul
    4: 'SC',  # Santa Catarina
    5: 'DF'   # Distrito Federal
}

def calcular_impostos(valor_total):
    """Calcula impostos (aproximadamente 10% do valor total)"""
    impostos = float(valor_total) * 0.10
    return round(impostos, 2)

def gerar_data_cobranca(reserva_id, status_reserva):
    """Gera data de cobrança baseada na reserva e status"""
    # Data base é a data da reserva + alguns dias
    dias_base = reserva_id - 1000  # Usando o ID como base para variação
    
    if status_reserva == 'Confirmada':
        # Cobrança próxima à data da reserva
        dias_ate_cobranca = random.randint(1, 7)
    elif status_reserva == 'Cancelada':
        # Cobrança pode ser antes ou depois, dependendo do cancelamento
        dias_ate_cobranca = random.randint(-3, 5)
    else:  # Pendente
        # Cobrança futura
        dias_ate_cobranca = random.randint(3, 15)
    
    data_base = datetime.now() - timedelta(days=dias_base)
    data_cobranca = data_base + timedelta(days=dias_ate_cobranca)
    return data_cobranca.strftime('%Y-%m-%d')

def gerar_status_pagamento(status_reserva):
    """Gera status de pagamento baseado no status da reserva"""
    if status_reserva == 'Cancelada':
        return random.choice(['Reembolsado', 'Não pago'])
    elif status_reserva == 'Confirmada':
        return random.choices(['Pago', 'Pendente'], weights=[80, 20])[0]
    else:  # Pendente ou outros
        return random.choice(['Pendente', 'Não pago'])

def gerar_nota_fiscal(reserva_id, hotel_id):
    """Gera número de nota fiscal"""
    prefixo = prefixos_nf.get(hotel_id, 'NF')
    numero_base = 12345 + reserva_id
    return f"{prefixo}{numero_base}"

def gerar_forma_pagamento(status_pagamento):
    """Gera forma de pagamento realista baseada no status"""
    if status_pagamento == 'Pago':
        return random.choices(['Cartão crédito', 'Pix', 'Cartão débito', 'Dinheiro'], 
                             weights=[50, 30, 15, 5])[0]
    elif status_pagamento == 'Pendente':
        return random.choice(['Boleto', 'Cartão crédito', 'Pix'])
    else:
        return random.choice(['Cartão crédito', 'Pix', 'Transferência'])

def gerar_faturas(reservas, total_faturas=200):
    """Gera lista de faturas"""
    faturas = []
    
    # Assumindo que temos 200 reservas (de 1001 a 1200)
    for i in range(total_faturas):
        fatura_id = 9001 + i
        reserva_id = 1001 + i
        
        # Simular dados da reserva (na prática, carregaria do CSV)
        valor_total_reserva = random.uniform(500, 5000)
        status_reserva = random.choice(['Confirmada', 'Cancelada', 'Pendente'])
        hotel_id = random.randint(1, 5)
        
        valor_total = round(valor_total_reserva, 2)
        impostos = calcular_impostos(valor_total)
        status_pgto = gerar_status_pagamento(status_reserva)
        forma_pgto = gerar_forma_pagamento(status_pgto)
        data_cobranca = gerar_data_cobranca(reserva_id, status_reserva)
        nota_fiscal = gerar_nota_fiscal(reserva_id, hotel_id)
        
        fatura = {
            'fatura_id': fatura_id,
            'reserva_id': reserva_id,
            'data_cobranca': data_cobranca,
            'valor_total': f"{valor_total:.2f}",
            'impostos': f"{impostos:.2f}",
            'forma_pagamento': forma_pgto,
            'status_pagamento': status_pgto,
            'notas_fiscais': nota_fiscal
        }
        
        faturas.append(fatura)
    
    return faturas

# Gerar as faturas
faturas = gerar_faturas(reservas_exemplo, 200)

# Criar arquivo CSV
with open(r'hotel_chain\staging\faturas.csv', 'w', newline='', encoding='utf-8') as arquivo:
    campos = [
        'fatura_id', 'reserva_id', 'data_cobranca', 'valor_total', 
        'impostos', 'forma_pagamento', 'status_pagamento', 'notas_fiscais'
    ]
    
    writer = csv.DictWriter(arquivo, fieldnames=campos)
    writer.writeheader()
    writer.writerows(faturas)

print("Arquivo 'faturas.csv' criado com sucesso!")
print(f"Total de faturas: {len(faturas)}")

# Estatísticas
faturas_pagas = sum(1 for f in faturas if f['status_pagamento'] == 'Pago')
faturas_pendentes = sum(1 for f in faturas if f['status_pagamento'] == 'Pendente')
faturas_nao_pagas = sum(1 for f in faturas if f['status_pagamento'] == 'Não pago')
faturas_reembolsadas = sum(1 for f in faturas if f['status_pagamento'] == 'Reembolsado')

valor_total_faturado = sum(float(f['valor_total']) for f in faturas if f['status_pagamento'] in ['Pago', 'Pendente'])
valor_total_impostos = sum(float(f['impostos']) for f in faturas)

print(f"\nEstatísticas das faturas:")
print(f"Faturas pagas: {faturas_pagas}")
print(f"Faturas pendentes: {faturas_pendentes}")
print(f"Faturas não pagas: {faturas_nao_pagas}")
print(f"Faturas reembolsadas: {faturas_reembolsadas}")
print(f"Valor total faturado: R$ {valor_total_faturado:,.2f}")
print(f"Valor total em impostos: R$ {valor_total_impostos:,.2f}")

# Distribuição por forma de pagamento
formas_count = {}
for fatura in faturas:
    forma = fatura['forma_pagamento']
    formas_count[forma] = formas_count.get(forma, 0) + 1

print(f"\nDistribuição por forma de pagamento:")
for forma, count in formas_count.items():
    porcentagem = (count / len(faturas)) * 100
    print(f"  {forma}: {count} faturas ({porcentagem:.1f}%)")

# Mostrar primeiros registros como exemplo
print("\nPrimeiros 8 registros:")
print("fatura_id | reserva_id | data_cobranca | valor_total | impostos | forma_pagamento | status_pagamento | notas_fiscais")
for i in range(min(8, len(faturas))):
    f = faturas[i]
    print(f"{f['fatura_id']} | {f['reserva_id']} | {f['data_cobranca']} | {f['valor_total']} | {f['impostos']} | {f['forma_pagamento']} | {f['status_pagamento']} | {f['notas_fiscais']}")