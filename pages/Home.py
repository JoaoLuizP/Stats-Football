import pandas as pd
import psycopg2
from sqlalchemy import create_engine
from datetime import datetime
from openpyxl import load_workbook
from openpyxl.styles.fills import PatternFill
from openpyxl.styles import Font
import time
import math
from numpy import random
import numpy as np
import streamlit as st
import datetime






local_online = psycopg2.connect(
    user="postgres",
    password="Santos010802.2311",
    host="woefully-hot-vulture.data-1.use1.tembo.io",
    port="5432",
    database="postgres")
engine_online = create_engine('postgresql://postgres:Santos010802.2311@woefully-hot-vulture.data-1.use1.tembo.io:5432')




st.set_page_config(layout="wide", initial_sidebar_state="expanded") # Setar a pagina



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



def poisson_prob_gols(stats_home, stats_away):
    home_poisson = random.poisson(lam=stats_home, size=10000)
    away_poisson = random.poisson(lam=stats_away, size=10000)

    def home_team_goal_prob(n):
        goals = 0
        for i in range(0, 10000):
            if home_poisson[i] == n:
                goals = goals + 1
                prob = goals / 10000
        return prob, goals

    def away_team_goal_prob(n):
        goals = 0
        for i in range(0, 10000):
            if away_poisson[i] == n:
                goals = goals + 1
                prob = goals / 10000
        return prob, goals
    

    ### Expectativa de gols e a probabilidade - Mandante
    home_0, g = home_team_goal_prob(0)
    home_1, g = home_team_goal_prob(1)
    home_2, g = home_team_goal_prob(2)
    home_3, g = home_team_goal_prob(3)
    home_4, g = home_team_goal_prob(4)
    home_5, g = home_team_goal_prob(5)
    home_6, g = home_team_goal_prob(6)

    ### Expectativa de gols e a probabilidade - Visitante
    try:
        away_0, g = away_team_goal_prob(0)
        away_1, g = away_team_goal_prob(1)
        away_2, g = away_team_goal_prob(2)
        away_3, g = away_team_goal_prob(3)
        away_4, g = away_team_goal_prob(4)
        away_5, g = away_team_goal_prob(5)
        away_6, g = away_team_goal_prob(6)
        status = True
    except Exception as e:
        st.error(f'This is an error. Try again select Team Away', icon="🚨")
        status = False

    if status:
        ### Transformando em um dataframe
        home_chance = [home_0, home_1, home_2, home_3, home_4, home_5, home_6]
        home_chance_frame = pd.DataFrame(home_chance, columns=['Probs'])
        home_chance_frame = home_chance_frame  # Probabilidades de gol do mandante
        away_chance = [away_0, away_1, away_2, away_3, away_4, away_5, away_6]
        away_chance_frame = pd.DataFrame(away_chance, columns=['Probs'])
        away_chance_frame = away_chance_frame  # Probabilidades de gol do visitante

        ### Juntar as probabilidades em um unico dataframe
        df_cross = home_chance_frame.dot(away_chance_frame.T)
        df_cross = df_cross.round(2)

        ### Somar as linhas e colunas para tirar a prob e odd de Over gols -> [linha(qtd_gols), coluna(qtd_gols)]
        # Eu faço: 1 — a porcentagem de dar under 0,5 na partida
        # Over 0.5 gols
        soma_over_05 = 1 - df_cross.iloc[0, 0]
        odd_over_05 = 1 / soma_over_05
        # Over 1.5 gols
        soma_over_15 = 1 - (df_cross.iloc[0, 0] + df_cross.iloc[0, 1] + df_cross.iloc[1, 0])
        odd_over_15 = 1 / soma_over_15
        # Over 2.5 gols
        soma_over_25 = 1 - (df_cross.iloc[0, 0] + df_cross.iloc[1, 1] + df_cross.iloc[0, 1] + df_cross.iloc[1, 0] +
                            df_cross.iloc[0, 2] + df_cross.iloc[2, 0])
        odd_over_25 = 1 / soma_over_25
        # Over 3.5 gols
        soma_over_35 = 1 - (df_cross.iloc[0, 0] + df_cross.iloc[0, 1] + df_cross.iloc[0, 2] + df_cross.iloc[0, 3] +
                            df_cross.iloc[1, 0] + df_cross.iloc[1, 1] + df_cross.iloc[1, 2] + df_cross.iloc[2, 0] +
                            df_cross.iloc[2, 1] + df_cross.iloc[3, 0])
        odd_over_35 = 1 / soma_over_35

        # Ambas marcam:
        ambas_marcam = (
                df_cross.iloc[1, 1] + df_cross.iloc[1, 2] + df_cross.iloc[1, 3] + df_cross.iloc[1, 4] + df_cross.iloc[
                    1, 5]
                + df_cross.iloc[1, 6] +
                df_cross.iloc[2, 1] + df_cross.iloc[2, 2] + df_cross.iloc[2, 3] + df_cross.iloc[2, 4] + df_cross.iloc[
                    2, 5]
                + df_cross.iloc[2, 6] +
                df_cross.iloc[3, 1] + df_cross.iloc[3, 2] + df_cross.iloc[3, 3] + df_cross.iloc[3, 4] + df_cross.iloc[
                    3, 5]
                + df_cross.iloc[3, 6] +
                df_cross.iloc[4, 1] + df_cross.iloc[4, 2] + df_cross.iloc[4, 3] + df_cross.iloc[4, 4] + df_cross.iloc[
                    4, 5]
                + df_cross.iloc[4, 6] +
                df_cross.iloc[5, 1] + df_cross.iloc[5, 2] + df_cross.iloc[5, 3] + df_cross.iloc[5, 4] + df_cross.iloc[
                    5, 5]
                + df_cross.iloc[5, 6] +
                df_cross.iloc[6, 1] + df_cross.iloc[6, 2] + df_cross.iloc[6, 3] + df_cross.iloc[6, 4] + df_cross.iloc[
                    6, 5]
                + df_cross.iloc[6, 6])
        odd_ambas_marcam = 1 / ambas_marcam

        # Ambas marcam & Over 2,5 gols
        btts_e_over_25 = (
                df_cross.iloc[1, 2] + df_cross.iloc[1, 3] + df_cross.iloc[1, 4] + df_cross.iloc[1, 5] +
                df_cross.iloc[1, 6] + df_cross.iloc[2, 1] + df_cross.iloc[2, 2] + df_cross.iloc[2, 3] +
                df_cross.iloc[2, 4] + df_cross.iloc[2, 5] + df_cross.iloc[2, 6] + df_cross.iloc[3, 1] +
                df_cross.iloc[3, 2] + df_cross.iloc[3, 3] + df_cross.iloc[3, 4] + df_cross.iloc[3, 5] +
                df_cross.iloc[3, 6] + df_cross.iloc[4, 1] + df_cross.iloc[4, 2] + df_cross.iloc[4, 3] +
                df_cross.iloc[4, 4] + df_cross.iloc[4, 5] + df_cross.iloc[4, 6] + df_cross.iloc[5, 1] +
                df_cross.iloc[5, 2] + df_cross.iloc[5, 3] + df_cross.iloc[5, 4] + df_cross.iloc[5, 5] +
                df_cross.iloc[5, 6] + df_cross.iloc[6, 1] + df_cross.iloc[6, 2] + df_cross.iloc[6, 3] +
                df_cross.iloc[6, 4] + df_cross.iloc[6, 5] + df_cross.iloc[6, 6])

        odd_btts_e_over_25 = 1 / btts_e_over_25

        return round(soma_over_15 * 100, 2), round(soma_over_25 * 100, 2), round(soma_over_35 * 100, 2), round(ambas_marcam * 100, 2), np.round(btts_e_over_25, 1) * 100, status

    else:
        return status




