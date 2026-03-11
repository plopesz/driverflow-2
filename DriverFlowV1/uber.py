import csv
import os
from datetime import datetime

def calcular_uber():
    print("-" * 40)
    print("CONTROLE DE METAS - HONDA FIT 1.6")
    print("-" * 40)

    data_hoje = datetime.now().strftime('%d/%m/%Y')
    km_inicial = float(input("KM Inicial (Painel): "))
    km_final = float(input("KM Final (Painel): "))
    bruto_app = float(input("Ganho Bruto no App (R$): "))
    preco_gas = float(input("Preço do Litro da Gasolina (R$): "))
    
    consumo_medio = 9.5 
    
    distancia = km_final - km_inicial
    gasto_combustivel = (distancia / consumo_medio) * preco_gas
    
    reserva_manutencao = distancia * 0.15
    
    lucro_liquido = bruto_app - gasto_combustivel - reserva_manutencao
    
    print("\n" + "="*40)
    print(f"📊 RESUMO DO TURNO - {data_hoje}")
    print(f"🛣️  Distância Percorrida: {distancia:.1f} km")
    print(f"⛽ Gasto com Gasolina: R$ {gasto_combustivel:.2f}")
    print(f"🔧 Reserva Manutenção: R$ {reserva_manutencao:.2f}")
    print(f"💰 LUCRO REAL NO BOLSO: R$ {lucro_liquido:.2f}")
    print("="*40)

    arquivo = 'D:\Projetos\Resultado.csv'
    colunas = ['Data', 'KMRodado', 'BrutoApp', 'GastoGasolina', 'ReservaManut', 'LucroLiquido']
    
    file_exists = os.path.isfile(arquivo)
    with open(arquivo, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(colunas)
        writer.writerow([data_hoje, distancia, bruto_app, f"{gasto_combustivel:.2f}", f"{reserva_manutencao:.2f}", f"{lucro_liquido:.2f}"])
    
    print(f"\n✅ Dados salvos em '{arquivo}'.")

if __name__ == "__main__":
    try:
        calcular_uber()
    except ValueError:
        print("Erro: Digite apenas números usando ponto (ex: 5.80) em vez de vírgula.")