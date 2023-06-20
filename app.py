import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
import json
import requests

df = pd.read_csv('data/analyzable_data.csv')
json_url = 'https://raw.githubusercontent.com/fititnt/gis-dataset-brasil/master/uf/geojson/uf.json'
response = requests.get(json_url)
geojson = response.json()

st.sidebar.title('Páginas')
options = st.sidebar.radio('', options=['Início',
          'Consumo Residencial', 'Consumo Industrial',
          'Ideb x Consumo Residencial',
          'Pib x Consumo Residencial',
          'Mapa Consumo Residencial',
          'Mapa Consumo Industrial'])

def home():
    st.title("Análise do Consumo de Energia Elétrica nos Estados do Brasil")
    st.text('Considerando o desenvolvimento tecnológico nos mais variados setores do Brasil, que \n'
            'está associado ao desenvolvimento destes setores no mundo, é perceptível o \n'
            'crescimento da demanda por energia elétrica ao longo dos anos. Aparelhos antes \n'
            'inexistentes, como os smartphones, são ferramentas comuns ao dia a dia de \n'
            'praticamente toda a população. A necessidade constante de conexão com a internet, \n'
            'os computadores e notebooks que são fundamentais ao funcionamento de qualquer \n'
            'empresa ou repartição pública e nas escolas e universidades, os equipamentos \n'
            'elétricos para realização de exames ou aplicação de tratamentos de saúde, as \n'
            'variadas mídias que funcionam como recursos didáticos aos professores. Enfim, todo \n'
            'esse novo universo de ferramentas amplia fortemente a necessidade por energia \n'
            'elétrica. Deste modo, é possível investigar a associação entre o consumo per capita \n'
            'de energia elétrica e o desenvolvimento (populacional, tecnológico, saúde, educação \n'
            'etc.) dos estados do Brasil, buscando entender o impacto da disponibilidade de \n'
            'energia nesses indicadores, bem como nas velocidades de suas mudanças. \n \n'
            'Trabalho realizado para a disciplina de Visuzalição de Dados do DCC (UFMG). \n'
            'Discentes: José Walter de Lima Mota, Augusto César Gontijo de Araújo, Vinícius do \n'
            'Pinho Barbosa e Débora Mello de Almeida.')

def residencial(df):
    fig = px.treemap(df, path=['ano', 'estado'], values='consumo_residencial_per_capita',
          color='ideb', color_continuous_scale='fall', title='Consumo Residencial (Per Capita) e IDEB x Ano')
    fig1 = px.line(df, 
              x='ano', 
              y='consumo_residencial_per_capita', 
              color='estado',              
              title='Consumo Residencial (Per Capita) x Ano',
              labels={'consumo_residencial_per_capita': 'Consumo',
                      'ano': 'Ano'})
    st.plotly_chart(fig)
    st.plotly_chart(fig1)

def industrial(df):
    fig = px.treemap(df, path=['ano', 'estado'], values='consumo_industrial_per_capita',
          color='ideb', color_continuous_scale='oranges', title='Consumo Industrial (Per Capita) e IDEB x Ano')
    fig1 = px.line(df, 
              x='ano', 
              y='consumo_industrial_per_capita', 
              color='estado',              
              title='Consumo Industrial (Per Capita) x Ano',
              labels={'consumo_industrial_per_capita': 'Consumo',
                      'ano': 'Ano'})
    st.plotly_chart(fig)
    st.plotly_chart(fig1)

def ideb(df):
    fig = px.scatter(df, 
              x='consumo_residencial_per_capita', 
              y='ideb', 
              color='regiao',
              animation_frame='ano',
              size="populacao_absoluta",
              hover_name='estado',
              title='Ideb x Consumo Residencial (Per Capita)',
              labels={'consumo_residencial_per_capita': 'Consumo', 'ideb': 'Ideb', 'regiao': 'Região'})
    fig.update_yaxes(range=[2, 7])
    fig.update_xaxes(range=[0.16, 0.96])
    st.plotly_chart(fig)

def pib(df):
    fig = px.scatter(df, 
              x='consumo_residencial_per_capita', 
              y='pib_per_capita', 
              color='regiao',
              animation_frame='ano',
              size="populacao_absoluta",
              hover_name='estado',
              title='Pib (Per Capita) x Consumo Residencial (Per Capita)',
              labels={'consumo_residencial_per_capita': 'Consumo', 'pib_per_capita': 'Pib', 'regiao': 'Região'})
    fig.update_xaxes(range=[0.16, 0.96])
    fig.update_yaxes(range=[2000, 91000])
    st.plotly_chart(fig)

def mapa_residencial(df):
    fig = px.choropleth_mapbox(df, geojson=geojson, 
            color="consumo_residencial_per_capita",
            animation_frame="ano",
            locations="sigla", 
            featureidkey="properties.UF_05",
            center={"lat": -15.30, "lon": -47.92},
            mapbox_style="carto-positron", 
            zoom=2,
            title='Consumo Residencial (Per Capita) x Ano',
            labels={'consumo_residencial_per_capita': 'Consumo', 'ano': 'Ano'})
    st.plotly_chart(fig)

def mapa_industrial(df):
    fig = px.choropleth_mapbox(df, geojson=geojson, 
            color="consumo_industrial_per_capita",
            animation_frame="ano",
            locations="sigla", 
            featureidkey="properties.UF_05",
            center={"lat": -15.30, "lon": -47.92},
            mapbox_style="carto-positron", 
            zoom=2,
            title='Consumo Industrial (Per Capita) x Ano',
            labels={'consumo_industrial_per_capita': 'Consumo', 'ano': 'Ano'})
    st.plotly_chart(fig)
    
if options == "Início":
    home()
elif options == 'Consumo Residencial':
    residencial(df)
elif options == 'Consumo Industrial':
    industrial(df)
elif options == 'Ideb x Consumo Residencial':
    ideb(df)
elif options == 'Pib x Consumo Residencial':
    pib(df)
elif options == 'Mapa Consumo Residencial':
    mapa_residencial(df)
elif options == 'Mapa Consumo Industrial':
    mapa_industrial(df)