import pandas as pd
from core.database import DataManager

class UberEngine:
    def __init__(self, usuario):
        self.db = DataManager()
        self.usuario = usuario
        # Valores padrão (depois podemos puxar do config.csv)
        self.custo_km_manutencao = 0.15
        self.consumo_padrao = 9.5
        self.preco_gas_padrao = 5.80

    def calcular_turno(self, bruto, km, preco_gas=None, consumo=None):
        """Calcula os custos usando valores dinâmicos ou padrões"""
        # Se você digitou um valor, ele usa. Se não, usa o padrão de 5.80
        gas = float(preco_gas) if preco_gas and preco_gas > 0 else self.preco_gas_padrao
        cons = float(consumo) if consumo and consumo > 0 else self.consumo_padrao
        
        custo_combustivel = (km / cons) * gas
        custo_manutencao = km * self.custo_km_manutencao
        liquido = bruto - custo_combustivel - custo_manutencao
        
        return {
            'usuario': self.usuario,
            'bruto': round(bruto, 2),
            'gasolina': round(custo_combustivel, 2),
            'manutencao': round(custo_manutencao, 2),
            'liquido': round(liquido, 2),
            'km': km
        }

    def get_resumo_mensal(self):
        """Busca todos os lançamentos do usuário e soma o lucro"""
        df = pd.read_csv(self.db._get_path('lancamentos'))
        if df.empty:
            return 0.0
        
        # Filtra apenas o usuário logado
        df_user = df[df['usuario'] == self.usuario]
        return df_user['liquido'].sum()