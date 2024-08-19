import pandas as pd
import streamlit as st

st.set_page_config(layout="wide")
st.sidebar.markdown(
    """
    <div style="position: fixed; bottom: 0; width: 100%; text-align: left;">
        Desenvolvido por <a href="https://joaoluizp.github.io/portfolio_jluizp/" target="_blank" style="color: #3399ff; text-decoration: none;">João Luiz Pinheiro</a>
    </div>
    """, 
    unsafe_allow_html=True
)
data = st.session_state["df_fut"]

temporada_selecionada = st.session_state["temporada_selecionada"]
st.sidebar.text(f"Temporada selecionada: {temporada_selecionada}")


opcao_0 = st.sidebar.selectbox(
    'Mercado desejado:',
    ['Ambas Marcam', 'Gols', 'ML'],
    index=None
)


opcao_1 = st.sidebar.selectbox(
    'Total da lista:',
    [5, 10, 15, 20],
    index=1  # O índice 1 corresponde à segunda opção (10)
)

opcao_2 = st.sidebar.selectbox(
    'Minimos de jogos na temporada',
    [5, 10, 15, 20],
    index=1
)


col1, col2, col3 = st.columns([1, 1, 0.12])
with col1:
    if opcao_0 != None:
        st.markdown(f"### Melhores ligas para {opcao_0}")
    else:
        st.markdown(f"### Melhores ligas para ")
#with col3:
    #if st.button("Home"):
    #    st.switch_page("D:\\João\\Python projects\\futebol\\st_fut\\Home.py")

    
### LIGA ###
if opcao_0 == 'Ambas Marcam':
    df_home_btts = data.groupby('League').agg({'League': 'count', 'BTTS': 'sum' })
    df_home_btts['BTTS_Percent_League'] = (df_home_btts['BTTS'] / df_home_btts['League']) * 100
    # Ordenar e selecionar os 10 maiores
    if opcao_2 != None: 
        df_home_btts = df_home_btts[df_home_btts['League'] > opcao_2] # Filtrar para ligas com mais de 10 jogos em casa
    top10_home_btts = df_home_btts.sort_values(by='BTTS_Percent_League', ascending=False).head(opcao_1)
    df_final = pd.DataFrame(top10_home_btts)
    df_final_league = df_final.rename(columns={
        'League': 'Jogos totais',
        'BTTS': 'Jogos ambas',
        'BTTS_Percent_League': '% BTTS',
    })


    st.dataframe(df_final_league[['Jogos totais', 'Jogos ambas', '% BTTS']],
                column_config={
                    "% BTTS": st.column_config.ProgressColumn(
                        "% BTTS", format="%d", min_value=0, max_value=100
                    ),
                })


