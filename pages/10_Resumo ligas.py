import pandas as pd
import streamlit as st
from connection import next_games
import numpy as np
from collections import Counter
import plotly.graph_objects as go


## ------------ FUNÇÕES -------------- ##

# Criar uma função para agregar dados para times de casa e fora
# Agregue as estatísticas para os times da casa e fora
def calcular_estatisticas(df_liga, coluna_time, coluna_gols_marcados, coluna_gols_sofridos, coluna_resultado):
    stats = df_liga.groupby(coluna_time).agg(
        #jogos_totais=('Column1', 'count'),
        vitorias=(coluna_resultado, lambda x: (x == 'W').sum()),
        empates=(coluna_resultado, lambda x: (x == 'D').sum()),
        derrotas=(coluna_resultado, lambda x: (x == 'L').sum()),
        gols_marcados=(coluna_gols_marcados, 'sum'),
        gols_sofridos=(coluna_gols_sofridos, 'sum')
    )
    stats['saldo_gols'] = stats['gols_marcados'] - stats['gols_sofridos']
    stats['jogos'] = stats['vitorias'] + stats['empates'] + stats['derrotas']
    stats['pts'] = (stats['vitorias'] * 3) + (stats['empates'] * 1)
    return stats


# Função para processar e calcular percentuais dos minutos
def minutes_gols(dataframe1, dataframe2):
    # Função para processar os minutos de uma coluna
    def process_minutes(dataframe):
        lista_minutos = []
        for x in dataframe:
            if x == "[]":
                continue
            try:
                x = x.strip("[]").replace("'", "")
                values = x.split(", ")
                lista_minutos.append([str(value) for value in values])  
            except:
                pass

        minutos_planos = []
        for sublist in lista_minutos:
            for m in sublist:
                if '+' in m:
                    m = m.split('+')
                    values_int = [int(value) for value in m]  # Somar os valores dentro da lista
                    total = sum(values_int)
                    minutos_planos.append(int(total))
                elif m in ('[', ']', "'"):
                    pass
                else:
                    minutos_planos.append(int(m))
        
        return minutos_planos

    # Processando ambas as colunas
    minutos_home = process_minutes(dataframe1)
    minutos_away = process_minutes(dataframe2)

    # Combinando os minutos de ambas as colunas
    minutos_totais = minutos_home + minutos_away

    # Definindo intervalos
    intervalos = [(0, 15), (16, 30), (31, 45), (46, 60), (61, 75), (76, 90), (91, 150)]
    intervalos_labels = ['0-15', '16-30', '31-45', '46-60', '61-75', '76-90', '91-150']
    intervalos_labels_2 = ['0-15', '16-30', '31-45', '46-60', '61-75', '76-90', '90+']

    # Contando gols em cada intervalo
    gols_por_intervalo = Counter()

    for minuto in minutos_totais:
        for start, end in intervalos:
            if start <= minuto <= end:
                gols_por_intervalo[f'{start}-{end}'] += 1
                break

    # Calculando a porcentagem de gols por intervalo
    total_gols = len(minutos_totais)
    percentuais = {k: (v / total_gols) * 100 for k, v in gols_por_intervalo.items()}

    # Ordenando o dicionário de percentuais
    percentuais_new = dict(sorted(percentuais.items()))

    # Garantindo que todos os intervalos estejam representados, mesmo com 0 gols
    percentuais_completos = [percentuais_new.get(label, 0) for label in intervalos_labels]

    return intervalos_labels_2, percentuais_completos



st.sidebar.markdown(
    """
    <div style="position: fixed; bottom: 0; width: 100%; text-align: left;">
        Desenvolvido por <a href="https://joaoluizp.github.io/portfolio_jluizp/" target="_blank" style="color: #3399ff; text-decoration: none;">João Luiz Pinheiro</a>
    </div>
    """, 
    unsafe_allow_html=True
)
st.html('style.html')


## ---------------- Lendo as bases para pegar os jogos dos dias ---------------- ##
columns_to_select = ['League', 'Date', 'Time', 'Rodada', 'Home', 'Away', 'XG_Home_Pre', 'XG_Away_Pre', 'XG_Total_Pre']
df_hoje = next_games.df_hoje
df_hoje = pd.DataFrame(df_hoje[columns_to_select])
df_hoje.rename(columns={
    'XG_Home_Pre': 'XG Home',
    'XG_Away_Pre': 'XG Away',
    'XG_Total_Pre': 'ExG'}, inplace=True)
