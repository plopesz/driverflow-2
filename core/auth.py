import streamlit as st
import pandas as pd
from core.database import DataManager
from datetime import datetime

class AuthManager:
    def __init__(self):
        self.db = DataManager()
        self.db.inicializar_tabelas()

    def verificar_login(self, usuario, senha):
        path = self.db._get_path('usuarios')
        df = pd.read_csv(path)
        
        if df.empty:
            return False

        usuario_limpo = str(usuario).strip().lower()
        senha_hash = self.db.hash_password(senha)

        df['usuario'] = df['usuario'].astype(str).str.strip().str.lower()

        user_match = df[(df['usuario'] == usuario_limpo) & (df['senha'] == senha_hash)]
        
        if not user_match.empty:
            st.session_state['autenticado'] = True
            st.session_state['usuario_logado'] = usuario_limpo
            return True
        return False

    def cadastrar_usuario(self, usuario, senha):
        path = self.db._get_path('usuarios')
        df = pd.read_csv(path)
        
        usuario = str(usuario).strip().lower()

        if not df.empty:
            df['usuario'] = df['usuario'].astype(str).str.strip().str.lower()
            if usuario in df['usuario'].values:
                return False, 
            
        novo_user = {
            'usuario': usuario,
            'senha': self.db.hash_password(senha),
            'data_criacao': datetime.now().strftime('%d/%m/%Y %H:%M')
        }
        
        self.db.salvar_registro('usuarios', novo_user)
        return True, 

    def logout(self):
        st.session_state['autenticado'] = False
        st.session_state['usuario_logado'] = None
        st.rerun()
