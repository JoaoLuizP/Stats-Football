import datetime
import pandas as pd



# Obtém a data atual
hoje = datetime.datetime.now().date()
# Cria um objeto timedelta representando um dia
um_dia = datetime.timedelta(days=1)
# Calcula os dois dias seguintes
amanha = hoje + um_dia
depois_de_amanha = hoje + 2 * um_dia


hoje = hoje.strftime("%Y-%m-%d")
amanha = amanha.strftime("%Y-%m-%d")
depois_de_amanha = depois_de_amanha.strftime("%Y-%m-%d")



url_hoje = f'https://raw.githubusercontent.com/futpythontrader/YouTube/main/Jogos_do_Dia/FootyStats/Jogos_do_Dia_FootyStats_{hoje}.csv'
url_amanha = f'https://raw.githubusercontent.com/futpythontrader/YouTube/main/Jogos_do_Dia/FootyStats/Jogos_do_Dia_FootyStats_{amanha}.csv'
url_depois_de_amanha = f'https://raw.githubusercontent.com/futpythontrader/YouTube/main/Jogos_do_Dia/FootyStats/Jogos_do_Dia_FootyStats_{depois_de_amanha}.csv'


columns_to_select = ['League', 'Date', 'Time', 'Rodada', 'Home', 'Away']


# Ler o arquivo CSV
df_hoje = pd.read_csv(url_hoje)
df_amanha = pd.read_csv(url_amanha)
try:
    df_depois_de_amanha = pd.read_csv(url_depois_de_amanha)

    filtered_df_hoje = df_hoje[columns_to_select]
    filtered_df_amanha = df_amanha[columns_to_select]
    filtered_df_depois = df_depois_de_amanha[columns_to_select]

    join = [filtered_df_hoje, filtered_df_amanha, filtered_df_depois]
    base_jogos_dias = pd.concat(join)

except:

    filtered_df_hoje = df_hoje[columns_to_select]
    filtered_df_amanha = df_amanha[columns_to_select]
    
    join = [filtered_df_hoje, filtered_df_amanha]
    base_jogos_dias = pd.concat(join)




# Exibir as primeiras linhas do DataFrame
#print(f"\n\n{base_jogos_dias}")