#df_hoje[['ExG', 'ExC', '1.5+', '2.5+', '3.5+', 'BTTS', 'BTTS & 2.5+']] = df_hoje.apply(calcular_expectativa_gols_cantos_confronto, axis=1, result_type='expand')
df_hoje['Time'] = pd.to_datetime(df_hoje['Time']).dt.strftime('%H:%M')





df_amanha = next_games.df_amanha
df_amanha = pd.DataFrame(df_amanha[columns_to_select])
df_amanha.rename(columns={
    'XG_Home_Pre': 'XG Home',
    'XG_Away_Pre': 'XG Away',
    'XG_Total_Pre': 'ExG'}, inplace=True)
#df_amanha[['ExG', 'ExC', '1.5+', '2.5+', '3.5+', 'BTTS', 'BTTS & 2.5+']] = df_hoje.apply(calcular_expectativa_gols_cantos_confronto, axis=1, result_type='expand')
df_amanha['Time'] = pd.to_datetime(df_amanha['Time']).dt.strftime('%H:%M')



try:
    df_depois_de_amanha = next_games.df_depois_de_amanha
    df_depois_de_amanha = pd.DataFrame(df_depois_de_amanha[columns_to_select])
    df_depois_de_amanha.rename(columns={
        'XG_Home_Pre': 'XG Home',
        'XG_Away_Pre': 'XG Away',
        'XG_Total_Pre': 'ExG'}, inplace=True)
    #df_depois_de_amanha[['ExG', 'ExC', '1.5+', '2.5+', '3.5+', 'BTTS', 'BTTS & 2.5+']] = df_hoje.apply(calcular_expectativa_gols_cantos_confronto, axis=1, result_type='expand')
    df_depois_de_amanha['Time'] = pd.to_datetime(df_depois_de_amanha['Time']).dt.strftime('%H:%M')
except:
    df_depois_de_amanha = None
    pass


try:
    jogos_do_dia_d3 = pd.concat([df_hoje, df_amanha, df_depois_de_amanha])
except:
    jogos_do_dia_d3 = pd.concat([df_hoje, df_amanha])

if 'df_fut' not in st.session_state:
    st.toast('Return to the "Selecionar-Confronto" tab to update the database and return to this page again.', icon=":material/report:")
    
    pass

