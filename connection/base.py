import datetime
import pandas as pd
from sqlalchemy import create_engine
import psycopg2
import time
import streamlit as st


temporada_selecionada = st.session_state["temporada_selecionada"]


if temporada_selecionada == '2023-2024':
    temp_1 = 20232024
    temp_1_0 = 2023
elif temporada_selecionada == '2024-2025':
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
            'Odd_Over15_HT', 'Odd_Under15_HT', 'Odd_Over25_HT', 'Odd_Under25_HT', 'Odd_H_FT',
            'Odd_D_FT', 'Odd_A_FT', 'Odd_Over05_FT', 'Odd_Under05_FT', 'Odd_Over15_FT', 'Odd_Under15_FT',
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