@st.cache_data
def load_base_geral():
    teste = pd.read_sql_table("base_geral", con=engine_online, schema="tembo")
    base_history_confrontos = pd.DataFrame(teste)
    return base_history_confrontos

@st.cache_data
def load_data(temp):

    if temp == '2023-2024':
        temp_1 = 20232024
        temp_1_0 = 2023
    elif temp == '2024-2025':
        temp_1 = 20242025
        temp_1_0 = 2024
    else:
        pass

    ### BASE DE DADOS
    # Alemanha
    BUNDES_1 = pd.read_excel(
        f"https://github.com/futpythontrader/YouTube/raw/main/Bases_de_Dados/FootyStats/Bases_de_Dados_(2022-2024)/Germany%20Bundesliga_{temp_1}.xlsx"
    )
    BUNDES_2 = pd.read_excel(
        f"https://github.com/futpythontrader/YouTube/raw/main/Bases_de_Dados/FootyStats/Bases_de_Dados_(2022-2024)/Germany%202.%20Bundesliga_{temp_1}.xlsx"
    )
    BUNDES01 = [BUNDES_1, BUNDES_2]
    BUNDES = pd.concat(BUNDES01)
    # Austria
    AUT = pd.read_excel(
        f"https://github.com/futpythontrader/YouTube/raw/main/Bases_de_Dados/FootyStats/Bases_de_Dados_(2022-2024)/Austria%20Bundesliga_{temp_1}.xlsx")
    # Argentina
    ARG = pd.read_excel(
        f"https://github.com/futpythontrader/YouTube/raw/main/Bases_de_Dados/FootyStats/Bases_de_Dados_(2022-2024)/Argentina%20Primera%20Divisi%C3%B3n_{temp_1_0}.xlsx")
    # Brasil
    BR1_01 = pd.read_excel(
        f"https://github.com/futpythontrader/YouTube/raw/main/Bases_de_Dados/FootyStats/Bases_de_Dados_(2022-2024)/Brazil%20Serie%20A_{temp_1_0}.xlsx")
    BR1_02 = pd.read_excel(
        f"https://github.com/futpythontrader/YouTube/raw/main/Bases_de_Dados/FootyStats/Bases_de_Dados_(2022-2024)/Brazil%20Serie%20B_{temp_1_0}.xlsx")
    BR1 = [BR1_01, BR1_02]
    BR = pd.concat(BR1)
    # Belgica
    BEL = pd.read_excel(
        f"https://github.com/futpythontrader/YouTube/raw/main/Bases_de_Dados/FootyStats/Bases_de_Dados_(2022-2024)/Belgium%20Pro%20League_{temp_1}.xlsx")
    # Croacia
    CRO = pd.read_excel(
        f"https://github.com/futpythontrader/YouTube/raw/main/Bases_de_Dados/FootyStats/Bases_de_Dados_(2022-2024)/Croatia%20Prva%20HNL_{temp_1}.xlsx"
    )
    # Chile
    CHI_01 = pd.read_excel(
        f"https://github.com/futpythontrader/YouTube/raw/main/Bases_de_Dados/FootyStats/Bases_de_Dados_(2022-2024)/Chile%20Primera%20Divisi%C3%B3n_{temp_1_0}.xlsx")
    CHILE = [CHI_01]
    CHI = pd.concat(CHILE)
    # China
    CHINA = pd.read_excel(
        f"https://github.com/futpythontrader/YouTube/raw/main/Bases_de_Dados/FootyStats/Bases_de_Dados_(2022-2024)/China%20Chinese%20Super%20League_{temp_1_0}.xlsx")
    # Dinamarca
    DIN = pd.read_excel(
        f"https://github.com/futpythontrader/YouTube/raw/main/Bases_de_Dados/FootyStats/Bases_de_Dados_(2022-2024)/Denmark%20Superliga_{temp_1}.xlsx"
    )
    # França
    FRA_01 = pd.read_excel(
        f"https://github.com/futpythontrader/YouTube/raw/main/Bases_de_Dados/FootyStats/Bases_de_Dados_(2022-2024)/France%20Ligue%201_{temp_1}.xlsx"
    )
    FRA_O2 = pd.read_excel(
        f"https://github.com/futpythontrader/YouTube/raw/main/Bases_de_Dados/FootyStats/Bases_de_Dados_(2022-2024)/France%20Ligue%202_{temp_1}.xlsx"
    )
    FRA01 = [FRA_01, FRA_O2]
    FRA = pd.concat(FRA01)
    # Finlandia
    FIN = pd.read_excel(
        f"https://github.com/futpythontrader/YouTube/raw/main/Bases_de_Dados/FootyStats/Bases_de_Dados_(2022-2024)/Finland%20Veikkausliiga_{temp_1_0}.xlsx"
    )
    # Holanda
    HOL_01 = pd.read_excel(
        f"https://github.com/futpythontrader/YouTube/raw/main/Bases_de_Dados/FootyStats/Bases_de_Dados_(2022-2024)/Netherlands%20Eredivisie_{temp_1}.xlsx"
    )
    HOL_02 = pd.read_excel(
        f"https://github.com/futpythontrader/YouTube/raw/main/Bases_de_Dados/FootyStats/Bases_de_Dados_(2022-2024)/Netherlands%20Eerste%20Divisie_{temp_1}.xlsx"
    )
    HOL01 = [HOL_01, HOL_02]
    HOL = pd.concat(HOL01)
    # Estonia
    EST = pd.read_excel(
        f"https://github.com/futpythontrader/YouTube/raw/main/Bases_de_Dados/FootyStats/Bases_de_Dados_(2022-2024)/Estonia%20Meistriliiga_{temp_1_0}.xlsx"
    )
    # Inglaterra
    ING_PL = pd.read_excel(
        f"https://github.com/futpythontrader/YouTube/raw/main/Bases_de_Dados/FootyStats/Bases_de_Dados_(2022-2024)/England%20Premier%20League_{temp_1}.xlsx"
    )
    ING_2 = pd.read_excel(
        f"https://github.com/futpythontrader/YouTube/raw/main/Bases_de_Dados/FootyStats/Bases_de_Dados_(2022-2024)/England%20Championship_{temp_1}.xlsx"
    )
    ING_3 = pd.read_excel(
        f"https://github.com/futpythontrader/YouTube/raw/main/Bases_de_Dados/FootyStats/Bases_de_Dados_(2022-2024)/England%20EFL%20League%20One_{temp_1}.xlsx"
    )
    ING1 = [ING_PL, ING_2, ING_3]
    ING = pd.concat(ING1)
    # Italia
    ITA_01 = pd.read_excel(
        f"https://github.com/futpythontrader/YouTube/raw/main/Bases_de_Dados/FootyStats/Bases_de_Dados_(2022-2024)/Italy%20Serie%20A_{temp_1}.xlsx"
    )
    ITA_02 = pd.read_excel(
        f"https://github.com/futpythontrader/YouTube/raw/main/Bases_de_Dados/FootyStats/Bases_de_Dados_(2022-2024)/Italy%20Serie%20B_{temp_1}.xlsx"
    )
    ITA01 = [ITA_01, ITA_02]
    ITA = pd.concat(ITA01)
    # Japao
    JAP_01 = pd.read_excel(
        f"https://github.com/futpythontrader/YouTube/raw/main/Bases_de_Dados/FootyStats/Bases_de_Dados_(2022-2024)/Japan%20J1%20League_{temp_1_0}.xlsx")
    JAP_02 = pd.read_excel(
        f"https://github.com/futpythontrader/YouTube/raw/main/Bases_de_Dados/FootyStats/Bases_de_Dados_(2022-2024)/Japan%20J2%20League_{temp_1_0}.xlsx")
    JAP1 = [JAP_01, JAP_02]
    JAP = pd.concat(JAP1)
    # Noruega
    NOR = pd.read_excel(
        f"https://github.com/futpythontrader/YouTube/raw/main/Bases_de_Dados/FootyStats/Bases_de_Dados_(2022-2024)/Norway%20Eliteserien_{temp_1_0}.xlsx")
    # Paraguai
    PAR = pd.read_excel(
        f"https://github.com/futpythontrader/YouTube/raw/main/Bases_de_Dados/FootyStats/Bases_de_Dados_(2022-2024)/Paraguay%20Division%20Profesional_{temp_1_0}.xlsx")
    # Portugal
    PORT_O1 = pd.read_excel(
        f"https://github.com/futpythontrader/YouTube/raw/main/Bases_de_Dados/FootyStats/Bases_de_Dados_(2022-2024)/Portugal%20Liga%20NOS_{temp_1}.xlsx")
    PORT_O2 = pd.read_excel(
        f"https://github.com/futpythontrader/YouTube/raw/main/Bases_de_Dados/FootyStats/Bases_de_Dados_(2022-2024)/Portugal%20LigaPro_{temp_1}.xlsx")
    PORT01 = [PORT_O1, PORT_O2]
    PORT = pd.concat(PORT01)
    # Romenia
    ROM = pd.read_excel(f"https://github.com/futpythontrader/YouTube/raw/main/Bases_de_Dados/FootyStats/Bases_de_Dados_(2022-2024)/Romania%20Liga%20I_{temp_1}.xlsx")
    # Scotland
    SCOT = pd.read_excel(f"https://github.com/futpythontrader/YouTube/raw/main/Bases_de_Dados/FootyStats/Bases_de_Dados_(2022-2024)/Scotland%20Premiership_{temp_1}.xlsx")
    # Spain
    SPAIN_01 = pd.read_excel(
        f"https://github.com/futpythontrader/YouTube/raw/main/Bases_de_Dados/FootyStats/Bases_de_Dados_(2022-2024)/Spain%20La%20Liga_{temp_1}.xlsx")
    SPAIN_02 = pd.read_excel(
        f"https://github.com/futpythontrader/YouTube/raw/main/Bases_de_Dados/FootyStats/Bases_de_Dados_(2022-2024)/Spain%20Segunda%20Divisi%C3%B3n_{temp_1}.xlsx")
    SPAIN01 = [SPAIN_01, SPAIN_02]
    SPAIN = pd.concat(SPAIN01)
    # Coreia do Sul
    COR = pd.read_excel(
        f"https://github.com/futpythontrader/YouTube/raw/main/Bases_de_Dados/FootyStats/Bases_de_Dados_(2022-2024)/South%20Korea%20K%20League%201_{temp_1_0}.xlsx")
    # Suiça
    SUI_O1 = pd.read_excel(
        f"https://github.com/futpythontrader/YouTube/raw/main/Bases_de_Dados/FootyStats/Bases_de_Dados_(2022-2024)/Switzerland%20Super%20League_{temp_1}.xlsx")
    SUI_02 = pd.read_excel(
        f"https://github.com/futpythontrader/YouTube/raw/main/Bases_de_Dados/FootyStats/Bases_de_Dados_(2022-2024)/Switzerland%20Challenge%20League_{temp_1}.xlsx")
    SUIO1 = [SUI_O1, SUI_02]
    SUI = pd.concat(SUIO1)
    # Suécia
    SWE_01 = pd.read_excel(
        f"https://github.com/futpythontrader/YouTube/raw/main/Bases_de_Dados/FootyStats/Bases_de_Dados_(2022-2024)/Sweden%20Allsvenskan_{temp_1_0}.xlsx")
    SWE_02 = pd.read_excel(
        f"https://github.com/futpythontrader/YouTube/raw/main/Bases_de_Dados/FootyStats/Bases_de_Dados_(2022-2024)/Sweden%20Superettan_{temp_1_0}.xlsx")
    SWE_BOTHS = [SWE_01, SWE_02]
    SWE = pd.concat(SWE_BOTHS)
    # EUA
    MLS = pd.read_excel(
        f"https://github.com/futpythontrader/YouTube/raw/main/Bases_de_Dados/FootyStats/Bases_de_Dados_(2022-2024)/USA%20MLS_{temp_1_0}.xlsx")
    EUA1 = [MLS]
    EUA = pd.concat(EUA1)
    # Uruguai
    URU = pd.read_excel(
        f"https://github.com/futpythontrader/YouTube/raw/main/Bases_de_Dados/FootyStats/Bases_de_Dados_(2022-2024)/Uruguay%20Primera%20Divisi%C3%B3n_{temp_1_0}.xlsx")
    # Turquia
    TUR = pd.read_excel(
        f"https://github.com/futpythontrader/YouTube/raw/main/Bases_de_Dados/FootyStats/Bases_de_Dados_(2022-2024)/Turkey%20S%C3%BCper%20Lig_{temp_1}.xlsx")

    ## Concatenando todas as Planilhas/Bases
    df = [AUT, ARG, BUNDES, BR, BEL, CRO, CHI, CHINA, DIN, FRA, FIN, HOL, EST, ING, ITA, JAP, NOR, PAR, PORT, COR, ROM, SCOT, SPAIN, SUI, SWE, EUA, URU, TUR]
    df = pd.concat(df)

    ## Exclui certas colunas
    df = df.drop(['Nº', 'Id_Jogo', 'Season', 'Odd_H_HT', 'Odd_D_HT', 'Odd_A_HT', 'Odd_Over05_HT', 'Odd_Under05_HT',
                'Odd_Over15_HT', 'Odd_Under15_HT', 'Odd_Over25_HT', 'Odd_Under25_HT',
                'Odd_Over05_FT', 'Odd_Under05_FT', 'Odd_Over15_FT', 'Odd_Under15_FT',
                'Odd_Over25_FT', 'Odd_Under25_FT', 'Odd_BTTS_Yes', 'Odd_BTTS_No', 'Odd_DC_1X',
                'Odd_DC_12', 'Odd_DC_X2', 'PPG_Home_Pre', 'PPG_Away_Pre', 'PPG_Home',
                'PPG_Away', 'XG_Home_Pre', 'XG_Away_Pre', 'XG_Total_Pre', 'Odd_Corners_H', 'Odd_Corners_D',
                'Odd_Corners_A', 'Odd_Corners_Over75', 'Odd_Corners_Over85', 'Odd_Corners_Over95',
                'Odd_Corners_Over105', 'Odd_Corners_Over115'], axis=1)

    ## Mudar o formato da data
    # Converter a coluna 'Data' para o tipo datetime
    df['Date'] = pd.to_datetime(df['Date'])
    # Formatar a coluna 'Data' para o formato desejado
    df['Date'] = df['Date'].dt.strftime('%d/%m/%Y %H:%M')

    ## GOLS
    df['Over05_HT'] = df.apply(lambda row: 1 if (row['TotalGoals_HT'] > 0) else 0, axis=1)
    df['Over05_FT'] = df.apply(lambda row: 1 if (row['TotalGoals_FT'] > 0) else 0, axis=1)
    df['Over15_FT'] = df.apply(lambda row: 1 if (row['TotalGoals_FT'] > 1) else 0, axis=1)
    df['Over25_FT'] = df.apply(lambda row: 1 if (row['TotalGoals_FT'] > 2) else 0, axis=1)
    df['Over35_FT'] = df.apply(lambda row: 1 if (row['TotalGoals_FT'] > 3) else 0, axis=1)
    df['BTTS'] = df.apply(lambda row: 1 if (row['Goals_H_FT'] > 0 and row['Goals_A_FT'] > 0) else 0, axis=1)

    ## Cantos
    df['Winrate_cantos_H'] = df.apply(lambda row: 1 if (row['Corners_H_FT'] > row['Corners_A_FT']) else 0, axis=1)
    df['Winrate_cantos_A'] = df.apply(lambda row: 1 if (row['Corners_H_FT'] < row['Corners_A_FT']) else 0, axis=1)
    df['Cantos_Ov_75'] = df.apply(lambda row: 1 if (row['Corners_H_FT'] + row['Corners_A_FT'] > 7) else 0, axis=1)
    df['Cantos_Ov_85'] = df.apply(lambda row: 1 if (row['Corners_H_FT'] + row['Corners_A_FT'] > 8) else 0, axis=1)
    df['Cantos_Ov_95'] = df.apply(lambda row: 1 if (row['Corners_H_FT'] + row['Corners_A_FT'] > 9) else 0, axis=1)
    df['Cantos_Ov_105'] = df.apply(lambda row: 1 if (row['Corners_H_FT'] + row['Corners_A_FT'] > 10) else 0, axis=1)
    df['Cantos_Ov_115'] = df.apply(lambda row: 1 if (row['Corners_H_FT'] + row['Corners_A_FT'] > 11) else 0, axis=1)
    df['Cantos_Ov_125'] = df.apply(lambda row: 1 if (row['Corners_H_FT'] + row['Corners_A_FT'] > 12) else 0, axis=1)

    ## ML
    df['Winrate_H'] = df.apply(lambda row: 1 if (row['Goals_H_FT'] > row['Goals_A_FT']) else 0, axis=1)
    df['Winrate_A'] = df.apply(lambda row: 1 if (row['Goals_H_FT'] < row['Goals_A_FT']) else 0, axis=1)


    return df


