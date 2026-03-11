import streamlit as st
import pandas as pd
from core.auth import AuthManager
from core.engine import UberEngine
from datetime import datetime

# 1. INICIALIZAÇÃO
auth = AuthManager()

st.set_page_config(page_title="DriverFlow", page_icon="🚗", layout="wide")

# Estilo CSS Personalizado
st.markdown("""
    <style>
    .stProgress > div > div > div > div { background-color: #800020; }
    .card-turno {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 12px;
        border-left: 6px solid #800020;
        margin-bottom: 12px;
        box-shadow: 0px 4px 6px rgba(0,0,0,0.05);
        color: #333;
    }
    .metric-label { font-size: 14px; color: #666; font-weight: normal; }
    .metric-value { font-size: 18px; font-weight: bold; color: #800020; }
    </style>
    """, unsafe_allow_html=True)

# 2. CONTROLE DE ACESSO
if 'autenticado' not in st.session_state:
    st.session_state['autenticado'] = False

if not st.session_state['autenticado']:
    # --- TELA DE ACESSO ---
    st.markdown("<h1 style='text-align: center; color: #800020;'>🚗 DriverFlow</h1>", unsafe_allow_html=True)
    tab_login, tab_cadastro = st.tabs(["Entrar", "Criar Conta"])
    
    with tab_login:
        u = st.text_input("Usuário", key="login_user").lower().strip()
        s = st.text_input("Senha", type="password", key="login_pass")
        if st.button("Acessar Sistema", use_container_width=True):
            if auth.verificar_login(u, s):
                st.rerun()
            else:
                st.error("Usuário ou senha inválidos.")

    with tab_cadastro:
        new_u = st.text_input("Novo Usuário", key="reg_user").lower().strip()
        new_s = st.text_input("Nova Senha", type="password", key="reg_pass")
        if st.button("Finalizar Cadastro", use_container_width=True):
            sucesso, msg = auth.cadastrar_usuario(new_u, new_s)
            if sucesso: st.success(msg)
            else: st.error(msg)
else:
    # --- DASHBOARD (ÁREA LOGADA) ---
    user = st.session_state['usuario_logado']
    engine = UberEngine(user)
    
    # Sidebar
    st.sidebar.markdown(f"### Bem-vindo, \n# **{user.capitalize()}**")
    if st.sidebar.button("Sair"):
        auth.logout()

    # Cabeçalho
    st.title("📊 Painel de Controle")
    
    lucro_total = engine.get_resumo_mensal()
    meta = 1600.0
    progresso = min(lucro_total / meta, 1.0)

    # Métricas Principais
    m1, m2, m3 = st.columns(3)
    m1.metric("Lucro Líquido", f"R$ {lucro_total:.2f}")
    m2.metric("Meta Mensal", f"R$ {meta:.2f}")
    m3.metric("Falta para Meta", f"R$ {max(meta - lucro_total, 0.0):.2f}")
    
    st.progress(progresso)
    st.markdown("---")

    # Form de Lançamento Atualizado
    with st.expander("➕ Lançar Novo Turno"):
        with st.form("form_turno", clear_on_submit=True):
            c1, c2 = st.columns(2)
            bruto = c1.number_input("Ganho Bruto (App)", min_value=0.0, step=10.0)
            km = c1.number_input("KM Rodado no Dia", min_value=0.0, step=1.0)
            
            # NOVOS CAMPOS:
            preco_gas_input = c2.number_input("Preço do Litro (R$)", min_value=0.0, value=5.80, step=0.01)
            consumo_input = c2.number_input("Consumo do Carro (km/l)", min_value=1.0, value=9.5, step=0.1)
            
            if st.form_submit_button("Salvar Turno"):
                if bruto > 0 and km > 0:
                    # Passando os valores digitados para a Engine
                    dados_calculados = engine.calcular_turno(
                        bruto, 
                        km, 
                        preco_gas=preco_gas_input, 
                        consumo=consumo_input
                    )
                    dados_calculados['data'] = datetime.now().strftime('%d/%m/%Y')
                    dados_calculados['veiculo'] = "Padrão"
                    
                    engine.db.salvar_registro('lancamentos', dados_calculados)
                    st.success("Turno salvo com sucesso!")
                    st.rerun()

    # Listagem em Cards
    st.subheader("📋 Histórico Recente")
    df_logs = pd.read_csv(engine.db._get_path('lancamentos'))
    
    if not df_logs.empty:
        df_user = df_logs[df_logs['usuario'] == user].sort_index(ascending=False)
        
        if not df_user.empty:
            for idx, row in df_user.iterrows():
                st.markdown(f"""
                <div class="card-turno">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="font-size: 14px; color: #666;">📅 {row['data']}</span>
                        <span style="color: #1e7e34; font-weight: bold; font-size: 20px;">R$ {row['liquido']:.2f}</span>
                    </div>
                    <div style="margin-top: 10px; display: flex; gap: 25px;">
                        <div><span class="metric-label">💰 Bruto:</span><br><span class="metric-value">R$ {row['bruto']:.2f}</span></div>
                        <div><span class="metric-label">⛽ Combustível:</span><br><span class="metric-value">R$ {row['gasolina']:.2f}</span></div>
                        <div><span class="metric-label">🚗 KM:</span><br><span class="metric-value">{row['km']} km</span></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Botão de Excluir
                if st.button(f"🗑️ Excluir", key=f"del_{idx}"):
                    all_data = pd.read_csv(engine.db._get_path('lancamentos'))
                    all_data = all_data.drop(idx)
                    all_data.to_csv(engine.db._get_path('lancamentos'), index=False)
                    st.rerun()
        else:
            st.info("Nenhum lançamento encontrado para seu usuário.")
    else:
        st.info("O banco de dados está vazio. Comece agora!")