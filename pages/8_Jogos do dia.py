import pandas as pd
import streamlit as st
from connection import next_games
from connection import base
import datetime
import numpy as np


st.set_page_config(layout="wide")
st.sidebar.markdown(
    """
    <div style="position: fixed; bottom: 0; width: 100%; text-align: left;">
        Desenvolvido por <a href="https://joaoluizp.github.io/portfolio_jluizp/" target="_blank" style="color: #3399ff; text-decoration: none;">João Luiz Pinheiro</a>
    </div>
    """, 
    unsafe_allow_html=True
)

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            .css-1rs6os {visibility: hidden;}
            .css-17ziqus {visibility: hidden;}
            """
            
st.markdown(hide_st_style,unsafe_allow_html=True)


### Capturar base geral para calcular os prognosticos
base_geral_atual_temp = base.df
base_geral_atual_temp = pd.DataFrame(base_geral_atual_temp)


def poisson_prob_gols(stats_home, stats_away):
    # Simulação de Poisson para os times
    home_poisson = np.random.poisson(lam=stats_home, size=10000)
    away_poisson = np.random.poisson(lam=stats_away, size=10000)

    # Cálculo das probabilidades para diferentes números de gols (0 a 6)
    home_probs = [np.mean(home_poisson == n) for n in range(7)]
    away_probs = [np.mean(away_poisson == n) for n in range(7)]

    # Transformando em DataFrames
    home_chance_frame = pd.DataFrame(home_probs, columns=['Probs'])
    away_chance_frame = pd.DataFrame(away_probs, columns=['Probs'])

    # Cálculo da matriz cruzada de probabilidades
    df_cross = np.outer(home_chance_frame['Probs'], away_chance_frame['Probs'])
    df_cross = pd.DataFrame(df_cross).round(2)

    # Cálculo das probabilidades e odds para diferentes tipos de aposta
    soma_over_05 = 1 - df_cross.iloc[0, 0]
    odd_over_05 = 1 / soma_over_05
    soma_over_15 = 1 - (df_cross.iloc[0, 0] + df_cross.iloc[0, 1] + df_cross.iloc[1, 0])
    odd_over_15 = 1 / soma_over_15
    soma_over_25 = 1 - (df_cross.iloc[0, 0] + df_cross.iloc[1, 1] + df_cross.iloc[0, 1] + df_cross.iloc[1, 0] +
                        df_cross.iloc[0, 2] + df_cross.iloc[2, 0])
    odd_over_25 = 1 / soma_over_25
    soma_over_35 = 1 - (df_cross.iloc[0, 0] + df_cross.iloc[0, 1] + df_cross.iloc[0, 2] + df_cross.iloc[0, 3] +
                        df_cross.iloc[1, 0] + df_cross.iloc[1, 1] + df_cross.iloc[1, 2] + df_cross.iloc[2, 0] +
                        df_cross.iloc[2, 1] + df_cross.iloc[3, 0])
    odd_over_35 = 1 / soma_over_35

    ambas_marcam = df_cross.iloc[1:, 1:].sum().sum()
    odd_ambas_marcam = 1 / ambas_marcam

    btts_e_over_25 = df_cross.iloc[1:, 2:].sum().sum()
    odd_btts_e_over_25 = 1 / btts_e_over_25

    return round(soma_over_15 * 100, 2), round(soma_over_25 * 100, 2), round(soma_over_35 * 100, 2), round(ambas_marcam * 100, 2), np.round(btts_e_over_25, 1) * 100, True




### Funções ####
def calcular_expectativa_gols_cantos_confronto(row):
    time_casa = row['Home']
    time_fora = row['Away']
    liga = row['League']
    
    # Verificar se a liga existe na base de dados
    if liga not in base_geral_atual_temp['League'].unique():
        return "Liga não encontrada", "Liga não encontrada", "Liga não encontrada", "Liga não encontrada", "Liga não encontrada", "Liga não encontrada", "Liga não encontrada"
    
    # Filtrar os jogos do time da casa
    df_casa = base_geral_atual_temp[base_geral_atual_temp['Home'] == time_casa] # df_filtered2
    df_fora = base_geral_atual_temp[base_geral_atual_temp['Away'] == time_fora] # df_filtered3

    # Verificar se há jogos suficientes para cálculo
    if len(df_casa) == 0 or len(df_fora) == 0:
        return "Falta mais jogos", "Falta mais jogos", "Falta mais jogos", "Falta mais jogos", "Falta mais jogos", "Falta mais jogos", "Falta mais jogos"
    
    # Calcular a média de gols do time da casa (Home) e do time de fora (Away)
    avg_home = ((df_casa['Goals_H_FT'].sum() / len(df_casa)) + (df_fora['Goals_H_FT'].sum() / len(df_fora))) / 2
    avg_away = ((df_fora['Goals_A_FT'].sum() / len(df_fora)) + (df_casa['Goals_A_FT'].sum() / len(df_casa))) / 2

    probabilidades_gols = poisson_prob_gols(stats_home=avg_home, stats_away=avg_away)


    # Calcular a média de cantos
    avg_cantos_home = (((df_casa['Corners_H_FT'].sum()/len(df_casa)) + (df_fora['Corners_H_FT'].sum()/len(df_fora))) / 2) 
    avg_cantos_away = (((df_fora['Corners_A_FT'].sum()/len(df_fora)) + (df_casa['Corners_A_FT'].sum()/len(df_casa))) / 2)
    
    # Calcular a expectativa de gols do confronto
    avg_gols_confronto = round((avg_home + avg_away), 2)
    # Calcula e xpectativa de cantos do confronto
    avg_cantos_confronto = round((avg_cantos_home + avg_cantos_away), 2)
    
    return avg_gols_confronto, avg_cantos_confronto, probabilidades_gols[0], probabilidades_gols[1], probabilidades_gols[2], probabilidades_gols[3], probabilidades_gols[4]


# Obtém a data atual
hoje = datetime.datetime.now().date()
um_dia = datetime.timedelta(days=1)
amanha = hoje + um_dia # Dia seguinte
d_mais_2 = hoje + 2 * um_dia


hoje = hoje.strftime('%d de %B de %Y')
amanha = amanha.strftime('%d de %B de %Y')
d_mais_2 = d_mais_2.strftime('%d de %B de %Y')



data = st.session_state["df_fut"]


### Lendo as bases
columns_to_select = ['League', 'Date', 'Time', 'Rodada', 'Home', 'Away', 'XG_Home_Pre', 'XG_Away_Pre', 'XG_Total_Pre']
df_hoje = next_games.df_hoje
df_hoje = pd.DataFrame(df_hoje[columns_to_select])
df_hoje.rename(columns={
    'XG_Home_Pre': 'XG Home',
    'XG_Away_Pre': 'XG Away',
    'XG_Total_Pre': 'ExG Footystats'}, inplace=True)
df_hoje[['ExG', 'ExC', '1.5+', '2.5+', '3.5+', 'BTTS', 'BTTS & 2.5+']] = df_hoje.apply(calcular_expectativa_gols_cantos_confronto, axis=1, result_type='expand')
df_hoje['Time'] = pd.to_datetime(df_hoje['Time']).dt.strftime('%H:%M')





df_amanha = next_games.df_amanha
df_amanha = pd.DataFrame(df_amanha[columns_to_select])
df_amanha.rename(columns={
    'XG_Home_Pre': 'XG Home',
    'XG_Away_Pre': 'XG Away',
    'XG_Total_Pre': 'ExG Footystats'}, inplace=True)
df_amanha[['ExG', 'ExC', '1.5+', '2.5+', '3.5+', 'BTTS', 'BTTS & 2.5+']] = df_hoje.apply(calcular_expectativa_gols_cantos_confronto, axis=1, result_type='expand')
df_amanha['Time'] = pd.to_datetime(df_amanha['Time']).dt.strftime('%H:%M')



try:
    df_depois_de_amanha = next_games.df_depois_de_amanha
    df_depois_de_amanha = pd.DataFrame(df_depois_de_amanha[columns_to_select])
    df_depois_de_amanha.rename(columns={
        'XG_Home_Pre': 'XG Home',
        'XG_Away_Pre': 'XG Away',
        'XG_Total_Pre': 'ExG Footystats'}, inplace=True)
    df_depois_de_amanha[['ExG', 'ExC', '1.5+', '2.5+', '3.5+', 'BTTS', 'BTTS & 2.5+']] = df_hoje.apply(calcular_expectativa_gols_cantos_confronto, axis=1, result_type='expand')
    df_depois_de_amanha['Time'] = pd.to_datetime(df_depois_de_amanha['Time']).dt.strftime('%H:%M')
except:
    df_depois_de_amanha = None
    pass

temporada_selecionada = st.session_state["temporada_selecionada"]
st.sidebar.text(f"Temporada selecionada: {temporada_selecionada}")


checkbox = st.sidebar.checkbox("Tirar dados Nulos", value=True)

if df_depois_de_amanha is None or not isinstance(df_depois_de_amanha, pd.DataFrame):
    data_desejada = st.sidebar.selectbox(
    'Date:',
    [hoje, amanha],
    index=None
    ) 
else:
    data_desejada = st.sidebar.selectbox(
        'Date:',
        [hoje, amanha, d_mais_2],
        index=None
    )

    

if data_desejada != None:

    with st.expander("OBS", icon="⚠️"):
        st.write('''
            Apenas os jogos do dia cujas ligas estão no nosso banco de dados serão exibidos. Como não temos todas as ligas, alguns jogos podem não aparecer.
        ''')
    st.divider()


    if data_desejada == hoje:
        try:
            df_hoje = df_hoje[df_hoje['ExC'] != 'Liga não encontrada']
        except:
            pass
        league = sorted(df_hoje["League"].unique())
        leagues = st.sidebar.selectbox("League:", league, index=None, placeholder="Choose League") # Dropdown 
        if checkbox:
            df_hoje = df_hoje[df_hoje['ExC'] != 'Falta mais jogos']
        if leagues!= None:
            df_hoje = df_hoje[df_hoje["League"] == leagues]
        else:
            pass
        st.dataframe(df_hoje[['League', 'Time', 'Rodada', 'Home', 'Away', 'ExG Footystats', 'ExG', 'ExC', '1.5+', '2.5+', '3.5+', 'BTTS', 'BTTS & 2.5+']], hide_index=True,
                    column_config={
                        "1.5+": st.column_config.ProgressColumn(
                            "1.5+", format="%d", min_value=0, max_value=100
                        ),
                        "2.5+": st.column_config.ProgressColumn(
                            "2.5+", format="%d", min_value=0, max_value=100
                        ),
                        "3.5+": st.column_config.ProgressColumn(
                            "3.5+", format="%d", min_value=0, max_value=100
                        ),
                        "BTTS": st.column_config.ProgressColumn(
                            "BTTS", format="%d", min_value=0, max_value=100
                        ),
                        "BTTS & 2.5+": st.column_config.ProgressColumn(
                            "BTTS & 2.5+", format="%d", min_value=0, max_value=100
                        ),
                    })
    elif data_desejada == amanha:
        try:
            df_depois_de_amanha = df_depois_de_amanha[df_hoje['ExC'] != 'Liga não encontrada']
        except:
            pass
        league = sorted(df_depois_de_amanha["League"].unique())
        leagues = st.sidebar.selectbox("League:", league, index=None, placeholder="Choose League") # Dropdown 
        if checkbox:
            df_depois_de_amanha = df_depois_de_amanha[df_depois_de_amanha['ExC'] != 'Falta mais jogos']
        if leagues!= None:
            df_depois_de_amanha = df_depois_de_amanha[df_depois_de_amanha["League"] == leagues]
        else:
            pass
        st.dataframe(df_depois_de_amanha[['League', 'Time', 'Rodada', 'Home', 'Away', 'ExG Footystats', 'ExG', 'ExC', '1.5+', '2.5+', '3.5+', 'BTTS', 'BTTS & 2.5+']], hide_index=True,
                    column_config={
                        "1.5+": st.column_config.ProgressColumn(
                            "1.5+", format="%d", min_value=0, max_value=100
                        ),
                        "2.5+": st.column_config.ProgressColumn(
                            "2.5+", format="%d", min_value=0, max_value=100
                        ),
                        "3.5+": st.column_config.ProgressColumn(
                            "3.5+", format="%d", min_value=0, max_value=100
                        ),
                        "BTTS": st.column_config.ProgressColumn(
                            "BTTS", format="%d", min_value=0, max_value=100
                        ),
                        "BTTS & 2.5+": st.column_config.ProgressColumn(
                            "BTTS & 2.5+", format="%d", min_value=0, max_value=100
                        ),
                    })
    else:
        try:
            df_amanha = df_amanha[df_hoje['ExC'] != 'Liga não encontrada']
        except:
            pass
        league = sorted(df_amanha["League"].unique())
        leagues = st.sidebar.selectbox("League:", league, index=None, placeholder="Choose League") # Dropdown 
        if checkbox:
            df_amanha = df_amanha[df_amanha['ExC'] != 'Falta mais jogos']
        if leagues!= None:
            df_amanha = df_amanha[df_amanha["League"] == leagues]
        else:
            pass
        st.dataframe(df_amanha[['League', 'Time', 'Rodada', 'Home', 'Away', 'ExG Footystats', 'ExG', 'ExC', '1.5+', '2.5+', '3.5+', 'BTTS', 'BTTS & 2.5+']], hide_index=True,
                    column_config={
                        "1.5+": st.column_config.ProgressColumn(
                            "1.5+", format="%d", min_value=0, max_value=100
                        ),
                        "2.5+": st.column_config.ProgressColumn(
                            "2.5+", format="%d", min_value=0, max_value=100
                        ),
                        "3.5+": st.column_config.ProgressColumn(
                            "3.5+", format="%d", min_value=0, max_value=100
                        ),
                        "BTTS": st.column_config.ProgressColumn(
                            "BTTS", format="%d", min_value=0, max_value=100
                        ),
                        "BTTS & 2.5+": st.column_config.ProgressColumn(
                            "BTTS & 2.5+", format="%d", min_value=0, max_value=100
                        ),
                    })

