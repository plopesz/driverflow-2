import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Configuração da Página
st.set_page_config(page_title="DriverFlow", page_icon="🚗")

st.title("🚗 Dashboard")
st.markdown("---")

# --- BANCO DE DADOS (CSV) ---
arquivo = 'dados_uber.csv'
if not os.path.exists(arquivo):
    df = pd.DataFrame(columns=['Data', 'Bruto', 'Gasolina', 'Manutencao', 'Liquido'])
    df.to_csv(arquivo, index=False)

df = pd.read_csv(arquivo)

# --- LÓGICA DE METAS ---
meta_objetivo = 1600.0
total_acumulado = df['Liquido'].sum() if not df.empty else 0.0
progresso = min(total_acumulado / meta_objetivo, 1.0)

# --- INTERFACE: BARRA DE PROGRESSO ---
st.subheader(f"Progresso da Meta: R$ {total_acumulado:.2f} / R$ {meta_objetivo:.2f}")
st.progress(progresso)
st.write(f"🎯 Faltam **R$ {max(meta_objetivo - total_acumulado, 0.0):.2f}** para fechar o mês!")

# --- FORMULÁRIO DE ENTRADA ---
with st.expander("➕ Lançar Novo Turno"):
    with st.form("novo_lancamento"):
        col1, col2 = st.columns(2)
        with col1:
            bruto = st.number_input("Ganho Bruto (App)", min_value=0.0, step=10.0)
            km = st.number_input("KM Total Rodado", min_value=0.0, step=1.0)
        with col2:
            preco_gas = st.number_input("Preço Gasolina", min_value=0.0, value=5.80)
            consumo = st.number_input("Consumo Fit (km/l)", min_value=1.0, value=9.5)
        
        btn_salvar = st.form_submit_button("Salvar Turno")

if btn_salvar:
    custo_gas = (km / consumo) * preco_gas
    manut = km * 0.15 # Reserva de 15 centavos/km
    liquido = bruto - custo_gas - manut
    
    novo_dado = {
        'Data': datetime.now().strftime('%d/%m/%Y'),
        'Bruto': bruto,
        'Gasolina': round(custo_gas, 2),
        'Manutencao': round(manut, 2),
        'Liquido': round(liquido, 2)
    }
    
    df = pd.concat([df, pd.DataFrame([novo_dado])], ignore_index=True)
    df.to_csv(arquivo, index=False)
    st.success("Boa, Pedro! Dados salvos. Atualize a página.")
    st.rerun()

# --- HISTÓRICO ---
if not df.empty:
    st.markdown("---")
    st.subheader("Histórico de Corridas")

    st.dataframe(df.sort_index(ascending=False), use_container_width=True)