elif opcao_0 == 'Gols':

    ## Over 0.5 HT ##
    df_over_05_ht = data.groupby('League').agg({'League': 'count', 'Over05_HT': 'sum' })
    df_over_05_ht['Over05_HT_Percent_League'] = (df_over_05_ht['Over05_HT'] / df_over_05_ht['League']) * 100
    # Ordenar e selecionar os 10 maiores
    if opcao_2 != None: 
        df_over_05_ht = df_over_05_ht[df_over_05_ht['League'] > opcao_2] # Filtrar para ligas com mais de 10 jogos em casa
    top10_over_05_ht = df_over_05_ht.sort_values(by='Over05_HT_Percent_League', ascending=False).head(opcao_1)
    df_final = pd.DataFrame(top10_over_05_ht)
    df_final_league_05_ht = df_final.rename(columns={
        'League': 'Jogos totais',
        'Over05_HT': 'Jogos over',
        'Over05_HT_Percent_League': '% Over 0.5 HT',
    })

    ## Over 1.5 FT ##
    df_over_15_ft = data.groupby('League').agg({'League': 'count', 'Over15_FT': 'sum' })
    df_over_15_ft['Over15_FT_Percent_League'] = (df_over_15_ft['Over15_FT'] / df_over_15_ft['League']) * 100
    # Ordenar e selecionar os 10 maiores
    if opcao_2 != None: 
        df_over_15_ft = df_over_15_ft[df_over_15_ft['League'] > opcao_2] # Filtrar para ligas com mais de 10 jogos em casa
    top10_over_15_ft = df_over_15_ft.sort_values(by='Over15_FT_Percent_League', ascending=False).head(opcao_1)
    df_final = pd.DataFrame(top10_over_15_ft)
    df_final_league_15_ft = df_final.rename(columns={
        'League': 'Jogos totais',
        'Over15_FT': 'Jogos over',
        'Over15_FT_Percent_League': '% Over 1.5 FT',
    })


    ## Over 2.5 FT ##
    df_over_25_ft = data.groupby('League').agg({'League': 'count', 'Over25_FT': 'sum' })
    df_over_25_ft['Over25_FT_Percent_League'] = (df_over_25_ft['Over25_FT'] / df_over_25_ft['League']) * 100
    # Ordenar e selecionar os 10 maiores
    if opcao_2 != None: 
        df_over_25_ft = df_over_25_ft[df_over_25_ft['League'] > opcao_2] # Filtrar para ligas com mais de 10 jogos em casa
    top10_over_25_ft = df_over_25_ft.sort_values(by='Over25_FT_Percent_League', ascending=False).head(opcao_1)
    df_final = pd.DataFrame(top10_over_25_ft)
    df_final_league_25_ft = df_final.rename(columns={
        'League': 'Jogos totais',
        'Over25_FT': 'Jogos over',
        'Over25_FT_Percent_League': '% Over 2.5 FT',
    })

    ## Over 3.5 FT ##
    df_over_35_ft = data.groupby('League').agg({'League': 'count', 'Over35_FT': 'sum' })
    df_over_35_ft['Over35_FT_Percent_League'] = (df_over_35_ft['Over35_FT'] / df_over_35_ft['League']) * 100
    # Ordenar e selecionar os 10 maiores
    if opcao_2 != None: 
        df_over_35_ft = df_over_35_ft[df_over_35_ft['League'] > opcao_2] # Filtrar para ligas com mais de 10 jogos em casa
    top10_over_35_ft = df_over_35_ft.sort_values(by='Over35_FT_Percent_League', ascending=False).head(opcao_1)
    df_final = pd.DataFrame(top10_over_35_ft)
    df_final_league_35_ft = df_final.rename(columns={
        'League': 'Jogos totais',
        'Over35_FT': 'Jogos over',
        'Over35_FT_Percent_League': '% Over 3.5 FT',
    })




    col1, col2= st.columns(2)
    with col1:
        st.text(f'Over 0.5 HT')
        st.dataframe(df_final_league_05_ht[['Jogos totais', 'Jogos over', '% Over 0.5 HT']],
                    column_config={
                        "% Over 0.5 HT": st.column_config.ProgressColumn(
                            "% Over 0.5 HT", format="%d", min_value=0, max_value=100
                        ),
                    })
    with col2:
        st.text(f'Over 1.5 FT')
        st.dataframe(df_final_league_15_ft[['Jogos totais', 'Jogos over', '% Over 1.5 FT']],
                    column_config={
                        "% Over 1.5 FT": st.column_config.ProgressColumn(
                            "% Over 1.5 FT", format="%d", min_value=0, max_value=100
                        ),
                    })



    col3, col4= st.columns(2)
    with col3:
        st.text(f'Over 2.5 FT')
        st.dataframe(df_final_league_25_ft[['Jogos totais', 'Jogos over', '% Over 2.5 FT']],
                    column_config={
                        "% Over 2.5 FT": st.column_config.ProgressColumn(
                            "% Over 2.5 FT", format="%d", min_value=0, max_value=100
                        ),
                    })
    with col4:
        st.text(f'Over 3.5 FT')
        st.dataframe(df_final_league_35_ft[['Jogos totais', 'Jogos over', '% Over 3.5 FT']],
                    column_config={
                        "% Over 3.5 FT": st.column_config.ProgressColumn(
                            "% Over 3.5 FT", format="%d", min_value=0, max_value=100
                        ),
                    })



elif opcao_0 == 'ML':

    df_home_ml = data.groupby('League').agg({'League': 'count', 'Winrate_H': 'sum' })
    df_home_ml['Winrate_H_Percent_League'] = (df_home_ml['Winrate_H'] / df_home_ml['League']) * 100
    # Ordenar e selecionar os 10 maiores
    if opcao_2 != None: 
        df_home_ml = df_home_ml[df_home_ml['League'] > opcao_2] # Filtrar para ligas com mais de 10 jogos em casa
    top10_home_ml = df_home_ml.sort_values(by='Winrate_H_Percent_League', ascending=False).head(opcao_1)
    df_final = pd.DataFrame(top10_home_ml)
    df_final_league_home = df_final.rename(columns={
        'League': 'Jogos totais',
        'Winrate_H': 'Jogos Home Win',
        'Winrate_H_Percent_League': '% Winrate H',
    })

    df_away_ml = data.groupby('League').agg({'League': 'count', 'Winrate_A': 'sum' })
    df_away_ml['Winrate_A_Percent_League'] = (df_away_ml['Winrate_A'] / df_away_ml['League']) * 100
    # Ordenar e selecionar os 10 maiores
    if opcao_2 != None: 
        df_away_ml = df_away_ml[df_away_ml['League'] > opcao_2] # Filtrar para ligas com mais de 10 jogos em casa
    top10_away_ml = df_away_ml.sort_values(by='Winrate_A_Percent_League', ascending=False).head(opcao_1)
    df_final = pd.DataFrame(top10_away_ml)
    df_final_league_away = df_final.rename(columns={
        'League': 'Jogos totais',
        'Winrate_A': 'Jogos Away Win',
        'Winrate_A_Percent_League': '% Winrate A',
    })

    col1, col2= st.columns(2)
    with col1:
        st.text(f'Em casa')
        st.dataframe(df_final_league_home[['Jogos totais', 'Jogos Home Win', '% Winrate H']],
                    column_config={
                        "% Winrate H": st.column_config.ProgressColumn(
                            "% Winrate H", format="%d", min_value=0, max_value=100
                        ),
                    })
    with col2:
        st.text(f'Fora de casa')
        st.dataframe(df_final_league_away[['Jogos totais', 'Jogos Away Win', '% Winrate A']],
                    column_config={
                        "% Winrate A": st.column_config.ProgressColumn(
                            "% Winrate A", format="%d", min_value=0, max_value=100
                        ),
                    })
    
    my_large_df = pd.DataFrame(df_final_league_home)  # Your DataFrame
        


