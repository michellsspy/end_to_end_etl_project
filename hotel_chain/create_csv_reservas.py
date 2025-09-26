import csv
import random
from datetime import datetime, timedelta
from faker import Faker

# Configurar Faker
fake = Faker('pt_BR')

# Dados base para as reservas
hoteis = [
    {'hotel_id': 1, 'nome': 'Hotel Praia Dourada', 'cidade': 'Rio de Janeiro'},
    {'hotel_id': 2, 'nome': 'Hotel Business Center', 'cidade': 'São Paulo'},
    {'hotel_id': 3, 'nome': 'Mountain Resort', 'cidade': 'Gramado'},
    {'hotel_id': 4, 'nome': 'Beach Paradise', 'cidade': 'Florianópolis'},
    {'hotel_id': 5, 'nome': 'Capital Suites', 'cidade': 'Brasília'}
]

# Quartos por hotel (quarto_id: [hotel_id, tipo, capacidade, diaria_base])
quartos = {
    101: [1, 'Standard', 2, 300.00],
    102: [1, 'Standard', 2, 300.00],
    201: [1, 'Luxo', 2, 500.00],
    202: [1, 'Luxo', 2, 500.00],
    301: [1, 'Suíte', 4, 800.00],
    103: [2, 'Standard', 2, 350.00],
    104: [2, 'Standard', 2, 350.00],
    203: [2, 'Luxo', 2, 600.00],
    303: [2, 'Suíte', 4, 900.00],
    105: [3, 'Standard', 2, 400.00],
    205: [3, 'Luxo', 2, 700.00],
    305: [3, 'Suíte', 4, 1100.00],
    106: [4, 'Standard', 2, 250.00],
    206: [4, 'Luxo', 2, 450.00],
    107: [5, 'Standard', 2, 320.00],
    207: [5, 'Luxo', 2, 550.00]
}

canais_reserva = ['Site', 'Booking', 'Expedia', 'Agência', 'Telefone', 'WhatsApp', 'Presencial']
status_reserva = ['Confirmada', 'Cancelada', 'Pendente', 'Check-in', 'Check-out', 'No Show']
observacoes_comuns = ['-', 'Cliente VIP', 'Aniversariante', 'Honeymoon', 'Cancelamento por covid', 
                     'Reagendamento', 'Pagamento pendente', 'Early check-in solicitado',
                     'Late check-out solicitado', 'Alergia a frutos do mar', 'Cama extra necessária']

def gerar_data_reserva():
    """Gera data de reserva (últimos 30 dias)"""
    dias = random.randint(1, 30)
    return (datetime.now() - timedelta(days=dias)).strftime('%Y-%m-%d')

def gerar_datas_checkin_checkout():
    """Gera datas de check-in (futuro) e check-out"""
    dias_ate_checkin = random.randint(5, 60)  # Check-in entre 5 e 60 dias no futuro
    noites = random.randint(1, 14)  # Estadia de 1 a 14 noites
    
    data_checkin = datetime.now() + timedelta(days=dias_ate_checkin)
    data_checkout = data_checkin + timedelta(days=noites)
    
    return data_checkin.strftime('%Y-%m-%d'), data_checkout.strftime('%Y-%m-%d')

def calcular_valor_total(quarto_id, noites, status):
    """Calcula valor total com possibilidade de desconto"""
    diaria_base = quartos[quarto_id][3]
    valor_base = diaria_base * noites
    
    # Aplicar desconto baseado no canal de reserva e status
    if status == 'Cancelada':
        desconto = valor_base  # Reembolso total para canceladas
    else:
        desconto = random.choice([0, 50, 100, 150, 200])  # Descontos possíveis
    
    valor_total = max(0, valor_base - desconto)
    return valor_total, desconto

def gerar_reservas(total_reservas=200):
    """Gera lista de reservas"""
    reservas = []
    
    for i in range(total_reservas):
        reserva_id = 1000 + i + 1
        hospede_id = random.randint(1, 200)  # Assumindo 200 hóspedes do arquivo anterior
        quarto_id = random.choice(list(quartos.keys()))
        hotel_id = quartos[quarto_id][0]
        
        data_reserva = gerar_data_reserva()
        data_checkin, data_checkout = gerar_datas_checkin_checkout()
        
        # Calcular número de noites
        checkin = datetime.strptime(data_checkin, '%Y-%m-%d')
        checkout = datetime.strptime(data_checkout, '%Y-%m-%d')
        noites = (checkout - checkin).days
        
        canal = random.choice(canais_reserva)
        status = random.choice(status_reserva)
        
        valor_total, desconto = calcular_valor_total(quarto_id, noites, status)
        observacao = random.choice(observacoes_comuns)
        
        reserva = {
            'reserva_id': reserva_id,
            'hóspede_id': hospede_id,
            'quarto_id': quarto_id,
            'hotel_id': hotel_id,
            'data_reserva': data_reserva,
            'data_checkin': data_checkin,
            'data_checkout': data_checkout,
            'canal_reserva': canal,
            'status': status,
            'valor_total': f"{valor_total:.2f}",
            'desconto': f"{desconto:.2f}",
            'observacoes': observacao
        }
        
        reservas.append(reserva)
    
    return reservas

# Gerar as reservas
reservas = gerar_reservas(200)

# Criar arquivo CSV
with open(r'hotel_chain\staging\reservas.csv', 'w', newline='', encoding='utf-8') as arquivo:
    campos = [
        'reserva_id', 'hóspede_id', 'quarto_id', 'hotel_id', 'data_reserva',
        'data_checkin', 'data_checkout', 'canal_reserva', 'status', 'valor_total',
        'desconto', 'observacoes'
    ]
    
    writer = csv.DictWriter(arquivo, fieldnames=campos)
    writer.writeheader()
    writer.writerows(reservas)

print("Arquivo 'reservas.csv' criado com sucesso!")
print(f"Total de reservas: {len(reservas)}")

# Estatísticas
reservas_confirmadas = sum(1 for r in reservas if r['status'] == 'Confirmada')
reservas_canceladas = sum(1 for r in reservas if r['status'] == 'Cancelada')
valor_total_gerado = sum(float(r['valor_total']) for r in reservas)

print(f"\nEstatísticas das reservas:")
print(f"Reservas confirmadas: {reservas_confirmadas}")
print(f"Reservas canceladas: {reservas_canceladas}")
print(f"Valor total gerado: R$ {valor_total_gerado:,.2f}")

# Mostrar primeiros registros como exemplo
print("\nPrimeiros 5 registros:")
print("reserva_id | hóspede_id | quarto_id | hotel_id | data_reserva | data_checkin | data_checkout | canal_reserva | status | valor_total | desconto | observacoes")
for i in range(5):
    r = reservas[i]
    print(f"{r['reserva_id']} | {r['hóspede_id']} | {r['quarto_id']} | {r['hotel_id']} | {r['data_reserva']} | {r['data_checkin']} | {r['data_checkout']} | {r['canal_reserva']} | {r['status']} | {r['valor_total']} | {r['desconto']} | {r['observacoes']}")