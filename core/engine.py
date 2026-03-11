import pandas as pd
from core.database import DataManager

class UberEngine:
    def __init__(self, usuario):
        self.db = DataManager()
        self.usuario = usuario
        self.custo_km_manutencao = 0.15
        self.consumo_padrao = 9.5
        self.preco_gas_padrao = 5.80

    def calcular_turno(self, bruto, km, preco_gas=None, consumo=None):
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
        df = pd.read_csv(self.db._get_path('lancamentos'))
        if df.empty:
            return 0.0

        df_user = df[df['usuario'] == self.usuario]
        return df_user['liquido'].sum()
    def get_meta(self):
        path = self.db._get_path('config')
        df = pd.read_csv(path)
        user_meta = df[df['usuario'] == self.usuario]
        if not user_meta.empty:
            return float(user_meta.iloc[0]['meta_mensal'])
        return 1600.0 

    def salvar_meta(self, nova_meta):
        path = self.db._get_path('config')
        df = pd.read_csv(path)
        if self.usuario in df['usuario'].values:
            df.loc[df['usuario'] == self.usuario, 'meta_mensal'] = nova_meta
        else:
            nova_linha = pd.DataFrame([{'usuario': self.usuario, 'meta_mensal': nova_meta}])
            df = pd.concat([df, nova_linha], ignore_index=True)
        df.to_csv(path, index=False)