temporada = st.sidebar.selectbox(
    'Temporada desejada:',
    ['2023-2024', '2024-2025'],
    index=1
)
st.session_state["temporada_selecionada"] = temporada


if temporada != None:
    df = load_data(temp=temporada)
    base_history_confrontos = load_base_geral()
    st.session_state["df_fut"] = df
    #display = st.sidebar.checkbox('Mostrar Bases') # Controlador de disposição


    # Ligas
    league = sorted(df["League"].unique())
    leagues = st.selectbox("League", league, index=None, placeholder="Choose League") # Dropdown 
    df_filtered = df[df["League"] == leagues]

    # Times
    times_ligas_home = sorted(df_filtered["Home"].unique())
    time_a = st.selectbox("Home Team", times_ligas_home, index=None, placeholder="Choose Home Team")
    df_filtered2 = df[df["Home"] == time_a]
    #if display:
    #    df_filtered2
    st.session_state["df_2"] = df_filtered2
    st.session_state["time_a"] = time_a



    times_ligas_away = sorted(df_filtered["Away"].unique())
    time_b = st.selectbox("Away Team", times_ligas_away, index=None, placeholder="Choose Away Team")
    df_filtered3 = df[df["Away"] == time_b]
    #if display:
    #    df_filtered3
    st.session_state["df_3"] = df_filtered3
    st.session_state["time_b"] = time_b



    if time_a and time_b != None:

        ### Base que traz todos os confrontos desde 2022
        historico = base_history_confrontos[
            ((base_history_confrontos['Home'] == time_a) & (base_history_confrontos['Away'] == time_b)) |
            ((base_history_confrontos['Home'] == time_b) & (base_history_confrontos['Away'] == time_a))
        ]

        progress_text = "Operation in progress. Please wait."
        my_bar = st.progress(0, text=progress_text)

        for percent_complete in range(100):
            time.sleep(0.01)
            my_bar.progress(percent_complete + 1, text=progress_text)
        time.sleep(1)
        my_bar.empty()

        # Media de gols marcados home home + Media de gols sofridos Away home
        ## Media de gols marcados home => Gols feitos em casa / qtd de jogos
        ## Media de gols sofridos Away => Gols sofridos fora de casa / qtd de jogos
        avg_home = (((df_filtered2['Goals_H_FT'].sum()/len(df_filtered2)) + (df_filtered3['Goals_H_FT'].sum()/len(df_filtered3))) / 2) 
        # Media de gols marcados away away + Media de gols sofridos home away
        ## Media de gols marcados away => Gols feitos fora de casa / qtd de jogos
        ## Media de gols sofridos home => Gols sofridos em casa / qtd de jogos
        avg_away = (((df_filtered3['Goals_A_FT'].sum()/len(df_filtered3)) + (df_filtered2['Goals_A_FT'].sum()/len(df_filtered2))) / 2)


        avg_cantos_home = (((df_filtered2['Corners_H_FT'].sum()/len(df_filtered2)) + (df_filtered3['Corners_H_FT'].sum()/len(df_filtered3))) / 2) 
        avg_cantos_away = (((df_filtered3['Corners_A_FT'].sum()/len(df_filtered3)) + (df_filtered2['Corners_A_FT'].sum()/len(df_filtered2))) / 2)




        prob_confronto = poisson_prob_gols(stats_home=avg_home, stats_away=avg_away)

        try:
            if prob_confronto[5]:
                avg_gols_confronto = round((avg_home + avg_away), 2)
                avg_cantos_confronto = round((avg_cantos_home + avg_cantos_away), 2)

                st.header(f'Probabilidades do confronto {time_a} X {time_b}')
                st.markdown(f'**Expecativa de gols para o confronto:** {avg_gols_confronto}')
                st.markdown(f'**Expecativa de cantos para o confronto:** {avg_cantos_confronto}')
                col1, col2, col3, col4, col5 = st.columns(5)
                col1.markdown(f'**% de Over 1.5:** {prob_confronto[0]}%')
                col2.markdown(f'**% de Over 2.5:** {prob_confronto[1]}%')
                col3.markdown(f'**% de Over 3.5:** {prob_confronto[2]}%')
                col4.markdown(f'**% Ambas:** {prob_confronto[3]}%')
                col5.markdown(f'**% Ambas & 2.5:** {prob_confronto[4]}%')

                # Selecionando as colunas desejadas
                st.divider()

                col1, col2 = st.columns([1, 0.06])
                on = col1.toggle("Show last games")
                if on:
                    #option_last_games = col2.select_slider(f"Last games", options=[3, 5, 10, 15], label_visibility="hidden")
                    option_last_games = col2.selectbox('', [3, 5, 10, 15], index=1, label_visibility="hidden")
                    

                    df_novo = df_filtered2[['Date', 'Home', 'Away', 'Goals_H_FT', 'Goals_A_FT', 'TotalCorners_FT',  'Corners_H_FT', 'Corners_A_FT', 'Winrate_H', 'Goals_H_HT', 'Goals_A_HT',
                                            'Over15_FT', 'Over25_FT', 'Over35_FT', 'BTTS', 'Over05_HT']].copy()
                    df_novo = df_novo.rename(columns={'TotalCorners_FT': 'Total de escanteios'})
                    df_novo = df_novo.rename(columns={'Winrate_H': 'Time com mais escanteios'})
                    df_novo['Confronto'] = df_novo['Home'] + ' x ' + df_novo['Away']
                    df_novo['Placar'] = df_novo['Goals_H_FT'].astype(str) + ' x ' + df_novo['Goals_A_FT'].astype(str)
                    df_novo['Date'] = pd.to_datetime(df_novo['Date'], format='%d/%m/%Y %H:%M')
                    # Calculando o total de escanteios de cada time
                    df_novo['Total de escanteios (Casa x Fora)'] = df_novo['Corners_H_FT'].astype(str) + ' x ' + df_novo['Corners_A_FT'].astype(str)
                    # Preenchendo a coluna 'Time com mais escanteios'
                    df_novo['Time com mais escanteios'] = df_novo.apply(
                        lambda row: f"{row['Total de escanteios (Casa x Fora)']} - {row['Home']}" if row['Time com mais escanteios'] == 1 
                        else f"{row['Total de escanteios (Casa x Fora)']} - {row['Away']}"
                        if row['Corners_H_FT'] != row['Corners_A_FT']  else f"{row['Total de escanteios (Casa x Fora)']} - Empate", axis=1)
                    df_novo['Win_H'] = df_novo.apply(lambda row: 1 if row['Goals_H_FT'] > row['Goals_A_FT'] else 0, axis=1)
                    df_novo = df_novo.sort_values(by='Date', ascending=False).head(option_last_games)
                    df_filtrado_home = pd.DataFrame(df_novo).reset_index(drop=True) 
                    df_filtrado_home['Date'] = df_filtrado_home['Date'].dt.strftime('%d de %B de %Y') 


                    df_novo = df_filtered3[['Date', 'Home', 'Away', 'Goals_H_FT', 'Goals_A_FT', 'TotalCorners_FT',  'Corners_H_FT', 'Corners_A_FT', 'Winrate_A', 'Goals_H_HT', 'Goals_A_HT',
                                            'Over15_FT', 'Over25_FT', 'Over35_FT', 'BTTS', 'Over05_HT']].copy()
                    df_novo = df_novo.rename(columns={'TotalCorners_FT': 'Total de escanteios'})
                    df_novo = df_novo.rename(columns={'Winrate_A': 'Time com mais escanteios'})
                    df_novo['Confronto'] = df_novo['Home'] + ' x ' + df_novo['Away']
                    df_novo['Placar'] = df_novo['Goals_H_FT'].astype(str) + ' x ' + df_novo['Goals_A_FT'].astype(str)
                    df_novo['Date'] = pd.to_datetime(df_novo['Date'], format='%d/%m/%Y %H:%M')
                    df_novo['Total de escanteios (Casa x Fora)'] = df_novo['Corners_H_FT'].astype(str) + ' x ' + df_novo['Corners_A_FT'].astype(str)
                    # Preenchendo a coluna 'Time com mais escanteios'
                    df_novo['Time com mais escanteios'] = df_novo.apply(
                        lambda row: f"{row['Total de escanteios (Casa x Fora)']} - {row['Away']}" if row['Time com mais escanteios'] == 1 
                        else f"{row['Total de escanteios (Casa x Fora)']} - {row['Home']}" 
                        if row['Corners_H_FT'] != row['Corners_A_FT']  else f"{row['Total de escanteios (Casa x Fora)']} - Empate", axis=1)
                    df_novo['Win_A'] = df_novo.apply(lambda row: 1 if row['Goals_H_FT'] < row['Goals_A_FT'] else 0, axis=1)
                    df_novo = df_novo.sort_values(by='Date', ascending=False).head(option_last_games)
                    df_filtrado_away = pd.DataFrame(df_novo).reset_index(drop=True)
                    df_filtrado_away['Date'] = df_filtrado_away['Date'].dt.strftime('%d de %B de %Y')
                    
                    

                    df_novo = historico[['Date', 'Home', 'Away', 'Goals_H_FT', 'Goals_A_FT', 'TotalCorners_FT',  'Corners_H_FT', 'Corners_A_FT', 'Winrate_H', 'Goals_H_HT', 'Goals_A_HT',
                                            'Over15_FT', 'Over25_FT', 'Over35_FT', 'BTTS', 'Over05_HT']].copy()
                    df_novo = df_novo.rename(columns={'TotalCorners_FT': 'Total de escanteios'})
                    df_novo = df_novo.rename(columns={'Winrate_H': 'Time com mais escanteios'})
                    df_novo['Confronto'] = df_novo['Home'] + ' x ' + df_novo['Away']
                    df_novo['Placar'] = df_novo['Goals_H_FT'].astype(str) + ' x ' + df_novo['Goals_A_FT'].astype(str)
                    df_novo['Date'] = pd.to_datetime(df_novo['Date'], format='%d/%m/%Y %H:%M')
                    # Calculando o total de escanteios de cada time
                    df_novo['Total de escanteios (Casa x Fora)'] = df_novo['Corners_H_FT'].astype(str) + ' x ' + df_novo['Corners_A_FT'].astype(str)
                    # Preenchendo a coluna 'Time com mais escanteios'
                    df_novo['Time com mais escanteios'] = df_novo.apply(
                        lambda row: f"{row['Total de escanteios (Casa x Fora)'].replace('.0', '')} - {row['Home']}" if row['Corners_H_FT'] > row['Corners_A_FT']
                        else f"{row['Total de escanteios (Casa x Fora)'].replace('.0', '')} - {row['Away']}"
                        if row['Corners_H_FT'] < row['Corners_A_FT']  else f"{row['Total de escanteios (Casa x Fora)'].replace('.0', '')} - Empate", axis=1)
                    df_novo = df_novo.sort_values(by='Date', ascending=False).head(len(historico))
                    df_filtrado_historico = pd.DataFrame(df_novo).reset_index(drop=True) 
                    df_filtrado_historico['Date'] = df_filtrado_historico['Date'].dt.strftime('%d de %B de %Y') 

                    # Contando as vitórias do Mandante (como mandante e visitante) no historico
                    vitorias_home = (
                        df_filtrado_historico[(df_filtrado_historico['Home'] == f'{time_a}') & (df_filtrado_historico['Goals_H_FT'] > df_filtrado_historico['Goals_A_FT'])].shape[0] +
                        df_filtrado_historico[(df_filtrado_historico['Away'] == f'{time_a}') & (df_filtrado_historico['Goals_A_FT'] > df_filtrado_historico['Goals_H_FT'])].shape[0]
                    )

                    # Contando as vitórias do Visitante (como mandante e visitante) no historico
                    vitorias_away = (
                        df_filtrado_historico[(df_filtrado_historico['Home'] == f'{time_b}' ) & (df_filtrado_historico['Goals_H_FT'] > df_filtrado_historico['Goals_A_FT'])].shape[0] +
                        df_filtrado_historico[(df_filtrado_historico['Away'] == f'{time_b}' ) & (df_filtrado_historico['Goals_A_FT'] > df_filtrado_historico['Goals_H_FT'])].shape[0]
                    )

                    # Contando os empates
                    empates = df_filtrado_historico[df_filtrado_historico['Goals_H_FT'] == df_filtrado_historico['Goals_A_FT']].shape[0]

                    

                    tab1, tab2, tab3 = st.tabs([f"{time_a}", f"{time_b}", f"H2H"]) 
                    with tab1:
                        tab1.text(f'Last {option_last_games} games')
                        col1, col2, col3, col4 = st.columns([1, 0.5, 0.5, 0.2])
                        col1.dataframe(df_filtrado_home[['Date', 'Confronto', 'Placar', 'Total de escanteios', 'Time com mais escanteios']], hide_index=True)
                        col2.metric(f"**Média de gols Marcados no 1ºT**", round(((df_filtrado_home['Goals_H_HT'].sum())/len(df_filtrado_home)),2))
                        col3.metric(f"**Média de gols sofridos no 1ºT**", round(((df_filtrado_home['Goals_A_HT'].sum())/len(df_filtrado_home)),2))
                        col4.metric(f"**% de Over 0.5HT**", round(df_filtrado_home['Over05_HT'].mean() * 100, 2))

                        

                        col1, col2, col3, col4 = st.columns([1, 0.5, 0.5, 0.2])
                        col1.text(f"Nos ultimos {option_last_games} jogos, o {time_a} venceu {round(df_filtrado_home['Win_H'].mean() * 100, 2)}% dos jogos em casa")
                        col2.metric(f"**Média de gols Marcados**", round(((df_filtrado_home['Goals_H_FT'].sum())/len(df_filtrado_home)),2))
                        col3.metric(f"**Média de gols Sofridos**", round(((df_filtrado_home['Goals_A_FT'].sum())/len(df_filtrado_home)),2))
                        col4.metric(f"**% do Ambas**", round(df_filtrado_home['BTTS'].mean() * 100, 2))
                        

                        col1, col2, col3, col4 = st.columns([1, 0.5, 0.5, 0.2])
                        col2.metric(f"**% de Over 1.5FT**", round(df_filtrado_home['Over15_FT'].mean() * 100, 2))
                        col3.metric(f"**% de Over 2.5FT**", round(df_filtrado_home['Over25_FT'].mean() * 100, 2))
                        col4.metric(f"**% de Over 3.5FT**", round(df_filtrado_home['Over35_FT'].mean() * 100, 2))


                    with tab2:
                        tab2.text(f'Last {option_last_games} games')
                        col1, col2, col3, col4 = st.columns([1, 0.5, 0.5, 0.2])
                        col1.dataframe(df_filtrado_away[['Date', 'Confronto', 'Placar', 'Total de escanteios', 'Time com mais escanteios']], hide_index=True)
                        col2.metric(f"**Média de gols Marcados no 1ºT**", round(((df_filtrado_away['Goals_A_HT'].sum())/len(df_filtrado_away)),2))
                        col3.metric(f"**Média de gols sofridos no 1ºT**", round(((df_filtrado_away['Goals_H_HT'].sum())/len(df_filtrado_away)),2))
                        col4.metric(f"**% de Over 0.5HT**", round(df_filtrado_away['Over05_HT'].mean() * 100, 2))

                        col1, col2, col3, col4 = st.columns([1, 0.5, 0.5, 0.2])
                        col1.text(f"Nos ultimos {option_last_games} jogos, o {time_b} venceu {round(df_filtrado_away['Win_A'].mean() * 100, 2)}% fora de casa")
                        col2.metric(f"**Média de gols Marcados**", round(((df_filtrado_away['Goals_A_FT'].sum())/len(df_filtrado_away)),2))
                        col3.metric(f"**Média de gols Sofridos**", round(((df_filtrado_away['Goals_H_FT'].sum())/len(df_filtrado_away)),2))
                        col4.metric(f"**% do Ambas**", round(df_filtrado_away['BTTS'].mean() * 100, 2))


                        col1, col2, col3, col4 = st.columns([1, 0.5, 0.5, 0.2])
                        col2.metric(f"**% de Over 1.5FT**", round(df_filtrado_away['Over15_FT'].mean() * 100, 2))
                        col3.metric(f"**% de Over 2.5FT**", round(df_filtrado_away['Over25_FT'].mean() * 100, 2))
                        col4.metric(f"**% de Over 3.5FT**", round(df_filtrado_away['Over35_FT'].mean() * 100, 2))

                    with tab3:
                        col1, col2, col3, col4 = st.columns([1, 0.5, 0.5, 0.5])
                        col1.text(f'Last {len(df_filtrado_historico)}')
                        col4.info('History may be incomplete', icon="ℹ️")
                        
                        col1, col2, col3, col4 = st.columns([1, 0.5, 0.5, 0.2])
                        col1.dataframe(df_filtrado_historico[['Date', 'Confronto', 'Placar', 'Total de escanteios', 'Time com mais escanteios']], hide_index=True)
                        col2.metric(f"**Média de gols Marcados no 1ºT**", round((((df_filtrado_historico['Goals_A_HT'].sum()) + (df_filtrado_historico['Goals_H_HT'].sum()))/len(df_filtrado_historico)),2),)
                        col3.metric(f"**Média de gols Marcados**", round((((df_filtrado_historico['Goals_A_FT'].sum()) + (df_filtrado_historico['Goals_H_FT'].sum()))/len(df_filtrado_historico)),2))
                        col4.metric(f"**% de Over 0.5HT**", round(df_filtrado_historico['Over05_HT'].mean() * 100, 2))


                        col1, col2, col3, col4, col5 = st.columns([1, 0.3, 0.3, 0.3, 0.3])
                        col1.text(f"Nos últimos {len(df_filtrado_historico)} jogos, {time_a} {vitorias_home}x{vitorias_away} {time_b}. Os outros {empates} jogos \nterminaram empatados.")
                        col2.metric(f"**% do Ambas**", round(df_filtrado_historico['BTTS'].mean() * 100, 2))
                        col3.metric(f"**% de Over 1.5FT**", round(df_filtrado_historico['Over15_FT'].mean() * 100, 2))
                        col4.metric(f"**% de Over 2.5FT**", round(df_filtrado_historico['Over25_FT'].mean() * 100, 2))
                        col5.metric(f"**% de Over 3.5FT**", round(df_filtrado_historico['Over35_FT'].mean() * 100, 2))

        except:
            pass
         
        #col1, col2, col3 = st.sidebar.columns([0.1, 0.1, 0.1])
        # Colocar o botão na última coluna (canto direito)
        #with col1:
            #btn = st.link_button("Gols", "https://footyanalyzer.streamlit.app/Gols")
            #if st.button("Gols"):
            #    st.switch_page("https://footyanalyzer.streamlit.app/Gols")
            
        #with col2:
            #btn = st.link_button("Cantos", "https://footyanalyzer.streamlit.app/Cantos")
            #if st.button("Cantos"):
            #    st.switch_page("https://footyanalyzer.streamlit.app/Cantos")


        #with col3:
            #btn = st.link_button("Chutes", "https://footyanalyzer.streamlit.app/Chutes")
            #if st.button("Chutes"):
            #    st.switch_page("D:\\João\\Python projects\\futebol\\st_fut\\pages\\4_⚽︎_Chutes.py")


