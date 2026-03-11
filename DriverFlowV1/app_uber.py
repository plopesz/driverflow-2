import streamlit as st
import pandas as pd
import os
from datetime import datetime
import plotly.express as px

# 1. --- SISTEMA DE LOGIN ---
def check_password():
    """Retorna True se o usuário/senha estiverem corretos."""
    def password_entered():
        if st.session_state["username"] in st.secrets["passwords"] and \
           st.session_state["password"] == st.secrets["passwords"][st.session_state["username"]]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Não guarda a senha na memória
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.title("🔐 Bem-vindo ao DriverFlow")
        st.text_input("Usuário", on_change=password_entered, key="username")
        st.text_input("Senha", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        st.title("🔐 Bem-vindo ao DriverFlow")
        st.text_input("Usuário", on_change=password_entered, key="username")
        st.text_input("Senha", type="password", on_change=password_entered, key="password")
        st.error("😕 Usuário ou senha incorretos.")
        return False
    else:
        return True

# ⚠️ PARA TESTE LOCAL: Se você não configurou o "Secrets" ainda, 
# use esta versão simplificada para ver funcionando no seu PC:
if "autenticado" not in st.session_state:
    st.session_state["autenticado"] = False

if not st.session_state["autenticado"]:
    st.title("🚀 DriverFlow Login")
    user = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")
    if st.button("Entrar"):
        # Aqui você pode criar usuários para seus amigos!
        usuarios_permitidos = {"pedro": "hondafit123", "amigo": "ifood2026", "teste": "123"}
        if user in usuarios_permitidos and usuarios_permitidos[user] == senha:
            st.session_state["autenticado"] = True
            st.rerun()
        else:
            st.error("Usuário ou senha inválidos")
    st.stop() 


st.set_page_config(page_title="DriverFlow SaaS", page_icon="📈", layout="wide")


st.title(f"Bem-vindo de volta, {st.session_state['username'].capitalize()}! 👋")

import streamlit as st
import pandas as pd
import os
from datetime import datetime
import plotly.express as px


st.set_page_config(page_title="DriverFlow | Gestão Profissional", page_icon="📈", layout="wide")

# Estilização Personalizada (CSS) para ficar com cara de App moderno
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

# --- BANCO DE DADOS ---
arquivo = 'banco_saas.csv'
if not os.path.exists(arquivo):
    df = pd.DataFrame(columns=['Data', 'Plataforma', 'Bruto', 'Custos', 'Liquido', 'KM'])
    df.to_csv(arquivo, index=False)
df = pd.read_csv(arquivo)

# --- SIDEBAR PROFISSIONAL ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3202/3202926.png", width=80) # Ícone genérico de App
    st.title("DriverFlow")
    st.subheader("Configurações de Perfil")
    nome = st.text_input("Nome do Motorista/Entregador", "Seu Nome")
    meta = st.number_input("Meta de Lucro Mensal (R$)", value=2000.0, step=100.0)
    
    st.markdown("---")
    st.write("🏃 **Ajuste de Custos**")
    veiculo = st.selectbox("Veículo de Trabalho", ["Carro", "Moto", "Bike/Pé"])
    
    if veiculo != "Bike/Pé":
        cons = st.number_input("Consumo Médio (km/l)", value=10.0 if veiculo == "Carro" else 35.0)
        gas = st.number_input("Preço Combustível (R$)", value=5.80)
        manut = st.number_input("Reserva de Manutenção (R$/km)", value=0.15 if veiculo == "Carro" else 0.05)
        custo_km = (gas / cons) + manut
    else:
        custo_km = 0.0

# --- TELA PRINCIPAL ---
st.title(f"Bem-vindo ao DriverFlow, {nome}! 👋")
st.info("Sua ferramenta definitiva para monitorar o lucro real, não apenas o bruto dos apps.")

# Métricas de Performance
lucro_total = df['Liquido'].sum() if not df.empty else 0.0
progresso = min(lucro_total / meta, 1.0)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Lucro Líquido", f"R$ {lucro_total:.2f}")
col2.metric("Faltam p/ Meta", f"R$ {max(meta - lucro_total, 0.0):.2f}")
col3.metric("Total Bruto", f"R$ {df['Bruto'].sum():.2f}")
col4.metric("Aproveitamento", f"{progresso*100:.1f}%")

st.progress(progresso)

st.markdown("---")

# Layout de duas colunas: Lançamento e Gráfico
col_left, col_right = st.columns([1, 1.5])

with col_left:
    st.subheader("➕ Registrar Novo Turno")
    with st.form("registro"):
        plat = st.selectbox("Plataforma", ["Uber", "iFood", "99", "Rappi", "Loggi", "Particular", "Outro"])
        v_bruto = st.number_input("Ganhos Brutos (R$)", min_value=0.0)
        v_km = st.number_input("KM Total Rodado", min_value=0.0)
        v_data = st.date_input("Data", datetime.now())
        
        if st.form_submit_button("Salvar Registro"):
            gastos = v_km * custo_km
            liq = v_bruto - gastos
            
            nova_linha = {
                'Data': v_data.strftime('%d/%m/%Y'),
                'Plataforma': plat,
                'Bruto': round(v_bruto, 2),
                'Custos': round(gastos, 2),
                'Liquido': round(liq, 2),
                'KM': v_km
            }
            df = pd.concat([df, pd.DataFrame([nova_linha])], ignore_index=True)
            df.to_csv(arquivo, index=False)
            st.success("Dados computados com sucesso!")
            st.rerun()

with col_right:
    st.subheader("📊 Análise de Fontes")
    if not df.empty:
        fig = px.bar(df.groupby('Plataforma')['Liquido'].sum().reset_index(), 
                     x='Plataforma', y='Liquido', 
                     color='Plataforma', title="Lucro Líquido por App")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Aguardando os primeiros registros para gerar gráficos.")

# Tabela de Histórico com busca
st.markdown("---")
if not df.empty:
    st.subheader("📅 Histórico de Atividades")
    st.dataframe(df.sort_index(ascending=False), use_container_width=True)
    
    # Opção de baixar os dados (Botão de Exportar)
    csv_data = df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Baixar Relatório (Excel/CSV)", data=csv_data, file_name=f"relatorio_{nome}.csv", mime='text/csv')