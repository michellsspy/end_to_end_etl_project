import csv
import random
from datetime import datetime, timedelta

# OTAs (Online Travel Agencies) com suas comissões típicas
otas = [
    {'nome': 'Booking', 'comissao_min': 12.0, 'comissao_max': 18.0, 'prefixo': 'BK'},
    {'nome': 'Expedia', 'comissao_min': 15.0, 'comissao_max': 20.0, 'prefixo': 'EX'},
    {'nome': 'Airbnb', 'comissao_min': 10.0, 'comissao_max': 15.0, 'prefixo': 'AB'},
    {'nome': 'Decolar', 'comissao_min': 12.0, 'comissao_max': 16.0, 'prefixo': 'DE'},
    {'nome': 'CVC', 'comissao_min': 8.0, 'comissao_max': 12.0, 'prefixo': 'CV'},
    {'nome': 'Tripadvisor', 'comissao_min': 13.0, 'comissao_max': 17.0, 'prefixo': 'TA'},
    {'nome': 'Hotels.com', 'comissao_min': 14.0, 'comissao_max': 19.0, 'prefixo': 'HO'},
    {'nome': 'Trivago', 'comissao_min': 11.0, 'comissao_max': 15.0, 'prefixo': 'TR'}
]

# Canais diretos (sem comissão)
canais_diretos = ['Site', 'Telefone', 'WhatsApp', 'Presencial', 'Email']

def calcular_comissao_por_tipo_quarto(tipo_quarto):
    """Calcula comissão ajustada por tipo de quarto"""
    ajustes = {
        'Standard': 0.0,      # Comissão padrão
        'Luxo': 1.0,          # +1% para quartos de luxo
        'Suíte': 2.0,         # +2% para suítes
        'Suíte Master': 3.0,  # +3% para suítes master
        'Suíte Presidencial': 4.0  # +4% para suítes presidenciais
    }
    return ajustes.get(tipo_quarto, 0.0)

def gerar_reserva_ota(reserva_id, data_reserva):
    """Gera uma reserva OTA para uma reserva existente"""
    # 70% das reservas vêm de OTAs, 30% de canais diretos
    if random.random() > 0.7:
        return None  # Reserva direta, sem OTA
    
    ota = random.choice(otas)
    comissao_percent = round(random.uniform(ota['comissao_min'], ota['comissao_max']), 1)
    
    # Gerar ID da OTA (prefixo + número sequencial)
    ota_id_number = 8001 + reserva_id - 1001  # Mantém relação com reserva_id
    reserva_ota_id = f"{ota['prefixo']}{ota_id_number}"
    
    return {
        'reserva_ota_id': reserva_ota_id,
        'reserva_id': reserva_id,
        'canal': ota['nome'],
        'comissao_percent': comissao_percent,
        'data_reserva': data_reserva
    }

def gerar_reservas_otas(total_reservas=200):
    """Gera lista de reservas OTA"""
    reservas_ota = []
    
    # Simular reservas existentes (de 1001 a 1200)
    for reserva_id in range(1001, 1001 + total_reservas):
        # Data de reserva baseada no ID (para variação)
        dias_antes = random.randint(1, 90)
        data_reserva = (datetime.now() - timedelta(days=dias_antes)).strftime('%Y-%m-%d')
        
        # Simular tipo de quarto para ajuste de comissão
        tipo_quarto = random.choice(['Standard', 'Luxo', 'Suíte', 'Suíte Master', 'Suíte Presidencial'])
        
        reserva_ota = gerar_reserva_ota(reserva_id, data_reserva)
        if reserva_ota:
            # Ajustar comissão baseada no tipo de quarto
            ajuste = calcular_comissao_por_tipo_quarto(tipo_quarto)
            reserva_ota['comissao_percent'] = round(reserva_ota['comissao_percent'] + ajuste, 1)
            reservas_ota.append(reserva_ota)
    
    return reservas_ota

# Gerar as reservas OTA
reservas_ota = gerar_reservas_otas(200)

# Criar arquivo CSV
with open(r'hotel_chain\staging\reservas_ota.csv', 'w', newline='', encoding='utf-8') as arquivo:
    campos = [
        'reserva_ota_id', 'reserva_id', 'canal', 
        'comissao_percent', 'data_reserva'
    ]
    
    writer = csv.DictWriter(arquivo, fieldnames=campos)
    writer.writeheader()
    writer.writerows(reservas_ota)

print("Arquivo 'reservas_ota.csv' criado com sucesso!")
print(f"Total de reservas OTA: {len(reservas_ota)}")
print(f"Reservas diretas (sem OTA): {200 - len(reservas_ota)}")

# Estatísticas
print(f"\nEstatísticas das reservas OTA:")

# Distribuição por OTA
otas_count = {}
comissao_total_ota = {}
for reserva in reservas_ota:
    ota = reserva['canal']
    otas_count[ota] = otas_count.get(ota, 0) + 1
    comissao_total_ota[ota] = comissao_total_ota.get(ota, 0) + reserva['comissao_percent']

print(f"\nDistribuição por OTA:")
for ota, count in otas_count.items():
    comissao_media = comissao_total_ota[ota] / count
    porcentagem = (count / len(reservas_ota)) * 100
    print(f"  {ota}: {count} reservas ({porcentagem:.1f}%) - Comissão média: {comissao_media:.1f}%")

# Estatísticas de comissão
comissao_min = min(r['comissao_percent'] for r in reservas_ota)
comissao_max = max(r['comissao_percent'] for r in reservas_ota)
comissao_media = sum(r['comissao_percent'] for r in reservas_ota) / len(reservas_ota)

print(f"\nComissões:")
print(f"  Mínima: {comissao_min}%")
print(f"  Máxima: {comissao_max}%")
print(f"  Média: {comissao_media:.1f}%")

# Top OTAs por volume
otas_ordenadas = sorted(otas_count.items(), key=lambda x: x[1], reverse=True)
print(f"\nTop OTAs por volume de reservas:")
for i, (ota, count) in enumerate(otas_ordenadas[:5], 1):
    print(f"  {i}. {ota}: {count} reservas")

# Mostrar primeiros registros como exemplo
print("\nPrimeiros 10 registros:")
print("reserva_ota_id | reserva_id | canal | comissao_percent | data_reserva")
for i in range(min(10, len(reservas_ota))):
    r = reservas_ota[i]
    print(f"{r['reserva_ota_id']} | {r['reserva_id']} | {r['canal']} | {r['comissao_percent']} | {r['data_reserva']}")

# Exemplos de diferentes OTAs
print("\nExemplos de reservas por OTA:")
otas_exibidas = set()
for reserva in reservas_ota:
    if reserva['canal'] not in otas_exibidas:
        print(f"  {reserva['canal']}: Reserva {reserva['reserva_ota_id']} - Comissão {reserva['comissao_percent']}%")
        otas_exibidas.add(reserva['canal'])
    if len(otas_exibidas) == 3:  # Mostrar apenas 3 exemplos
        break

# Simular cálculo de comissão em valores monetários (exemplo)
if reservas_ota:
    reserva_exemplo = reservas_ota[0]
    print(f"\nExemplo de cálculo de comissão:")
    print(f"Reserva OTA: {reserva_exemplo['reserva_ota_id']}")
    print(f"OTA: {reserva_exemplo['canal']}")
    print(f"Comissão: {reserva_exemplo['comissao_percent']}%")
    print(f"Valor da reserva estimado: R$ 1.500,00")
    comissao_valor = 1500 * (reserva_exemplo['comissao_percent'] / 100)
    print(f"Valor da comissão: R$ {comissao_valor:.2f}")