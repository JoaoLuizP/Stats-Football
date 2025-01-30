import datetime
import pandas as pd
from sqlalchemy import create_engine
import psycopg2
import time
import json


# Lendo o arquivo config.json
try:
    with open('connection\json.json') as f:
        config_data = json.load(f)
except:
    with open('C:\\Users\\Pichau\\Documents\\GitHub\\Stats-Football\\connection\\json.json') as f:
        config_data = json.load(f)

# Acessando as informações
host = config_data['host']
senha = config_data['senha']
user = config_data['user']
port = config_data['port']

local_db = psycopg2.connect(
    user=user,
    password=senha,
    host=host,
    port=port,
    database="postgres")
engine_online = create_engine(f'postgresql://{user}:{senha}@{host}:{port}')



def verificar_tabela_se_existe(nome_tabela):
    try:
        query = pd.read_sql_query(f"""SELECT * FROM tembo.{nome_tabela}""", engine_online)

        return True
    except:
        return False
    
checa_se_tbl_existe = verificar_tabela_se_existe('base_geral')
if checa_se_tbl_existe:
    cursor = local_db.cursor()
    time.sleep(1.5)
    cursor.execute('DROP TABLE tembo.base_geral')
    local_db.commit()
    print('\nBase antiga excluída')




base2022_atual = pd.read_csv(
    "https://github.com/futpythontrader/YouTube/raw/main/Bases_de_Dados/FootyStats/Base_de_Dados_FootyStats_(2022_2025).csv"
)
base_atual_tradada = base2022_atual[base2022_atual != -1].dropna()


base_before_2022 = pd.read_csv(
    "https://github.com/futpythontrader/YouTube/raw/main/Bases_de_Dados/FootyStats/Base_de_Dados_FootyStats_(2006_2021).csv"
)
base_before_2022_tratada = base_before_2022[base_before_2022 != -1].dropna()

join_bases = [base_atual_tradada, base_before_2022_tratada]
df_final = pd.concat(join_bases)



## Exclui certas colunas
df = df_final.drop(['Id_Jogo', 'Season', 'Odd_H_HT', 'Odd_D_HT', 'Odd_A_HT', 'Odd_Over05_HT', 'Odd_Under05_HT',
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

df['dt_execucao'] = datetime.datetime.today()

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


df.to_sql("base_geral",  engine_online, schema='tembo', if_exists='append')

print('Base atualizada e subida!')