import pandas as pd
import streamlit as st
from supabase import create_client

# Configuração da página com o nome oficial do projeto
st.set_page_config(
    page_title='SeuRadar - Leilões Judiciais de Veículos (Art. 895 CPC)',
    page_icon='📡',
    layout='wide',
)

# Estilização CSS do SeuRadar
st.markdown(
    """
    <style>
    .card-veiculo {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }
    .badge-art895 {
        background-color: #0284c7;
        color: white;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 12px;
        font-weight: bold;
    }
    .badge-risco-baixo {
        background-color: #22c55e;
        color: white;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 12px;
        font-weight: bold;
    }
    .badge-risco-alerta {
        background-color: #eab308;
        color: black;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 12px;
        font-weight: bold;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# Conexão com o Banco de Dados (Supabase)
SUPABASE_URL = "SUA_URL_SUPABASE"
SUPABASE_KEY = "SUA_CHAVE_ANON_PUBLIC"


@st.cache_resource
def init_connection():
  return create_client(SUPABASE_URL, SUPABASE_KEY)


# Título e Apresentação do Projeto
st.title('📡 SeuRadar')
st.subheader('Garimpo Inteligente de Veículos Judiciais pelo Art. 895 do CPC')
st.markdown(
    'O **SeuRadar** varre editais de leilões judiciais, identifica veículos com'
    ' direito a **parcelamento (25% de entrada + 30x)**, analisa débitos por IA'
    ' e calcula a margem sobre a FIPE.'
)

# Filtros do SeuRadar na Barra Lateral
st.sidebar.header('🔍 Filtros do SeuRadar')
filtro_uf = st.sidebar.multiselect(
    'Estado (UF):', ['SP', 'RJ', 'MG', 'PR'], default=['SP', 'RJ']
)
filtro_aporte_max = st.sidebar.slider(
    'Aporte Inicial Máximo (R$):', 5000, 50000, 15000, step=1000
)
filtro_margem_min = st.sidebar.slider(
    'Margem Mínima sobre FIPE (%):', 10, 60, 30
)

# Exibição dos Veículos
col_main, col_detail = st.columns([2, 1])

with col_main:
  st.subheader('🚗 Oportunidades Mapeadas pelo SeuRadar')

  # Código que puxa os dados do Supabase ou Mock para exibição
  # (Insira aqui a iteração de cards com os dados do banco)

with col_detail:
  st.subheader('🧮 Simulador Art. 895 - SeuRadar')
  st.info('Calcule seu aporte inicial e parcelas:')

  sim_lance = st.number_input(
      'Lance Pretendido (R$):', value=40000.0, step=1000.0
  )
  sim_fipe = st.number_input(
      'Valor FIPE do Veículo (R$):', value=75000.0, step=1000.0
  )

  sim_ent = sim_lance * 0.25
  sim_com = sim_lance * 0.05
  sim_aporte = sim_ent + sim_com
  sim_parc = (sim_lance * 0.75) / 30
  sim_lucro = sim_fipe - (sim_lance + sim_com)

  st.write('---')
  st.write(f'• **Entrada (25%):** R$ {sim_ent:,.2f}')
  st.write(f'• **Comissão Leiloeiro (5%):** R$ {sim_com:,.2f}')
  st.markdown(f'### **Aporte Inicial Total:**\n# R$ {sim_aporte:,.2f}')
  st.write(f'• **30 Parcelas de:** R$ {sim_parc:,.2f} / mês')
  st.success(f'**Lucro Estimado x FIPE:** R$ {sim_lucro:,.2f}')