else:
    df = st.session_state["df_fut"]

    temporada_selecionada = st.session_state["temporada_selecionada"]
    st.sidebar.text(f"Temporada selecionada: {temporada_selecionada}")


    # Ligas
    league = sorted(df["League"].unique())
    leagues = st.selectbox("League", league, index=None, placeholder="Choose League") # Dropdown 
    df_filtered = df[df["League"] == leagues]



    if leagues != None:

        
        st.write('')
        tab1, tab2, tab3, tab4, tab5 = st.tabs(["Table", "Home", "Away", "Stats", "Next Games (D+3)"]) 

        with tab1:
            #df_filtered

            # Calcular estatísticas para times da casa e fora
            stats_home = calcular_estatisticas(df_filtered, 'Home', 'Goals_H_FT', 'Goals_A_FT', 'Resultado_H')
            stats_away = calcular_estatisticas(df_filtered, 'Away', 'Goals_A_FT', 'Goals_H_FT', 'Resultado_A')

            # Somar as estatísticas de casa e fora
            classificacao = stats_home.add(stats_away, fill_value=0)

            # Ordene a tabela pela quantidade de pontos e depois pelo saldo de gols
            classificacao = classificacao.sort_values(by=['pts', 'saldo_gols', 'vitorias', 'gols_marcados'], ascending=False)

            # Adicionar a colocação e ajustar o índice
            classificacao = classificacao.reset_index()
            classificacao.rename(columns={'index': 'Time'}, inplace=True)  # Renomeia a coluna do índice para 'Time'
            classificacao.insert(0, 'colocacao', range(1, len(classificacao) + 1))  # Adiciona a colocação como a primeira coluna
            classificacao = classificacao.set_index('colocacao')  # Define a colocação como o índice


            # Obtenha a lista dos últimos 5 jogos para cada time
            df_filtered['Date'] = pd.to_datetime(df_filtered['Date'], errors='coerce')
            def ultimos_5_jogos(time):
                #print(f"Verificando jogos para o time: {time}")

                df_time_home = df_filtered[df_filtered['Home'] == time]
                df_time_away = df_filtered[df_filtered['Away'] == time]
                df_time = pd.concat([df_time_home, df_time_away])
                df_time = df_time.sort_values(by='Date', ascending=False)

                #print(df_time)
                #df_time.to_excel("df_time.xlsx")
                
                def resultado(row):
                    if row['Home'] == time:
                        return 'W' if row['Resultado_H'] == 'W' else 'D' if row['Resultado_H'] == 'D' else 'L'
                    else:
                        return 'W' if row['Resultado_A'] == 'W' else 'D' if row['Resultado_A'] == 'D' else 'L'
                
                resultados = df_time.apply(resultado, axis=1).head(5).tolist()
                resultados = resultados[::-1]  # Inverter a lista
                return resultados + [''] * (5 - len(resultados))  # Preenche com '' se houver menos de 5 jogos

            # Adicione a coluna com os últimos 5 resultados
            classificacao['ultimos_5_jogos'] = classificacao['Home'].apply(ultimos_5_jogos)


            # Renomeando as colunas
            classificacao.rename(columns={
                'Home': 'Time',
                'vitorias': 'V',
                'empates': 'E',
                'derrotas': 'D',
                'gols_marcados': 'GP',
                'gols_sofridos': 'GA',
                'saldo_gols': 'SG',
                'jogos': 'MP',
                'pts': 'PTS',
                'ultimos_5_jogos': 'Last 5'
            }, inplace=True)

            classificacao.index.name = ''
            
            if len(classificacao) == 20:
                height = 738
            elif len(classificacao) == 10:
                height = 388
            elif len(classificacao) == 12:
                height = 458
            elif len(classificacao) == 16:
                height = 598
            elif len(classificacao) == 18:
                height = 668
            elif len(classificacao) == 19:
                height = 704
            else:
                height = 738

            st.dataframe(classificacao[['Time', 'MP', 'V', 'E', 'D', 'GP', 'GA', 'SG', 'PTS', 'Last 5']].head(20), hide_index=False, width=1500, height=height, use_container_width=True)
    

        with tab2:

            stats_home = calcular_estatisticas(df_filtered, 'Home', 'Goals_H_FT', 'Goals_A_FT', 'Resultado_H')

            classificacao = stats_home.sort_values(by=['pts', 'saldo_gols', 'vitorias', 'gols_marcados'], ascending=False)

            # Adicionar a colocação e ajustar o índice
            classificacao = classificacao.reset_index()
            classificacao.rename(columns={'index': 'Time'}, inplace=True)  # Renomeia a coluna do índice para 'Time'
            classificacao.insert(0, 'colocacao', range(1, len(classificacao) + 1))  # Adiciona a colocação como a primeira coluna
            classificacao = classificacao.set_index('colocacao')  # Define a colocação como o índice


            # Obtenha a lista dos últimos 5 jogos para cada time
            df_filtered['Date'] = pd.to_datetime(df_filtered['Date'], errors='coerce')
            def ultimos_5_jogos(time):
                #print(f"Verificando jogos para o time: {time}")

                df_time_home = df_filtered[df_filtered['Home'] == time]
                df_time_away = df_filtered[df_filtered['Away'] == time]
                df_time = pd.concat([df_time_home, df_time_away])
                df_time = df_time.sort_values(by='Date', ascending=False)

                #print(df_time)
                #df_time.to_excel("df_time.xlsx")
                
                def resultado(row):
                    if row['Home'] == time:
                        return 'W' if row['Resultado_H'] == 'W' else 'D' if row['Resultado_H'] == 'D' else 'L'
                    else:
                        return 'W' if row['Resultado_A'] == 'W' else 'D' if row['Resultado_A'] == 'D' else 'L'
                
                resultados = df_time.apply(resultado, axis=1).head(5).tolist()
                resultados = resultados[::-1]  # Inverter a lista
                return resultados + [''] * (5 - len(resultados))  # Preenche com '' se houver menos de 5 jogos

            # Adicione a coluna com os últimos 5 resultados
            classificacao['ultimos_5_jogos'] = classificacao['Home'].apply(ultimos_5_jogos)


            # Renomeando as colunas
            classificacao.rename(columns={
                'Home': 'Time',
                'vitorias': 'V',
                'empates': 'E',
                'derrotas': 'D',
                'gols_marcados': 'GP',
                'gols_sofridos': 'GA',
                'saldo_gols': 'SG',
                'jogos': 'MP',
                'pts': 'PTS',
                'ultimos_5_jogos': 'Last 5'
            }, inplace=True)

            classificacao.index.name = ''

            if len(classificacao) == 20:
                height = 738
            elif len(classificacao) == 10:
                height = 388
            elif len(classificacao) == 12:
                height = 458
            elif len(classificacao) == 16:
                height = 598
            elif len(classificacao) == 18:
                height = 668
            elif len(classificacao) == 19:
                height = 704
            else:
                height = 738

                                
            st.dataframe(classificacao[['Time', 'MP', 'V', 'E', 'D', 'GP', 'GA', 'SG', 'PTS', 'Last 5']].head(20), hide_index=False, width=1500, height=height, use_container_width=True)


        with tab3:

            stats_away = calcular_estatisticas(df_filtered, 'Away', 'Goals_A_FT', 'Goals_H_FT', 'Resultado_A')

            classificacao = stats_away.sort_values(by=['pts', 'saldo_gols', 'vitorias', 'gols_marcados'], ascending=False)

            # Adicionar a colocação e ajustar o índice
            classificacao = classificacao.reset_index()
            classificacao.rename(columns={'index': 'Time'}, inplace=True)  # Renomeia a coluna do índice para 'Time'
            classificacao.insert(0, 'colocacao', range(1, len(classificacao) + 1))  # Adiciona a colocação como a primeira coluna
            classificacao = classificacao.set_index('colocacao')  # Define a colocação como o índice


            # Obtenha a lista dos últimos 5 jogos para cada time
            df_filtered['Date'] = pd.to_datetime(df_filtered['Date'], errors='coerce')
            def ultimos_5_jogos(time):
                #print(f"Verificando jogos para o time: {time}")

                df_time_home = df_filtered[df_filtered['Home'] == time]
                df_time_away = df_filtered[df_filtered['Away'] == time]
                df_time = pd.concat([df_time_home, df_time_away])
                df_time = df_time.sort_values(by='Date', ascending=False)

                #print(df_time)
                #df_time.to_excel("df_time.xlsx")
                
                def resultado(row):
                    if row['Away'] == time:
                        return 'W' if row['Resultado_H'] == 'W' else 'D' if row['Resultado_H'] == 'D' else 'L'
                    else:
                        return 'W' if row['Resultado_A'] == 'W' else 'D' if row['Resultado_A'] == 'D' else 'L'
                
                resultados = df_time.apply(resultado, axis=1).head(5).tolist()
                resultados = resultados[::-1]  # Inverter a lista
                return resultados + [''] * (5 - len(resultados))  # Preenche com '' se houver menos de 5 jogos

            # Adicione a coluna com os últimos 5 resultados
            classificacao['ultimos_5_jogos'] = classificacao['Away'].apply(ultimos_5_jogos)


            # Renomeando as colunas
            classificacao.rename(columns={
                'Away': 'Time',
                'vitorias': 'V',
                'empates': 'E',
                'derrotas': 'D',
                'gols_marcados': 'GP',
                'gols_sofridos': 'GA',
                'saldo_gols': 'SG',
                'jogos': 'MP',
                'pts': 'PTS',
                'ultimos_5_jogos': 'Last 5'
            }, inplace=True)

            classificacao.index.name = ''

            if len(classificacao) == 20:
                height = 738
            elif len(classificacao) == 10:
                height = 388
            elif len(classificacao) == 12:
                height = 458
            elif len(classificacao) == 16:
                height = 598
            elif len(classificacao) == 18:
                height = 668
            elif len(classificacao) == 19:
                height = 704
            else:
                height = 738
                                
            st.dataframe(classificacao[['Time', 'MP', 'V', 'E', 'D', 'GP', 'GA', 'SG', 'PTS', 'Last 5']].head(20), hide_index=False, width=1500, height=height, use_container_width=True)


        with tab4:
            
             ## ========= GOLS  ========= ##
            #st.write('')
            col0, col0_1 = st.columns([0.5, 0.5])
            col0_1.subheader('1X2', help="Estatistica de gols do campeonato")
            st.write('')

            home_win_count = df_filtered['Resultado_H'].value_counts().get('W', 0)
            away_win_count = df_filtered['Resultado_A'].value_counts().get('W', 0)
            total_games = len(df_filtered)
            home_win_percentage = round((home_win_count / total_games) * 100,2)
            away_win_percentage = round((away_win_count / total_games) * 100,2)
            draw_percentage = round(100 - home_win_percentage - away_win_percentage,2)

            # Contar os clean sheets do time da casa (Goals_A_FT == 0)
            home_clean_sheets_count = len(df_filtered[df_filtered['Goals_A_FT'] == 0])
            # Contar os clean sheets do time visitante (Goals_H_FT == 0)
            away_clean_sheets_count = len(df_filtered[df_filtered['Goals_H_FT'] == 0])
            clean_sheets_geral = len(df_filtered[df_filtered['TotalGoals_FT'] == 0])
            # Calcular as porcentagens de clean sheets
            home_clean_sheet_percentage = round((home_clean_sheets_count / total_games) * 100, 2)
            away_clean_sheet_percentage = round((away_clean_sheets_count / total_games) * 100, 2)
            clean_sheets_geral_prcentage = round((clean_sheets_geral / total_games) * 100, 2)

            col0, col1, col2, col3 = st.columns([0.3, 0.5, 0.5, 0.5])
            col0.text('1x2:')
            col1.metric(f"Home Win", home_win_percentage)
            col2.metric(f"Draw", draw_percentage)
            col3.metric(f"Away Win", away_win_percentage)


            col0, col1, col2, col3 = st.columns([0.3, 0.5, 0.5, 0.5])
            col0.text('Clean Sheets:')
            col1.metric(f"Home Clean Sheets", home_clean_sheet_percentage)
            col2.metric(f"Away Clean Sheets", away_clean_sheet_percentage)
            col3.metric(f"Clean Sheets", clean_sheets_geral_prcentage)
            



            ## ========= GOLS  ========= ##
            st.write('')
            st.write('')
            st.write('')
            col0, col0_1 = st.columns([0.44, 0.5])
            col0_1.subheader('Goal Heatmap', help="Estatistica de gols do campeonato")
            st.write('')

            minutes_home = minutes_gols(df_filtered['Goals_H_Minutes'], df_filtered['Goals_A_Minutes'])
            # Plotando o gráfico
            # Create the Plotly figure
            fig = go.Figure(
                data=[go.Bar(x=minutes_home[0], y=minutes_home[1])],
                layout=dict(
                    title='Percentual de Gols por Intervalo de Minutos',
                    xaxis_title='Intervalo de Minutos',
                    yaxis_title='Percentual de Gols (%)',
                    # Adjust layout options as needed
                )
            )
            

            col1, col2, col3, col3_1, col3_2, col3_3 = st.columns([0.3, 0.5, 0.5, 0.5, 0.5, 0.5])
            col1.text('Dados HT:')
            #col2.metric(f"Total de Gols Marcados no 1º Tempo - {time_a}", df_filtered2['Goals_H_HT'].sum())
            #col3.metric(f"Total de Gols Sofridos no 1º Tempo - {time_a}", df_filtered2['Goals_A_HT'].sum())
            col2.metric(f"Goals HT/ Match", round(((df_filtered['TotalGoals_HT'].sum())/len(df_filtered)),2))
            col3.metric(f"Goals HT (Home)", round(((df_filtered['Goals_H_HT'].sum())/len(df_filtered)),2))
            col3_1.metric(f"Goals HT (Away)", round(((df_filtered['Goals_A_HT'].sum())/len(df_filtered)),2))
            col3_2.metric(f"% de Over 0.5HT", round(df_filtered['Over05_HT'].mean() * 100, 2))

            st.write('')
            st.write('')
            col4, col5, col6, col7, col8, col9 = st.columns([0.3, 0.5, 0.5, 0.5, 0.5, 0.5])
            col4.text('Dados FT:')
            col5.metric(f"Goals / Match", round(((df_filtered['TotalGoals_FT'].sum())/len(df_filtered)),2))
            col6.metric(f"Goals (Home)", round(((df_filtered['Goals_H_FT'].sum())/len(df_filtered)),2))
            col7.metric(f"Goals (Away)", round(((df_filtered['Goals_A_FT'].sum())/len(df_filtered)),2))

            st.write('')
            st.write('')
            col4, col5, col6, col7, col8, col9 = st.columns([0.3, 0.5, 0.5, 0.5, 0.5, 0.5])
            col4.text('Over +:')
            col5.metric(f"% de Over 0.5", round(df_filtered['Over05_FT'].mean() * 100, 2))
            col6.metric(f"% de Over 1.5", round(df_filtered['Over15_FT'].mean() * 100, 2))
            col7.metric(f"% de Over 2.5", round(df_filtered['Over25_FT'].mean() * 100, 2))
            col8.metric(f"% de Over 3.5", round(df_filtered['Over35_FT'].mean() * 100, 2))
            col9.metric(f"% do Ambas", round(df_filtered['BTTS'].mean() * 100, 2))

            st.write('')
            st.plotly_chart(fig, use_container_width=True)


            ## ========= CANTOS  ========= ##
            st.write('')
            st.write('')
            st.write('')
            col0, col0_1 = st.columns([0.5, 0.5])
            col0_1.subheader('Corners', help="Estatistica de cantos do campeonato")
            st.write('')

        
            col0, col1, col2, col3 = st.columns([0.5, 1, 1, 1])
            col0.text('Corners ML :')
            col1.metric(f"Corners ML/ Match (Home)", round(df_filtered['Winrate_cantos_H'].mean() * 100, 2))
            col2.metric(f"Corners ML / Match (Away)", round(df_filtered['Winrate_cantos_A'].mean() * 100, 2))
            
            st.write('')
            st.write('')
            col0, col1, col2, col3 = st.columns([0.5, 1, 1, 1])
            col0.text('Medias:')
            col1.metric(f"Corners / Match", round(((df_filtered['TotalCorners_FT'].sum())/len(df_filtered)),2))
            col2.metric(f"Corners / Match (Home)", round(((df_filtered['Corners_H_FT'].sum())/len(df_filtered)),2))
            col3.metric(f"Corners / Match (Away)", round(((df_filtered['Corners_A_FT'].sum())/len(df_filtered)),2))


            st.write('')
            st.write('')
            col4, col5, col6, col7, col8, col9 = st.columns([0.3, 0.5, 0.5, 0.5, 0.5, 0.5])
            col4.text('Over +:')
            col5.metric(f"% de Over 8.5", round(df_filtered['Cantos_Ov_85'].mean() * 100, 2))
            col6.metric(f"% de Over 9.5", round(df_filtered['Cantos_Ov_95'].mean() * 100, 2))
            col7.metric(f"% de Over 10.5", round(df_filtered['Cantos_Ov_105'].mean() * 100, 2))
            col8.metric(f"% de Over 11.5", round(df_filtered['Cantos_Ov_115'].mean() * 100, 2))
            col9.metric(f"% de Over 12.5", round(df_filtered['Cantos_Ov_125'].mean() * 100, 2))
        


            ## ========= CHUTES  ========= ##
            st.write('')
            st.write('')
            st.write('')
            col0, col0_1 = st.columns([0.5, 0.5])
            col0_1.subheader('Shots', help="Estatistica de chutes do campeonato")
            st.write('')

            col0, col1, col2, col3 = st.columns([0.5, 1, 1, 1])
            col0.text('Total:')
            col1.metric(f"Shots / Match (Home)", round(((df_filtered['Shots_H'].sum())/len(df_filtered)),2))
            col2.metric(f"Shots / Match (Away)", round(((df_filtered['Shots_A'].sum())/len(df_filtered)),2))
            col3.metric(f"Shots per Match", round(((df_filtered['Shots_H'].sum() + df_filtered['Shots_A'].sum()) / len(df_filtered)), 2))

            st.write('')

            col0, col1, col2, col3 = st.columns([0.5, 1, 1, 1])
            col0.text('On Goal:')
            col1.metric(f"Shots on goal / Match (Home)", round(((df_filtered['ShotsOnTarget_H'].sum())/len(df_filtered)),2))
            col2.metric(f"Shots on goal / Match (Away)", round(((df_filtered['ShotsOnTarget_A'].sum())/len(df_filtered)),2))
            col3.metric(f"Shots on goal per Match", round(((df_filtered['ShotsOnTarget_H'].sum() + df_filtered['ShotsOnTarget_A'].sum()) / len(df_filtered)), 2))



            #df_filtered
            

        with tab5:

            jogos_do_dia_d3 = jogos_do_dia_d3[jogos_do_dia_d3['League'] == leagues]

            st.dataframe(jogos_do_dia_d3[['Date', 'Time', 'Rodada', 'Home', 'Away', 'XG Home', 'XG Away', 'ExG']], hide_index=True, width=1500, use_container_width=True)
