import pandas as pd
import numpy as np
import plotly.express as px
import json

df = pd.read_csv('data/processed_data.csv', sep=";")


df['Consumo Residencial'] = df['Consumo Residencial'].str.replace('.', '').astype(float)
df['Consumo Industrial'] = df['Consumo Industrial'].str.replace('.', '').astype(float)

rename = {"Timestamp": "mes_ano",
          "Estado": "estado",
          "Consumo Residencial": "consumo_residencial_absoluto",
          "Consumo Industrial": "consumo_industrial_absoluto",
          "Populacao": "populacao_absoluta",
          "PIB": "pib_absoluto",
          "IDEB": "ideb"}
df = df.rename(columns = rename)

df['ano'] = df['mes_ano'].str[-4:] 

df = df.groupby(['ano', 'estado']).agg({'consumo_residencial_absoluto': 'sum', 
                                                 'consumo_industrial_absoluto': 'sum', 
                                                 'populacao_absoluta': 'mean',
                                                 'pib_absoluto': 'mean',
                                                 'ideb': 'mean'}
                                          ).reset_index()

df = df.sort_values(['estado', 'ano']).reset_index(drop=True)

df['consumo_residencial_per_capita'] = df['consumo_residencial_absoluto'] / df['populacao_absoluta']
df['consumo_industrial_per_capita'] = df['consumo_industrial_absoluto'] / df['populacao_absoluta']
df['pib_per_capita'] = df['pib_absoluto'] / df['populacao_absoluta']

df['populacao_absoluta_yoy'] = df.groupby('estado')['populacao_absoluta'].pct_change() * 100
df['consumo_residencial_absoluto_yoy'] = df.groupby('estado')['consumo_residencial_absoluto'].pct_change() * 100
df['consumo_industrial_absoluto_yoy'] = df.groupby('estado')['consumo_industrial_absoluto'].pct_change() * 100

df['populacao_absoluta_yoy_acumulado'] = df.groupby('estado', group_keys=False)['populacao_absoluta'].apply(lambda x: round(x / x.iloc[0] - 1,3))
df['populacao_absoluta_yoy_acumulado'] *= 100

df['consumo_residencial_absoluto_yoy_acumulado'] = df.groupby('estado', group_keys=False)['consumo_residencial_absoluto'].apply(lambda x: round(x / x.iloc[0] - 1,3))
df['consumo_residencial_absoluto_yoy_acumulado'] *= 100

capitais = {
            'Acre': {'capital': 'Rio Branco', 'lat': -9.975377, 'long': -67.824897, 'regiao': 'Norte', 'sigla': 'AC'},
            'Alagoas': {'capital': 'Maceió', 'lat': -9.665227, 'long': -35.735008, 'regiao': 'Nordeste', 'sigla': 'AL'},
            'Amapá': {'capital': 'Macapá', 'lat': 0.035571, 'long': -51.060405, 'regiao': 'Norte', 'sigla': 'AP'},
            'Amazonas': {'capital': 'Manaus', 'lat': -3.119028, 'long': -60.021731, 'regiao': 'Norte', 'sigla': 'AM'},
            'Bahia': {'capital': 'Salvador', 'lat': -12.971598, 'long': -38.501548, 'regiao': 'Nordeste', 'sigla': 'BA'},
            'Ceará': {'capital': 'Fortaleza', 'lat': -3.71839, 'long': -38.543398, 'regiao': 'Nordeste', 'sigla': 'CE'},
            'Distrito Federal': {'capital': 'Brasília', 'lat': -15.794229, 'long': -47.882166, 'regiao': 'Centro-Oeste', 'sigla': 'DF'},
            'Espírito Santo': {'capital': 'Vitória', 'lat': -20.319639, 'long': -40.337316, 'regiao': 'Sudeste', 'sigla': 'ES'},
            'Goiás': {'capital': 'Goiânia', 'lat': -16.686898, 'long': -49.264794, 'regiao': 'Centro-Oeste', 'sigla': 'GO'},
            'Maranhão': {'capital': 'São Luís', 'lat': -2.53874, 'long': -44.282097, 'regiao': 'Nordeste', 'sigla': 'MA'},
            'Mato Grosso': {'capital': 'Cuiabá', 'lat': -15.601411, 'long': -56.097892, 'regiao': 'Centro-Oeste', 'sigla': 'MT'},
            'Mato Grosso do Sul': {'capital': 'Campo Grande', 'lat': -20.469522, 'long': -54.620827, 'regiao': 'Centro-Oeste', 'sigla': 'MS'},
            'Minas Gerais': {'capital': 'Belo Horizonte', 'lat': -19.916681, 'long': -43.934493, 'regiao': 'Sudeste', 'sigla': 'MG'},
            'Pará': {'capital': 'Belém', 'lat': -1.455754, 'long': -48.490179, 'regiao': 'Norte', 'sigla': 'PA'},
            'Paraíba': {'capital': 'João Pessoa', 'lat': -7.119495, 'long': -34.845011, 'regiao': 'Nordeste', 'sigla': 'PB'},
            'Paraná': {'capital': 'Curitiba', 'lat': -25.429596, 'long': -49.271272, 'regiao': 'Sul', 'sigla': 'PR'},
            'Pernambuco': {'capital': 'Recife', 'lat': -8.057838, 'long': -34.882896, 'regiao': 'Nordeste', 'sigla': 'PE'},
            'Piauí': {'capital': 'Teresina', 'lat': -5.08921, 'long': -42.801301, 'regiao': 'Nordeste', 'sigla': 'PI'},
            'Rio de Janeiro': {'capital': 'Rio de Janeiro', 'lat': -22.906847, 'long': -43.172896, 'regiao': 'Sudeste', 'sigla': 'RJ'},
            'Rio Grande do Norte': {'capital': 'Natal', 'lat': -5.779256, 'long': -35.200916, 'regiao': 'Nordeste', 'sigla': 'RN'},
            'Rio Grande do Sul': {'capital': 'Porto Alegre', 'lat': -30.031831, 'long': -51.206749, 'regiao': 'Sul', 'sigla': 'RS'},
            'Rondônia': {'capital': 'Porto Velho', 'lat': -8.76194, 'long': -63.903538, 'regiao': 'Norte', 'sigla': 'RO'},
            'Roraima': {'capital': 'Boa Vista', 'lat': 2.82351, 'long': -60.675833, 'regiao': 'Norte', 'sigla': 'RR'},
            'Santa Catarina': {'capital': 'Florianópolis', 'lat': -27.594987, 'long': -48.54821, 'regiao': 'Sul', 'sigla': 'SC'},
            'São Paulo': {'capital': 'São Paulo', 'lat': -23.55052, 'long': -46.633308, 'regiao': 'Sudeste', 'sigla': 'SP'},
            'Sergipe': {'capital': 'Aracaju', 'lat': -10.909294, 'long': -37.074763, 'regiao': 'Nordeste', 'sigla': 'SE'},
            'Tocantins': {'capital': 'Palmas', 'lat': -10.249091, 'long': -48.324293, 'regiao': 'Norte', 'sigla': 'TO'}
}

# Adicionando as colunas de latitude e longitude ao dataframe
df['lat'] = df['estado'].map(lambda estado: capitais[estado]['lat'])
df['long'] = df['estado'].map(lambda estado: capitais[estado]['long'])
df['regiao'] = df['estado'].map(lambda estado: capitais[estado]['regiao'])
df['sigla'] = df['estado'].map(lambda estado: capitais[estado]['sigla'])


df.to_csv('data/analyzable_data.csv', index=False)