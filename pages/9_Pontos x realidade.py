import pandas as pd
import streamlit as st
from connection import next_games
from connection import base
import datetime
import matplotlib.pyplot as plt
import seaborn as sns  
import numpy as np
from time import sleep

st.sidebar.markdown(
    """
    <div style="position: fixed; bottom: 0; width: 100%; text-align: left;">
        Desenvolvido por <a href="https://joaoluizp.github.io/portfolio_jluizp/" target="_blank" style="color: #3399ff; text-decoration: none;">João Luiz Pinheiro</a>
    </div>
    """, 
    unsafe_allow_html=True
)
st.html('style.html')


df = st.session_state["df_fut"]

df 


# Adicionando colunas para pagina Expectativa de pontos x realidade
df['juice'] = ((1/df['Odd_H_FT']) + (1/df['Odd_D_FT']) + (1/df['Odd_A_FT']))-1

## ODD mais correta
df['odd_real_H'] = df['Odd_H_FT']*(1+df['juice'])
df['odd_real_D'] = df['Odd_D_FT']*(1+df['juice'])
df['odd_real_A'] = df['Odd_A_FT']*(1+df['juice'])

## Pontos dos times jogo a jogo
df['ptH'] = df.apply(lambda row: 3 if row['Goals_H_FT'] > row['Goals_A_FT'] else (1 if row['Goals_H_FT'] == row['Goals_A_FT'] else 0), axis=1)
df['ptA'] = df.apply(lambda row: 3 if row['Goals_H_FT'] < row['Goals_A_FT'] else (1 if row['Goals_H_FT'] == row['Goals_A_FT'] else 0), axis=1)

## Expectativa de pontos que o mercado está nos fornecendo através das ODDS
df['xptH'] = ( (1/df['odd_real_H']) * 3 + (1/df['odd_real_D']) )
df['xptA'] = ( (1/df['odd_real_A']) * 3 + (1/df['odd_real_D']) )

## Contagem
df['contagem'] = range(1, len(df) + 1)
df['contH'] = df.groupby('Home').cumcount() + 1
df['contA'] = df.groupby('Away').cumcount() + 1

## Media de periodos especificos
# Ordena o DataFrame
df = df.sort_values(by=['Home', 'Date'])
# Função para calcular a média dos últimos `window` jogos, excluindo o valor atual
def calculate_exclude_current(group, window=6): # Ultimos 6 jogos
    means = []
    for i in range(len(group)):
        # Pega os últimos `window` valores anteriores à linha atual
        previous_values = group.iloc[max(i - window, 0):i]
        # Calcula a média dos valores anteriores
        if len(previous_values) > 0:
            means.append(np.mean(previous_values))
        else:
            means.append(np.nan)
        window += 1
    return pd.Series(means, index=group.index)

# Aplica a função ao DataFrame
df['mptH6p'] = df.groupby('Home')['ptH'].apply(lambda x: calculate_exclude_current(x)).reset_index(level=0, drop=True)
df['mptA6p'] = df.groupby('Away')['ptA'].apply(lambda x: calculate_exclude_current(x)).reset_index(level=0, drop=True)
df['mxptH6p'] = df.groupby('Away')['xptH'].apply(lambda x: calculate_exclude_current(x)).reset_index(level=0, drop=True)
df['mxptA6p'] = df.groupby('Away')['xptA'].apply(lambda x: calculate_exclude_current(x)).reset_index(level=0, drop=True)

## Lucro
df['plH'] = df.apply(lambda row: (row['Odd_H_FT'] - 1) if row['Goals_H_FT'] > row['Goals_A_FT'] else -1, axis=1)
df['plA'] = df.apply(lambda row: (row['Odd_A_FT'] - 1) if row['Goals_H_FT'] < row['Goals_A_FT'] else -1, axis=1)



temporada_selecionada = st.session_state["temporada_selecionada"]
st.sidebar.text(f"Temporada selecionada: {temporada_selecionada}")


# Ligas
league = sorted(df["League"].unique())
leagues = st.selectbox("League", league, index=None, placeholder="Choose League") # Dropdown 
df_filtered = df[df["League"] == leagues]

# Times
time_liga = sorted(df_filtered["Home"].unique())
time_a = st.selectbox("Team", time_liga, index=None, placeholder="Choose Team")

if time_a != None:

    df_time_home = df[df["Home"] == time_a]

    df_time_away = df[df["Away"] == time_a]

else:
    st.toast('Select a team.', icon=":material/report:")
    sleep(5)
    st.toast('Select a team.', icon=":material/report:")