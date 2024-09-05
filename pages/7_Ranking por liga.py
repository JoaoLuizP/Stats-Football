import pandas as pd
import streamlit as st


st.sidebar.markdown(
    """
    <div style="position: fixed; bottom: 0; width: 100%; text-align: left;">
        Desenvolvido por <a href="https://joaoluizp.github.io/portfolio_jluizp/" target="_blank" style="color: #3399ff; text-decoration: none;">João Luiz Pinheiro</a>
    </div>
    """, 
    unsafe_allow_html=True
)
st.html('style.html')


data = st.session_state["df_fut"]

col1, col2, col3 = st.columns([1, 1, 0.12])
with col1:
    st.markdown(f"### Estatistica dos times na liga 📊 ")
st.empty()
st.divider()
st.empty()
#with col3:
#    if st.button("Home"):
#        st.switch_page("D:\\João\\Python projects\\futebol\\st_fut\\Home.py")


temporada_selecionada = st.session_state["temporada_selecionada"]

st.sidebar.text(f"Temporada selecionada: {temporada_selecionada}")

league = sorted(data["League"].unique())
leagues = st.selectbox("Ligas", league, index=None, placeholder="Choose League") # Dropdown 


if leagues != None:
    opcao_0 = st.selectbox(
        'Mercado desejado:',
        ['Ambas Marcam', 'Cantos', 'Gols', 'ML'],
        index=None
    )

    if opcao_0 == 'Gols':
        new_opcao_gols = st.selectbox(
        'Linha desejada:',
        ['Over 0.5 HT', 'Over 1.5 FT', 'Over 2.5 FT', 'Over 3.5 FT'],
        index=None
        )
    elif opcao_0 == 'Cantos':
        new_opcao_cantos = st.selectbox(
        'Linha desejada:',
        ['Over 7.5', 'Over 8.5', 'Over 9.5', 'Over 10.5', 'Over 11.5', 'Over 12.5'],
        index=None
        )
    else:
        pass
    

    df_league = data[data['League'] == leagues]


    if opcao_0 == 'Ambas Marcam':
        # Agrupa os dados por time e calcula as métricas desejadas
        ### HOME ###
        df_grouped = df_league.groupby('Home').agg(
            qtd_jogos=('Home', 'count'),
            jogos_ambas_marcam=('BTTS', 'sum'),
            gols_pro=('Goals_H_FT', 'sum'),
            gols_sofridos=('Goals_A_FT', 'sum')
        )
        # Calcula a porcentagem de jogos em que ambas marcam
        df_grouped['percent_ambas_marcam'] = round((df_grouped['jogos_ambas_marcam'] / df_grouped['qtd_jogos']) * 100, 2)
        # Ordena o DataFrame pela porcentagem de ambas marcam de forma decrescente
        df_sorted = df_grouped.sort_values(by='percent_ambas_marcam', ascending=False)
        df_final = pd.DataFrame(df_sorted)
        df_final_home_btts = df_final.rename(columns={
            'qtd_jogos': 'Jogos totais',
            'jogos_ambas_marcam': 'Jogos ambas',
            'percent_ambas_marcam': '% BTTS',
            'gols_pro': 'Gols Pró',
            'gols_sofridos': 'Gols Sofr.'
        })


        ### Away ###
        df_grouped = df_league.groupby('Away').agg(
            qtd_jogos=('Away', 'count'),
            jogos_ambas_marcam=('BTTS', 'sum'),
            gols_pro=('Goals_A_FT', 'sum'),
            gols_sofridos=('Goals_H_FT', 'sum')
        )
        # Calcula a porcentagem de jogos em que ambas marcam
        df_grouped['percent_ambas_marcam'] = round((df_grouped['jogos_ambas_marcam'] / df_grouped['qtd_jogos']) * 100, 2)
        # Ordena o DataFrame pela porcentagem de ambas marcam de forma decrescente
        df_sorted = df_grouped.sort_values(by='percent_ambas_marcam', ascending=False)
        df_final = pd.DataFrame(df_sorted)
        df_final_away_btts = df_final.rename(columns={
            'qtd_jogos': 'Jogos totais',
            'jogos_ambas_marcam': 'Jogos ambas',
            'percent_ambas_marcam': '% BTTS',
            'gols_pro': 'Gols Pró',
            'gols_sofridos': 'Gols Sofr.'
        })


        ### DE MODO GERAL ###
        # Agrupar por time e liga e calcular a soma de BTTS
        df_total_btts = df_league.groupby(['Home', 'League']).agg({'BTTS': 'sum'}).rename(columns={'BTTS': 'BTTS_Home'})
        df_total_btts['BTTS_Away'] = df_league.groupby(['Away', 'League']).agg({'BTTS': 'sum'})
        # Calcular o total de jogos por time e liga
        df_total_btts['Total_Games_Home'] = df_league.groupby(['Home', 'League']).size()
        df_total_btts['Total_Games_Away'] = df_league.groupby(['Away', 'League']).size()
        # Somar os jogos em casa e fora para o total de jogos
        df_total_btts['Total_Games'] = df_total_btts['Total_Games_Home'] + df_total_btts['Total_Games_Away']
        # Calcular o total de BTTS (em casa e fora)
        df_total_btts['BTTS_Total'] = df_total_btts['BTTS_Home'] + df_total_btts['BTTS_Away']
        # Calcular a porcentagem de BTTS no total de jogos
        df_total_btts['BTTS_Percent_Total'] = (df_total_btts['BTTS_Total'] / df_total_btts['Total_Games']) * 100
        top10_total_btts = df_total_btts.sort_values(by='BTTS_Percent_Total', ascending=False)
        df_final_boths = top10_total_btts.rename(columns={
            'Total_Games': 'Jogos totais',
            'BTTS_Total': 'Jogos ambas',
            'BTTS_Percent_Total': '% BTTS',
        })

        tab1, tab2, tab3 = st.tabs([f"Em casa", f"Fora de casa", f"Geral"])
        with tab1:
            st.dataframe(df_final_home_btts[['Jogos totais', 'Jogos ambas', '% BTTS', 'Gols Pró', 'Gols Sofr.']],
                    column_config={
                        "% BTTS": st.column_config.ProgressColumn(
                            "% BTTS", format="%d", min_value=0, max_value=100
                        ),
                    })
        with tab2:
            st.dataframe(df_final_away_btts[['Jogos totais', 'Jogos ambas', '% BTTS', 'Gols Pró', 'Gols Sofr.']],
                    column_config={
                        "% BTTS": st.column_config.ProgressColumn(
                            "% BTTS", format="%d", min_value=0, max_value=100
                        ),
                    })
        
        with tab3:
            st.dataframe(df_final_boths[['Jogos totais', 'Jogos ambas', '% BTTS']],
                        column_config={
                            "% BTTS": st.column_config.ProgressColumn(
                                "% BTTS", format="%d", min_value=0, max_value=100
                            ),
                        })
            

    elif opcao_0 == 'Cantos':

        if new_opcao_cantos == 'Over 7.5':
            number = 7
        elif new_opcao_cantos == 'Over 8.5':
            number = 8
        elif new_opcao_cantos == 'Over 9.5':
            number = 9
        elif new_opcao_cantos == 'Over 10.5':
            number = 10
        elif new_opcao_cantos == 'Over 11.5':
            number = 11
        else:
            number = 12
        
        if new_opcao_cantos != None:
            st.text(f' Linha: {new_opcao_cantos}')
        else:
            st.text(f' Linha: ')


        if new_opcao_cantos != None:
            ### HOME ###
            df_home_cantos = df_league.groupby(['Home', 'League']).agg({'Home': 'count', 'Corners_H_FT': 'sum',  'Corners_A_FT': 'sum', f'Cantos_Ov_{number}5': 'sum'})
            df_home_cantos[f'Percent_Cantos_Ov_{number}5'] = (df_home_cantos[f'Cantos_Ov_{number}5'] / df_home_cantos['Home']) * 100
            df_home_cantos['Avg_Corners_Pro'] = round((df_home_cantos['Corners_H_FT'] / df_home_cantos['Home']), 2)
            df_home_cantos['Avg_Corners_Sofr'] = round((df_home_cantos['Corners_A_FT'] / df_home_cantos['Home']), 2)
            top_home_cantos = df_home_cantos.sort_values(by=f'Percent_Cantos_Ov_{number}5', ascending=False)
            df_final = pd.DataFrame(top_home_cantos)
            df_final_home_cantos = df_final.rename(columns={
                'Home': 'Jogos totais',
                f'Cantos_Ov_{number}5': f'Jogos over {number}.5',
                f'Percent_Cantos_Ov_{number}5': f'% Ov {number}.5',
                'Avg_Corners_Pro': 'Avg Corners Pró',
                'Avg_Corners_Sofr': 'Avg Corners Sofr.'
            })

            ### AWAY ###
            df_away_cantos = df_league.groupby(['Away', 'League']).agg({'Away': 'count', 'Corners_H_FT': 'sum',  'Corners_A_FT': 'sum', f'Cantos_Ov_{number}5': 'sum'})
            df_away_cantos[f'Percent_Cantos_Ov_{number}5'] = (df_away_cantos[f'Cantos_Ov_{number}5'] / df_away_cantos['Away']) * 100
            df_away_cantos['Avg_Corners_Pro'] = round((df_away_cantos['Corners_H_FT'] / df_away_cantos['Away']), 2)
            df_away_cantos['Avg_Corners_Sofr'] = round((df_away_cantos['Corners_A_FT'] / df_away_cantos['Away']), 2)
            top_away_cantos = df_away_cantos.sort_values(by=f'Percent_Cantos_Ov_{number}5', ascending=False)
            df_final = pd.DataFrame(top_away_cantos)
            df_final_away_cantos = df_final.rename(columns={
                'Away': 'Jogos totais',
                f'Cantos_Ov_{number}5': f'Jogos over {number}.5',
                f'Percent_Cantos_Ov_{number}5': f'% Ov {number}.5',
                'Avg_Corners_Pro': 'Avg Corners Pró',
                'Avg_Corners_Sofr': 'Avg Corners Sofr.'
            })


            ### DE MODO GERAL ###
            # Agrupar por time e liga e calcular a soma de BTTS
            df_total_cantos = df_league.groupby(['Home', 'League']).agg({f'Cantos_Ov_{number}5': 'sum'}).rename(columns={f'Cantos_Ov_{number}5': f'Cantos_Ov_{number}5_Home'})
            df_total_cantos[f'Cantos_Ov_{number}5_Away'] = data.groupby(['Away', 'League']).agg({f'Cantos_Ov_{number}5': 'sum'})
            # Calcular o total de jogos por time e liga
            df_total_cantos['Total_Games_Home'] = df_league.groupby(['Home', 'League']).size()
            df_total_cantos['Total_Games_Away'] = df_league.groupby(['Away', 'League']).size()
            # Somar os jogos em casa e fora para o total de jogos
            df_total_cantos['Total_Games'] = df_total_cantos['Total_Games_Home'] + df_total_cantos['Total_Games_Away']
            # Calcular o total de BTTS (em casa e fora)
            df_total_cantos[f'Cantos_Ov_{number}5_Total'] = df_total_cantos[f'Cantos_Ov_{number}5_Home'] + df_total_cantos[f'Cantos_Ov_{number}5_Away']
            # Calcular a porcentagem de BTTS no total de jogos
            df_total_cantos[f'Cantos_Ov_{number}5_Percent_Total'] = (df_total_cantos[f'Cantos_Ov_{number}5_Total'] / df_total_cantos['Total_Games']) * 100
            top_total_cantos = df_total_cantos.sort_values(by=f'Cantos_Ov_{number}5_Percent_Total', ascending=False)
            df_final_boths_cantos = top_total_cantos.rename(columns={
                'Total_Games': 'Jogos totais',
                f'Cantos_Ov_{number}5_Total': f'Jogos over {number}.5',
                f'Cantos_Ov_{number}5_Percent_Total': f'% Ov {number}.5',
            })


            tab1, tab2, tab3 = st.tabs([f"Em casa", f"Fora de casa", f"Geral"]) 
            with tab1:
                st.dataframe(df_final_home_cantos[['Jogos totais', f'Jogos over {number}.5', f'% Ov {number}.5', 'Avg Corners Pró', 'Avg Corners Sofr.']],
                        column_config={
                            f"% Ov {number}.5": st.column_config.ProgressColumn(
                                f"% Ov {number}.5", format="%d", min_value=0, max_value=100
                            ),
                        })
            with tab2:
                st.dataframe(df_final_away_cantos[['Jogos totais', f'Jogos over {number}.5', f'% Ov {number}.5', 'Avg Corners Pró', 'Avg Corners Sofr.']],
                        column_config={
                            f"% Ov {number}.5": st.column_config.ProgressColumn(
                                f"% Ov {number}.5", format="%d", min_value=0, max_value=100
                            ),
                        })
                
            with tab3:
                st.dataframe(df_final_boths_cantos[['Jogos totais', f'Jogos over {number}.5', f'% Ov {number}.5']],
                            column_config={
                                f"% Ov {number}.5": st.column_config.ProgressColumn(
                                    f"% Ov {number}.5", format="%d", min_value=0, max_value=100
                                ),
                            })


    elif opcao_0 == 'ML':

        ### HOME ###
        df_home_ml = df_league.groupby(['Home', 'League']).agg({'Home': 'count', 'Goals_H_FT': 'sum',  'Goals_A_FT': 'sum', 'Winrate_H': 'sum'})
        df_home_ml['Percent_Winrate_H'] = round((df_home_ml['Winrate_H'] / df_home_ml['Home']) * 100, 2)
        top_home_ml = df_home_ml.sort_values(by='Percent_Winrate_H', ascending=False)
        df_final = pd.DataFrame(top_home_ml)
        df_final_home_ml = df_final.rename(columns={
            'Home': 'Jogos totais',
            'Winrate_H': 'Jogos Home Win',
            'Percent_Winrate_H': '% Home Win',
            'Goals_H_FT': 'Gols Pró',
            'Goals_A_FT': 'Gols Sofr.'
        })

        ### Away ###
        df_away_ml = df_league.groupby(['Away', 'League']).agg({'Away': 'count', 'Goals_H_FT': 'sum',  'Goals_A_FT': 'sum', 'Winrate_A': 'sum'})
        df_away_ml['Percent_Winrate_A'] = round((df_away_ml['Winrate_A'] / df_away_ml['Away']) * 100, 2)
        # Ordenar e selecionar os 10 maiores
        top_away_ml = df_away_ml.sort_values(by='Percent_Winrate_A', ascending=False)
        df_final = pd.DataFrame(top_away_ml)
        df_final_away_ml = df_final.rename(columns={
            'Away': 'Jogos totais',
            'Winrate_A': 'Jogos Away Win',
            'Percent_Winrate_A': '% Away Win',
            'Goals_A_FT': 'Gols Pró',
            'Goals_H_FT': 'Gols Sofr.'
        })

        ### DE MODO GERAL ###
        # Agrupar por time e liga e calcular a soma de BTTS
        df_total_ml = df_league.groupby(['Home', 'League']).agg({'Winrate_H': 'sum'}).rename(columns={'Winrate_H': 'Winrate_H_Home'})
        df_total_ml['Winrate_A_Away'] = data.groupby(['Away', 'League']).agg({'Winrate_A': 'sum'})
        # Calcular o total de jogos por time e liga
        df_total_ml['Total_Games_Home'] = data.groupby(['Home', 'League']).size()
        df_total_ml['Total_Games_Away'] = data.groupby(['Away', 'League']).size()
        # Somar os jogos em casa e fora para o total de jogos
        df_total_ml['Total_Games'] = df_total_ml['Total_Games_Home'] + df_total_ml['Total_Games_Away']
        # Calcular o total de BTTS (em casa e fora)
        df_total_ml['Winrate_Total'] = df_total_ml['Winrate_H_Home'] + df_total_ml['Winrate_A_Away']
        # Calcular a porcentagem de BTTS no total de jogos
        df_total_ml['Winrate_Percent_Total'] = (df_total_ml['Winrate_Total'] / df_total_ml['Total_Games']) * 100
        top_total_ml = df_total_ml.sort_values(by='Winrate_Percent_Total', ascending=False)
        df_final_boths_ml = top_total_ml.rename(columns={
            'Total_Games': 'Jogos totais',
            'Winrate_Total': 'Jogos Win',
            'Winrate_Percent_Total': '% Win',
        })



        tab1, tab2, tab3 = st.tabs([f"Em casa", f"Fora de casa", f"Geral"]) 
        with tab1:
            st.dataframe(df_final_home_ml[['Jogos totais', 'Jogos Home Win', '% Home Win', 'Gols Pró', 'Gols Sofr.']],
                    column_config={
                        "% Home Win": st.column_config.ProgressColumn(
                            "% Home Win", format="%d", min_value=0, max_value=100
                        ),
                    })
        with tab2:
            st.dataframe(df_final_away_ml[['Jogos totais', 'Jogos Away Win', '% Away Win', 'Gols Pró', 'Gols Sofr.']],
                    column_config={
                        "% Away Win": st.column_config.ProgressColumn(
                            "% Away Win", format="%d", min_value=0, max_value=100
                        ),
                    })
        

        with tab3:
            st.dataframe(df_final_boths_ml[['Jogos totais', 'Jogos Win', '% Win']],
                        column_config={
                            "% Win": st.column_config.ProgressColumn(
                                "% Win", format="%d", min_value=0, max_value=100
                            ),
                        })
            



    elif opcao_0 == 'Gols':

        if new_opcao_gols == 'Over 0.5 HT':
            variable = 'Over05_HT'
            variable_2 = 'Goals_H_HT'
            variable_3 = 'Goals_A_HT'

        elif new_opcao_gols == 'Over 1.5 FT':
            variable = 'Over15_FT'
        elif new_opcao_gols == 'Over 2.5 FT':
            variable = 'Over25_FT'
        elif new_opcao_gols == 'Over 3.5 FT':
            variable = 'Over35_FT'
        else:
            pass


        if new_opcao_gols in ('Over 1.5 FT', 'Over 2.5 FT', 'Over 3.5 FT'):
            variable_2 = 'Goals_H_FT'
            variable_3 = 'Goals_A_FT'

        if new_opcao_gols != None:
            st.text(f' Linha: {new_opcao_gols}')
        else:
            st.text(f' Linha: ')

        if opcao_0 != None and new_opcao_gols != None:

            ### HOME ###
            df_home_gols = df_league.groupby(['Home', 'League']).agg({'Home': 'count', f'{variable_2}': 'sum',  f'{variable_3}': 'sum', f'{variable}': 'sum'})
            df_home_gols[f'Percent_{variable}'] = (df_home_gols[f'{variable}'] / df_home_gols['Home']) * 100
            # Ordenar e selecionar os 10 maiores
            top_home_gols = df_home_gols.sort_values(by=f'Percent_{variable}', ascending=False)
            df_final = pd.DataFrame(top_home_gols)
            df_final_home_gols = df_final.rename(columns={
                'Home': 'Jogos totais',
                f'{variable}': f'Jogos {new_opcao_gols}',
                f'Percent_{variable}': f'% {new_opcao_gols}',
                f'{variable_2}': 'Gols Pró',
                f'{variable_3}': 'Gols Sofr.'
            })


            ### AWAY ###
            df_away_gols = df_league.groupby(['Away', 'League']).agg({'Away': 'count', f'{variable_2}': 'sum',  f'{variable_3}': 'sum', f'{variable}': 'sum'})
            df_away_gols[f'Percent_{variable}'] = (df_away_gols[f'{variable}'] / df_away_gols['Away']) * 100
            # Ordenar e selecionar os 10 maiores
            top_away_gols = df_away_gols.sort_values(by=f'Percent_{variable}', ascending=False)
            df_final = pd.DataFrame(top_away_gols)
            df_final_away_gols = df_final.rename(columns={
                'Away': 'Jogos totais',
                f'{variable}': f'Jogos {new_opcao_gols}',
                f'Percent_{variable}': f'% {new_opcao_gols}',
                f'{variable_3}': 'Gols Pró',
                f'{variable_2}': 'Gols Sofr.'
            })

            ### DE MODO GERAL ###
            # Agrupar por time e liga e calcular a soma de BTTS
            df_total_gols = df_league.groupby(['Home', 'League']).agg({f'{variable}': 'sum'}).rename(columns={f'{variable}': f'{variable}_Home'})
            df_total_gols[f'{variable}_Away'] = df_league.groupby(['Away', 'League']).agg({f'{variable}': 'sum'})
            # Calcular o total de jogos por time e liga
            df_total_gols['Total_Games_Home'] = df_league.groupby(['Home', 'League']).size()
            df_total_gols['Total_Games_Away'] = df_league.groupby(['Away', 'League']).size()
            # Somar os jogos em casa e fora para o total de jogos
            df_total_gols['Total_Games'] = df_total_gols['Total_Games_Home'] + df_total_gols['Total_Games_Away']
            # Calcular o total de BTTS (em casa e fora)
            df_total_gols[f'{variable}_Total'] = df_total_gols[f'{variable}_Home'] + df_total_gols[f'{variable}_Away']
            # Calcular a porcentagem de BTTS no total de jogos
            df_total_gols[f'{variable}_Percent_Total'] = (df_total_gols[f'{variable}_Total'] / df_total_gols['Total_Games']) * 100
            top_total_gols = df_total_gols.sort_values(by=f'{variable}_Percent_Total', ascending=False)
            df_final_boths_gols = top_total_gols.rename(columns={
                'Total_Games': 'Jogos totais',
                f'{variable}_Total': f'Jogos {new_opcao_gols}',
                f'{variable}_Percent_Total': f'% {new_opcao_gols}',
            })

            tab1, tab2, tab3 = st.tabs([f"Em casa", f"Fora de casa", f"Geral"]) 
            with tab1:
                st.dataframe(df_final_home_gols[['Jogos totais', f'Jogos {new_opcao_gols}', f'% {new_opcao_gols}', 'Gols Pró', 'Gols Sofr.']],
                        column_config={
                            f"% {new_opcao_gols}": st.column_config.ProgressColumn(
                                f"% {new_opcao_gols}", format="%d", min_value=0, max_value=100
                            ),
                        })
            with tab2:
                st.dataframe(df_final_away_gols[['Jogos totais', f'Jogos {new_opcao_gols}', f'% {new_opcao_gols}', 'Gols Pró', 'Gols Sofr.']],
                        column_config={
                            f"% {new_opcao_gols}": st.column_config.ProgressColumn(
                                f"% {new_opcao_gols}", format="%d", min_value=0, max_value=100
                            ),
                        })
                
            with tab3:
                st.dataframe(df_final_boths_gols[['Jogos totais', f'Jogos {new_opcao_gols}', f'% {new_opcao_gols}']],
                            column_config={
                                f"% {new_opcao_gols}": st.column_config.ProgressColumn(
                                    f"% {new_opcao_gols}", format="%d", min_value=0, max_value=100
                                ),
                            })
        else:
            pass