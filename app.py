import streamlit as st
import pandas as pd
import plotly.express as px

# Carregando os dados
dados = pd.read_excel('Vendas_Base_de_Dados.xlsx')

# Calcula o faturamento por linha
dados['Faturamento'] = dados['Quantidade'] * dados['Valor Unitário']

# ===== SIDEBAR =====
st.sidebar.title("Filtros")

# Filtro de loja
lojas = sorted(dados['Loja'].unique())
loja_escolhida = st.sidebar.selectbox("Escolha a loja:", ["Todas"] + lojas)

# Filtro de produto (dinâmico com base na loja)
if loja_escolhida == "Todas":
    produtos_disponiveis = sorted(dados['Produto'].unique())
else:
    produtos_disponiveis = sorted(dados[dados['Loja'] == loja_escolhida]['Produto'].unique())

produto_escolhido = st.sidebar.selectbox("Escolha o produto:", ["Todos"] + produtos_disponiveis)

# ===== APLICA OS FILTROS =====
dados_filtrados = dados.copy()

if loja_escolhida != "Todas":
    dados_filtrados = dados_filtrados[dados_filtrados['Loja'] == loja_escolhida]

if produto_escolhido != "Todos":
    dados_filtrados = dados_filtrados[dados_filtrados['Produto'] == produto_escolhido]

# ===== MAIN =====

# Título principal
st.title("Dashboard de Vendas")

# Tabela de vendas filtrada
st.subheader("Tabela de vendas do mês:")
st.dataframe(dados_filtrados)

# Faturamento total filtrado
faturamento_total = dados_filtrados['Faturamento'].sum()
st.subheader("Faturamento Total:")
st.metric(label="", value=f"R$ {faturamento_total:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

# Gráfico de barras com faturamento por loja (usando os dados originais)
faturamento_lojas = (
    dados.groupby('Loja')['Faturamento']
    .sum()
    .reset_index()
    .sort_values(by='Faturamento', ascending=False)
)

fig_bar = px.bar(faturamento_lojas, x='Loja', y='Faturamento', title='Faturamento por Loja')
st.plotly_chart(fig_bar)

# Gráfico de pizza com participação por produto na loja selecionada
if loja_escolhida != "Todas":
    dados_loja = dados[dados['Loja'] == loja_escolhida]
    dados_pizza = (
        dados_loja.groupby('Produto')['Faturamento']
        .sum()
        .reset_index()
    )
    fig_pizza = px.pie(dados_pizza, values='Faturamento', names='Produto', title=f'Participação dos Produtos - Loja {loja_escolhida}')
    st.plotly_chart(fig_pizza)

# Texto-resumo final
produto_txt = f"o produto **{produto_escolhido}**" if produto_escolhido != "Todos" else "**todos os produtos**"

if loja_escolhida != "Todas":
    loja_txt = f"Na loja **{loja_escolhida}**, "
else:
    loja_txt = "Em **todas as lojas**, "

st.markdown("### Resumo")
valor_formatado = f"R$ {faturamento_total:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

st.markdown(f"{loja_txt}o faturamento total considerando {produto_txt} foi de **{valor_formatado}**.")