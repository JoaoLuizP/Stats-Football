import pandas as pd
import streamlit as st
from collections import Counter
import plotly.graph_objects as go


def order_dict(data):
    """Ordena as chaves de um dicionário de intervalos.

    Args:
        data (dict): O dicionário contendo os intervalos e seus valores.

    Returns:
        list: Uma lista de tuplas ordenadas por intervalo.
    """
    # Filtra as chaves relevantes e converte para tuplas de inteiros
    intervals = [(int(k.split('-')[0]), int(k.split('-')[1]), v)
                 for k, v in data.items() if '-' in k]

    # Ordena pela primeira posição da tupla (início do intervalo)
    intervals.sort()
    
    # Transforma a lista em dict
    dicionario_new = {}
    for inicio, fim, valor in intervals:
        chave = f"{inicio}-{fim}"
        dicionario_new[chave] = valor

    return dicionario_new



def minutes_gols(dataframe):
    # Extraindo e convertendo os minutos (ignorando os acréscimos)
    lista_minutos = []
    for x in dataframe:
        if x == "[]":
            continue
        try:
            x = x.strip("[]").replace("'", "")
            values = x.split(", ")
            # Convertendo os valores para inteiros (opcional, dependendo do uso)
            lista_minutos.append([str(value) for value in values])  
        except:
            pass


    minutos_planos = []
    for sublist in lista_minutos:
        for m in sublist:
            if '+' in m:
                m = m.split('+')
                values_int = [int(value) for value in m] # Somar os valores dentro da lista
                total = sum(values_int)
                minutos_planos.append(int(total))
            elif m in ('[', ']', "'"):
                pass
            else:
                minutos_planos.append(int(m))

    # Definindo intervalos
    intervalos = [(0, 15), (16, 30), (31, 45), (46, 60), (61, 75), (76, 90), (91, 150)]
    intervalos_labels = ['0-15', '16-30', '31-45', '46-60', '61-75', '76-90', '91-150']
    intervalos_labels_2 = ['0-15', '16-30', '31-45', '46-60', '61-75', '76-90', '90+']

    # Contando gols em cada intervalo
    gols_por_intervalo = Counter()

    for minuto in minutos_planos:
        for start, end in intervalos:
            if start <= minuto <= end:
                gols_por_intervalo[f'{start}-{end}'] += 1
                break

    # Calculando a porcentagem de gols por intervalo
    total_gols = len(minutos_planos)
    percentuais = {k: (v / total_gols) * 100 for k, v in gols_por_intervalo.items()}
    percentuais_new = order_dict(data=percentuais)


    # Garantindo que todos os intervalos estejam representados, mesmo com 0 gols
    percentuais_completos = [percentuais_new.get(label, 0) for label in intervalos_labels]


    return intervalos_labels_2, percentuais_completos




st.set_page_config(layout="wide")
st.sidebar.markdown(
    """
    <div style="position: fixed; bottom: 0; width: 100%; text-align: left;">
        Desenvolvido por <a href="https://joaoluizp.github.io/portfolio_jluizp/" target="_blank" style="color: #3399ff; text-decoration: none;">João Luiz Pinheiro</a>
    </div>
    """, 
    unsafe_allow_html=True
)
col1, col2, col3 = st.columns([1, 1, 0.15])
with col1:
    st.markdown(f"#### Estatistica de gols 🥅 ")
with col3:
    btn = st.link_button("Cantos", "https://footyanalyzer.streamlit.app/Cantos")
    #if st.button("Cantos"):
        #st.switch_page("D:\\João\\Python projects\\futebol\\st_fut\\pages\\3_⛳_Cantos.py")

if 'df_2' not in st.session_state or 'df_3' not in st.session_state:
    pass
