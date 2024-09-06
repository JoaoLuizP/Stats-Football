import pandas as pd
import streamlit as st
import datetime
import matplotlib.pyplot as plt
import plotly.graph_objs as go
import numpy as np
from time import sleep


def new_columns(df) -> pd.DataFrame:
    # Adicionando colunas
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
    #df = df.sort_values(by=['Home', 'Date'])
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


    return df




def graphics(base, realidade, expecativa, acumulado, casa_fora):
    # Gráfico
    fig = go.Figure()

    # Linha de Realidade
    fig.add_trace(go.Scatter(x=base.index, y=base[realidade], mode='lines', name='Realidade', line=dict(color='blue', width=2), marker=dict(size=10)))

    # Linha de Expectativa
    fig.add_trace(go.Scatter(x=base.index, y=base[expecativa], mode='lines', name='Expectativa', line=dict(color='orange', width=2), marker=dict(size=10)))

    # Preenchimento de lucro acumulado (área)
    cumsum_values = base[acumulado].cumsum()
    fig.add_trace(go.Scatter(
        x=base.index,
        y=cumsum_values,
        mode='lines+markers',
        name='Lucro Acumulado',
        line=dict(color='black', width=2),
        fill='tonexty',  # Preenchimento da área
        fillcolor='rgba(255, 0, 0, 0.2)' if (cumsum_values.iloc[-1] < 0) else 'rgba(0, 255, 0, 0.2)',
        marker=dict(symbol='triangle-up')
    ))

    # Adicionar anotação com o último valor de lucro acumulado
    ultimo_valor = cumsum_values.iloc[-1]
    fig.add_annotation(
        x=base.index[-1],
        y=ultimo_valor,
        text=f'{ultimo_valor:.2f} stakes',
        showarrow=True,
        arrowhead=2,
        ax=0,
        ay=-40,
        font=dict(color='green' if ultimo_valor >= 0 else 'red', size=18, weight="bold", family="cursive")
    )

    if casa_fora == 'Home':
        texto = 'em casa'
    else:
        texto = 'fora de casa'

    # Ajustes de layout
    fig.update_layout(
        title=f'Expectativa de pontos X Realidade - {base[casa_fora].unique()[0]} {texto}',
        xaxis_title=f'Número de Jogos {texto}: {len(base)}',
        yaxis_title='Pontos',
        plot_bgcolor='white',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        font=dict(size=12),
        xaxis=dict(showgrid=False, showticklabels=False),
        yaxis=dict(showgrid=True, gridwidth=1, gridcolor='LightGray'),
        
        #height=700,  # Ajuste a altura do gráfico
        #width=1150    # Ajuste a largura do gráfico
        #yaxis=dict()
    )



    return fig




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

#df 


temporada_selecionada = st.session_state["temporada_selecionada"]
st.sidebar.text(f"Temporada selecionada: {temporada_selecionada}")


# Ligas
league = sorted(df["League"].unique())
leagues = st.selectbox("League", league, index=None, placeholder="Choose League") # Dropdown 
df_filtered = df[df["League"] == leagues]
df_filtered = new_columns(df=df_filtered)

# Times
time_liga = sorted(df_filtered["Home"].unique())
time_a = st.selectbox("Team", time_liga, index=None, placeholder="Choose Team")

if time_a != None:


    df_time_home = df_filtered[df_filtered["Home"] == time_a]
    df_time_away = df_filtered[df_filtered["Away"] == time_a]

    #df_time_home_new_columns = new_columns(df=df_time_home)

    tab1, tab2 = st.tabs(["Em casa", "Fora de casa"]) 

    with tab1:
        #df_time_home
        grafico_home = graphics(base=df_time_home, realidade="mptH6p", expecativa="mxptH6p", acumulado="plH", casa_fora="Home")

        ## Calculos uteis
        odd_media_home = df_time_home['Odd_H_FT'].mean()
        winrate_home = round((df_time_home['Winrate_H'].sum() / len(df_time_home)) * 100, 2)


        col11, col21, col31, col41 = st.columns([0.5, 1, 1, 1])
        col21.metric(f"**Jogos**", len(df_time_home))
        col31.metric(f"**ODD média**", round(odd_media_home, 2))
        col41.metric(f"**Winrate**", f'{winrate_home} %')

        col111, col211, col311 = st.columns([1, 0.2, 0.2])
        col111.plotly_chart(grafico_home)
    


    with tab2:
        grafico_away = graphics(base=df_time_away, realidade="mptA6p", expecativa="mxptA6p", acumulado="plA", casa_fora="Away")

        ## Calculos uteis
        odd_media_away = df_time_away['Odd_A_FT'].mean()
        winrate_away = round((df_time_away['Winrate_A'].sum() / len(df_time_away)) * 100, 2)

        col11, col21, col31, col41 = st.columns([0.5, 1, 1, 1])
        col21.metric(f"**Jogos**", len(df_time_away))
        col31.metric(f"**ODD média**", round(odd_media_away, 2))
        col41.metric(f"**Winrate**", f'{winrate_away} %')

        col111, col211, col311 = st.columns([1, 0.2, 0.2])
        col111.plotly_chart(grafico_away)




else:
    st.toast('Select a team.', icon=":material/report:")
    sleep(5)
    st.toast('Select a team.', icon=":material/report:")