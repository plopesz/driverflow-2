import pandas as pd
import os
import hashlib
from datetime import datetime

class DataManager:
    def __init__(self, folder='data'):
        self.folder = folder
        if not os.path.exists(self.folder):
            os.makedirs(self.folder)
            
        self.schemas = {
            'usuarios': ['usuario', 'senha', 'data_criacao'],
            'lancamentos': ['usuario', 'data', 'bruto', 'gasolina', 'manutencao', 'liquido', 'km', 'veiculo'],
            'config': ['usuario', 'meta_mensal', 'consumo_medio', 'preco_gas_padrao']
        }

    def _get_path(self, table):
        return os.path.join(self.folder, f"{table}.csv")

    def inicializar_tabelas(self):

        for table, columns in self.schemas.items():
            path = self._get_path(table)
            if not os.path.exists(path):
                pd.DataFrame(columns=columns).to_csv(path, index=False)

    def salvar_registro(self, table, novo_dado_dict):

        path = self._get_path(table)
        df = pd.read_csv(path)
        
        novo_df = pd.DataFrame([novo_dado_dict])
        df = pd.concat([df, novo_df], ignore_index=True)

        df.to_csv(path + ".tmp", index=False) 
        os.replace(path + ".tmp", path) 
        return True

    def hash_password(self, password):
        return hashlib.sha256(str.encode(password)).hexdigest()