else:
    df_filtered2 = st.session_state["df_2"]
    df_filtered3 = st.session_state["df_3"]


    if st.session_state["time_a"] != None and st.session_state["time_b"] != None:

        st.empty()
        tab1, tab2 = st.tabs([f"{st.session_state["time_a"]}", f"{st.session_state["time_b"]}"]) 

        with tab1:
            ### Time HOME
            minutes_home = minutes_gols(dataframe=df_filtered2['Goals_H_Minutes'])
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
            col1, col2, col3, col3_1 = st.columns([0.4, 0.2, 0.1, 0.3])
            col1.bar_chart(df_filtered2, x='Away', y='Goals_H_HT')
            #col2.metric(f"Total de Gols Marcados no 1º Tempo - {time_a}", df_filtered2['Goals_H_HT'].sum())
            #col3.metric(f"Total de Gols Sofridos no 1º Tempo - {time_a}", df_filtered2['Goals_A_HT'].sum())
            col2.metric(f"Média de gols Marcados no 1º Tempo", round(((df_filtered2['Goals_H_HT'].sum())/len(df_filtered2)),2))
            col3.metric(f"% de Over 0.5HT", round(df_filtered2['Over05_HT'].mean() * 100, 2))
            col3_1.plotly_chart(fig, use_container_width=False)

            col5, col6, col7, col8, col9, col9_1 = st.columns([0.4, 0.25, 0.15, 0.15, 0.15, 0.15])
            col5.bar_chart(df_filtered2, x='Away', y='TotalGoals_FT')
            col6.metric(f"Média de gols Marcados", round(((df_filtered2['Goals_H_FT'].sum())/len(df_filtered2)),2))
            col7.metric(f"% de Over 1.5FT", round(df_filtered2['Over15_FT'].mean() * 100, 2))
            col8.metric(f"% de Over 2.5FT", round(df_filtered2['Over25_FT'].mean() * 100, 2))
            col9.metric(f"% de Over 3.5FT", round(df_filtered2['Over35_FT'].mean() * 100, 2))
            col9_1.metric(f"% do Ambas", round(df_filtered2['BTTS'].mean() * 100, 2))



        with tab2:
            ### Time AWAY
            minutes_away = minutes_gols(dataframe=df_filtered3['Goals_A_Minutes'])
            # Plotando o gráfico
            # Create the Plotly figure
            fig = go.Figure(
                data=[go.Bar(x=minutes_away[0], y=minutes_away[1])],
                layout=dict(
                    title='Percentual de Gols por Intervalo de Minutos',
                    xaxis_title='Intervalo de Minutos',
                    yaxis_title='Percentual de Gols (%)',
                    # Adjust layout options as needed
                )
            )

            col10, col11, col12, col12_1 = st.columns([0.4, 0.2, 0.1, 0.3])
            col10.bar_chart(df_filtered3, x='Home', y='Goals_A_HT')
            #col6.metric(f"Total de Gols Marcados no 1º Tempo - {time_b}", df_filtered3['Goals_A_HT'].sum())
            #col7.metric(f"Média de gols Marcados no 1º Tempo - {time_b}", ((df_filtered3['Goals_A_HT'].sum())/len(df_filtered3)).round(2))
            col11.metric(f"Média de gols Marcados no 1º Tempo", round(((df_filtered3['Goals_A_HT'].sum())/len(df_filtered3)),2))
            col12.metric(f"% de Over 0.5HT", round(df_filtered3['Over05_HT'].mean() * 100, 2))
            col12_1.plotly_chart(fig, use_container_width=False)


            col13, col14, col15, col16, col17, col17_1 = st.columns([0.4, 0.25, 0.15, 0.15, 0.15, 0.15])
            col13.bar_chart(df_filtered3, x='Home', y='TotalGoals_FT')
            col14.metric(f"Média de gols Marcados", round(((df_filtered3['Goals_A_FT'].sum())/len(df_filtered3   )),2))
            col15.metric(f"% de Over 1.5FT", round(df_filtered3['Over15_FT'].mean() * 100, 2))
            col16.metric(f"% de Over 2.5FT", round(df_filtered3['Over25_FT'].mean() * 100, 2))
            col17.metric(f"% de Over 3.5FT", round(df_filtered3['Over35_FT'].mean() * 100, 2))
            col17_1.metric(f"% do Ambas", round(df_filtered3['BTTS'].mean() * 100, 2))
            

