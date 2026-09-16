import pandas as pd
import streamlit as st

# Configuração da página
st.set_page_config(
    page_title='LeilãoJá - Veículos Art. 895 CPC',
    page_icon='🚗',
    layout='wide',
)

# CSS Personalizado para deixar com cara de App Profissional
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
    .metric-box {
        background-color: #f8fafc;
        padding: 12px;
        border-radius: 8px;
        text-align: center;
        border: 1px solid #f1f5f9;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# Mock Data - Simulação dos dados processados pelos Scrapers + IA
veiculos_mock = [
    {
        'id': '101',
        'modelo': 'Honda Civic LXR 2.0 Flex Aut.',
        'ano': '2015/2016',
        'uf': 'SP',
        'cidade': 'Campinas',
        'fipe': 72000.0,
        'avaliacao': 68000.0,
        'lance_minimo': 34000.0,
        'imagem': (
            'https://images.unsplash.com/photo-1590362891991-f776e747a588?w=500&q=80'
        ),
        'risco': 'Baixo (Sem Débitos)',
        'risco_tipo': 'baixo',
        'resumo_edital': (
            'Edital sem débitos anteriores assumidos. IPTU e IPVA sub-rogam no'
            ' preço. Exige caução do próprio veículo.'
        ),
        'leiloeiro': 'Freitas Leiloeiro',
    },
    {
        'id': '102',
        'modelo': 'Toyota Corolla XE-i 2.0 Flex Aut.',
        'ano': '2018/2019',
        'uf': 'RJ',
        'cidade': 'Niterói',
        'fipe': 88000.0,
        'avaliacao': 80000.0,
        'lance_minimo': 40000.0,
        'imagem': (
            'https://images.unsplash.com/photo-1621007947382-bb3c3994e3fb?w=500&q=80'
        ),
        'risco': 'Atenção (IPVA Pendente)',
        'risco_tipo': 'alerta',
        'resumo_edital': (
            'Arrematante assume R$ 2.400 em IPVA e taxa de guincho/pátio de R$'
            ' 650. Aceita parcelamento do Art. 895 CPC.'
        ),
        'leiloeiro': 'Zukerman Leilões',
    },
    {
        'id': '103',
        'modelo': 'Jeep Compass Longitude 2.0 Aut.',
        'ano': '2020/2021',
        'uf': 'SP',
        'cidade': 'São Paulo',
        'fipe': 115000.0,
        'avaliacao': 110000.0,
        'lance_minimo': 55000.0,
        'imagem': (
            'https://images.unsplash.com/photo-1533473359331-0135ef1b58bf?w=500&q=80'
        ),
        'risco': 'Baixo (Sem Débitos)',
        'risco_tipo': 'baixo',
        'resumo_edital': (
            'Lote de recuperação judicial. Livre de ônus. Necessita confecção'
            ' de chave cópia.'
        ),
        'leiloeiro': 'Sodré Santoro',
    },
]

# Título e Barra Lateral
st.title('🏎️ Radar de Oportunidades - Leilão Judicial (Art. 895 CPC)')
st.markdown(
    'Painel inteligente com cálculo automatizado de **Aporte Inicial (25% +'
    ' 5%)** e análise de edital.'
)

# Sidebar - Filtros do Investidor
st.sidebar.header('🔍 Filtros de Busca')
filtro_uf = st.sidebar.multiselect(
    'Estado (UF):', ['SP', 'RJ', 'MG', 'PR'], default=['SP', 'RJ']
)
filtro_aporte_max = st.sidebar.slider(
    'Aporte Inicial Máximo (R$):', 5000, 30000, 15000, step=1000
)
filtro_margem_min = st.sidebar.slider(
    'Margem de Lucro Mínima sobre FIPE (%):', 10, 60, 30
)

# Processamento dos Cards
st.subheader('🚗 Oportunidades Encontradas')

col_main, col_detail = st.columns([2, 1])

with col_main:
  for item in veiculos_mock:
    if item['uf'] not in filtro_uf:
      continue

    # Cálculos Financeiros
    lance = item['lance_minimo']
    comissao = lance * 0.05
    entrada_25 = lance * 0.25
    aporte_inicial = entrada_25 + comissao
    parcela_30x = (lance * 0.75) / 30
    lucro_estimado = item['fipe'] - (lance + comissao)
    margem_porcentagem = (lucro_estimado / item['fipe']) * 100

    if (
        aporte_inicial <= filtro_aporte_max
        and margem_porcentagem >= filtro_margem_min
    ):
      # Card do Veículo
      st.markdown(
          f"""
            <div class="card-veiculo">
                <span class="badge-art895">Art. 895 CPC Habilitado</span>
                <span class="badge-risco-{item['risco_tipo']}">{item['risco']}</span>
                <h3 style="margin-top:10px;">{item['modelo']} ({item['ano']})</h3>
                <p style="color: #64748b; font-size: 14px;">📍 {item['cidade']} - {item['uf']} | ⚖️ {item['leiloeiro']}</p>
            </div>
            """,
          unsafe_allow_html=True,
      )

      c1, c2, c3, c4 = st.columns(4)
      c1.metric('Valor FIPE', f'R$ {item["fipe"]:,.2f}')
      c2.metric('Lance Mínimo', f'R$ {lance:,.2f}')
      c3.metric(
          'Aporte Inicial (25%+5%)',
          f'R$ {aporte_inicial:,.2f}',
          delta=f'Entrada R$ {entrada_25:,.0f}',
      )
      c4.metric(
          'Margem Est. Lucro',
          f'R$ {lucro_estimado:,.2f}',
          delta=f'{margem_porcentagem:.1f}% FIPE',
      )

      with st.expander('📄 Ver Análise de Edital & Simulação de Parcelas'):
        st.write(f'**Resumo do Edital (IA Gemini):** {item["resumo_edital"]}')
        st.write(
            f'**Plano de Parcelamento:** 30x de **R$ {parcela_30x:,.2f}/mês**'
            ' (com garantia do próprio veículo).'
        )
        st.button(f'Abrir Lote no Leiloeiro #{item["id"]}', key=item['id'])

      st.markdown('---')

with col_detail:
  st.subheader('🧮 Simulador Art. 895')
  st.info('Calcule seu lance customizado:')

  sim_lance = st.number_input(
      'Lance Pretendido (R$):', value=40000.0, step=1000.0
  )
  sim_fipe = st.number_input(
      'Valor FIPE de Referência (R$):', value=75000.0, step=1000.0
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
  st.write(f'• **30 Parcelas Mensais de:** R$ {sim_parc:,.2f}')
  st.success(f'**Lucro Bruto Estimado:** R$ {sim_lucro:,.2f}')