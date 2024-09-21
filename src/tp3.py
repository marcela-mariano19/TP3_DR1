import pandas as pd 
import streamlit as st
import matplotlib.pyplot as plt


st.set_page_config(
    page_title="TP3- DR1",
    layout="wide",  
)

def load_data(file):
    df = pd.read_excel(file,header=4, usecols="A:H")
    df.drop(index=0, inplace=True)
    df.drop(index=[13,14,15,16,17,18], inplace=True)
    for column in df.columns[1:]:
        df[column] = [str(i).replace("...", "0") for i in df[column]] #Inserido, porque a converção seguinte estava apresentando erro por causa dos "..."
        df[column] = [float(str(i).replace(" ", "")) for i in df[column]] #Inserido para corrigir as informações que estavam erras no gráfico.

    return df

st.title("Estudo sobre o volume de visitação do Centro Cultural Banco do Brasil - 2015 a 2021")

st.header("- Explicação do Objetivo e Motivação:")
st.write("Escolhi trabalhar com esses dados, porque o Centro Cultural Banco do Brasil é um dos principais centros culturais do país e lá é um dos meus locais preferidos")
#falta explicar o que será implantado

st.header(" Realizar Upload de Arquivo Excel:")
#VALE PARA AS QUESTÕES 2 E 3
st.write("Nota: foi necessário usar arquivo excel, porque o site Data Rio Não gera arquivos em CSV, então a experíência para o cliente leigo seria mais dificil se ele antes tivesse que converter o arquivo baixado")


file = st.file_uploader("Suba seu arquivo Excel (.xls) aqui: ",type=['xls'])
if file is not None:
    bar = st.progress(0)
    text = st.empty()
    df = load_data(file)
    
    with st.spinner("Carregando..."):
        for percent_complete in range(100):
            bar.progress(percent_complete + 1)
            text.text(f"Porcentagem de Carregamento: {percent_complete + 1}%")  # Usado para que o carregamento vá até 100% e não 99%

    st.success("Carregado com Sucesso!")

else:
    df = None

col1, col2,col3 = st.columns(3)

col1.metric("Quantidade de Colunas", value=df.shape[1])
col2.metric("Quantidade de Linhas", value=df.shape[0])
col3.metric("Soma total das visitas", value=df.iloc[:,1:].sum().sum()) #Tive que colocar o segundo sum para somar todos os valores da tabela, pois o primeiro sum só estava somando as colunas.


st.write("Tabela com os dados do arquivo: ")
st.dataframe(df)

st.header("- Filtro de Dados, Seleção e Visualização: ")
#VALE PARA AS QUESTÕES 3, 10 e 11
year = st.radio("Selecione o ano que deseja visualizar a quantidade de visitas agrupadas por mês: ",  df.columns[1:],horizontal = True)
fig, ax = plt.subplots(figsize=(20,7))
plt.bar(df["Mês"], df[year].astype(float))
plt.xticks(rotation=45)
st.pyplot(fig)

month = st.selectbox("Selecione o mês para visualizar a tendência ao longo dos anos: ", df["Mês"].unique())
fig, ax = plt.subplots(figsize=(20,7))
plt.plot(df.columns[1:], df.loc[df["Mês"] == month].values[0][1:].astype(float))
plt.xticks(rotation=45)
st.pyplot(fig)

graph = st.checkbox("Deseja visualizar o gráfico de histograma do ano selecionado?")
if graph:
    fig, ax = plt.subplots(figsize=(20,7))
    plt.hist(df[year], bins=10)
    st.pyplot(fig)






