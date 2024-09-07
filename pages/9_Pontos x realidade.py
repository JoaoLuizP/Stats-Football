import pandas as pd
import streamlit as st
import datetime
import matplotlib.pyplot as plt
import plotly.graph_objs as go
import numpy as np
from time import sleep
import plotly.express as px


@st.cache_data
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

    ## Média de periodos específicos para cálculo das diferenças
    df['diff_H'] = df['mptH6p'] - df['mxptH6p']
    df['diff_A'] = df['mptA6p'] - df['mxptA6p']

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



def apostar_ou_nao(df_time, diff, odd_ft):

    # Filtrar os últimos 5 jogos em casa ou fora de casa
    ultimos_5_jogos = df_time.tail(5)

    # Calcular a média das diferenças entre a expectativa e a realidade
    media_diff = ultimos_5_jogos[diff].mean()

    # Verificar se a média das diferenças é maior que 0.5
    if media_diff > 0.5:
        # Média acima de 0.5, recomendar aposta
        odd_media = ultimos_5_jogos[odd_ft].mean()
        # Definir o intervalo de odds
        intervalo_inf = round(odd_media - 0.15, 2)
        intervalo_sup = round(odd_media + 0.15, 2)
        return f"Recomenda-se apostar na equipe com odd entre [{intervalo_inf} - {intervalo_sup}]."
    else:
        # Média abaixo de 0.5, não recomendar aposta
        return "Não se recomenda apostar nessa equipe no momento."


def verificar_lucratividade(df_time, diff, odd_ft, gols_home, gols_away, casa_fora):
    # Pegar os últimos 5 jogos em casa
    df_ultimos_jogos = df_time.tail(5)

    # Calcular a diferença entre expectativa e realidade nos últimos 5 jogos
    #df_ultimos_jogos['dif_realidade_expectativa'] = df_ultimos_jogos['ptH'] - df_ultimos_jogos['xptH']

    # Calcular a média da diferença
    media_diferenca = df_ultimos_jogos[diff].mean()

    # Calcular a odd média dos últimos 5 jogos
    odd_media = df_ultimos_jogos[odd_ft].mean()

    # Definir o intervalo de odds
    intervalo_inf = odd_media - 0.2
    intervalo_sup = odd_media + 0.2

    if media_diferenca > 0.5:
        # Calcular o lucro acumulado simulando apostas nos últimos 5 jogos
        if casa_fora == "Home":
            df_ultimos_jogos['lucro_simulado'] = df_ultimos_jogos.apply(lambda row: (row[odd_ft] - 1) if row[gols_home] > row[gols_away] else -1, axis=1)
        else:
             df_ultimos_jogos['lucro_simulado'] = df_ultimos_jogos.apply(lambda row: (row[odd_ft] - 1) if row[gols_home] < row[gols_away] else -1, axis=1)
        lucro_acumulado = df_ultimos_jogos['lucro_simulado'].sum()

        return f"A média da diferença entre a linha Expectativa x Realidade dos ultimos 5 jogos é {media_diferenca:.2f}, que é maior que 0.5. \
            [[ Lucro acumulado simulando apostas nos últimos 5 jogos: {lucro_acumulado:.2f} unidades ]]"
        #st.write(f"Sugerido apostar entre a odd de {intervalo_inf:.2f} e {intervalo_sup:.2f}.")
       
    else:
        return f"A média da diferença é {media_diferenca:.2f}, que é menor ou igual a 0.5. Não é sugerido apostar."



def filtrar_jogos_estrategia(df, differ, casa_fora, n=5):
    # Função para calcular a diferença e filtrar com base nos últimos 5 jogos
    def filtrar_por_time(grupo):
        # Ordena os jogos pela data
        grupo['Date'] = pd.to_datetime(grupo['Date'], errors='coerce')
        grupo = grupo.sort_values(by='Date', ascending=False).head(n)
        #grupo
        # Calcula a média da diferença (expectativa vs realidade)
        media_diferenca = grupo[differ].mean()
        # Se a média for maior que 0.5, incluímos o time na estratégia
        if media_diferenca > 0.5:
            return grupo
        else:
            return pd.DataFrame()  # Retorna um DataFrame vazio se não passar na estratégia
    
    # Aplica a função de filtragem para cada time
    df_filtrado = df.groupby(casa_fora).apply(filtrar_por_time).reset_index(drop=True)
    return df_filtrado


def calcular_metricas_por_time_estrategia(df, casa_fora):
    # Agrupa por time e calcula as métricas
    if casa_fora == "Home":
        df_grouped = df.groupby('Home').apply(lambda x: pd.Series({
            'lucro_acumulado': x.apply(lambda row: (row['Odd_H_FT'] - 1) if row['Goals_H_FT'] > row['Goals_A_FT'] else -1, axis=1).sum(),
            'odd_media': x['Odd_H_FT'].mean(),
            'win_rate': (x['Goals_H_FT'] > x['Goals_A_FT']).mean() * 100,
            'total_jogos': len(x)
        })).reset_index()
    else:
        df_grouped = df.groupby('Away').apply(lambda x: pd.Series({
        'lucro_acumulado': x.apply(lambda row: (row['Odd_A_FT'] - 1) if row['Goals_H_FT'] < row['Goals_A_FT'] else -1, axis=1).sum(),
        'odd_media': x['Odd_A_FT'].mean(),
        'win_rate': (x['Goals_H_FT'] < x['Goals_A_FT']).mean() * 100,
        'total_jogos': len(x)
    })).reset_index()
    
    return df_grouped


def calcular_lucro(row):
    if row['Goals_H_FT'] > row['Goals_A_FT']:  # Time da casa venceu
        return row['Odd_H_FT'] - 1
    else:  # Time da casa perdeu ou empatou
        return -1

def calcular_lucro_away(row):
    if row['Goals_H_FT'] < row['Goals_A_FT']:  # Time de fora venceu
        return row['Odd_A_FT'] - 1
    else:  # Time de fora perdeu ou empatou
        return -1       
    

def plot_evolucao_lucro(df, times_selecionados, casa_fora):
    # Filtrar o DataFrame com base nos times selecionados
    df_filtrado = df[df[casa_fora].isin(times_selecionados)]
    
    df_filtrado['Date'] = pd.to_datetime(df_filtrado['Date'], errors='coerce')
    df_filtrado = df_filtrado.sort_values(by=['Date', 'Rodada'], ascending=True)
    #df_filtrado

    # Criar gráfico de linhas para cada time selecionado
    fig = go.Figure()
    for time in times_selecionados:
        df_time = df_filtrado[df_filtrado[casa_fora] == time]
        df_time['lucro_acumulado_time_indiv'] = df_time['lucro_jogo'].cumsum()
        #df_time
        fig.add_trace(go.Scatter(
            x=df_time['Date'],
            y=df_time['lucro_acumulado_time_indiv'],
            mode='lines+markers',
            name=time,
            line=dict(width=2),
            marker=dict(size=6)
        ))
    
    # Calcular lucro acumulado total (de todos os times)
    df_filtrado['lucro_acumulado_total'] = df_filtrado['lucro_jogo'].cumsum()
    
    # Adicionar linha de lucro acumulado global
    fig.add_trace(go.Scatter(
        x=df_filtrado['Date'],
        y=df_filtrado['lucro_acumulado_total'],
        mode='lines+markers',
        name='Lucro Acumulado Total',
        line=dict(color='black', width=3, dash='dash'),
        marker=dict(size=8, symbol='circle')
    ))

    # Mostrar o último valor de lucro acumulado total no gráfico
    ultimo_lucro = df_filtrado['lucro_acumulado_total'].iloc[-1]
    ultima_data = df_filtrado['Date'].iloc[-1]

    fig.add_trace(go.Scatter(
        x=[ultima_data],
        y=[ultimo_lucro],
        mode='markers+text',
        name='Último Lucro Acumulado',
        marker=dict(color='black', size=10, symbol='x'),
        text=[f"{ultimo_lucro:.2f} U"],
        textposition="top center"
    ))
    
    # Ajustar o layout
    fig.update_layout(
        title="Evolução do Lucro Acumulado por Time",
        xaxis_title="Date",
        yaxis_title="Lucro Acumulado",
        legend_title="Times",
        hovermode="x unified"
    )


    return fig


# Função para calcular as métricas baseadas nos times filtrados
def calcular_metricas_filtradas(df, times_selecionados, casa_fora):
    df_filtrado = df[df[casa_fora].isin(times_selecionados)]

    df_filtrado['Date'] = pd.to_datetime(df_filtrado['Date'], errors='coerce')
    df_filtrado = df_filtrado.sort_values(by=['Date', 'Rodada'], ascending=True)#.head(n)

    #df_filtrado

    lucro_final = df_filtrado['lucro_jogo'].sum()  # Lucro acumulado
    odd_media = df_filtrado['Odd_H_FT'].mean()
    win_rate = df_filtrado['Winrate_H'].mean() * 100

    # Ultimos 5 jogos
    return lucro_final, odd_media, win_rate





@st.cache_data
def gerar_relatorio_todas_as_ligas(base, lista_ligas):

    ## Iterar casa ##
    resultado_casa = []
    for league in lista_ligas:

        df_filtered = base[base["League"] == league]
        df_filtered = new_columns(df=df_filtered)

        home_win_count = df_filtered['Resultado_H'].value_counts().get('W', 0)
        total_games = len(df_filtered)
        home_win_percentage = round((home_win_count / total_games) * 100,2)

        ## Filtra os times em casa que estão respeitando o critério
        df_filtrado_estrategia = filtrar_jogos_estrategia(df_filtered,differ="diff_H", casa_fora="Home")
        
        if df_filtrado_estrategia.empty:
            continue
        else:
            df_filtrado_estrategia['Date'] = pd.to_datetime(df_filtrado_estrategia['Date'], errors='coerce')
            df_filtrado_estrategia = df_filtrado_estrategia.sort_values(by=['Date', 'Rodada'], ascending=True)
            # Calcular o lucro por jogo e acumular
            df_filtrado_estrategia['lucro_jogo'] = df_filtrado_estrategia.apply(calcular_lucro, axis=1)
            df_filtrado_estrategia['lucro_acumulado'] = df_filtrado_estrategia['lucro_jogo'].cumsum()  # Lucro acumulado


            # Calcular as métricas baseadas nos jogos filtrados
            df_metricas = calcular_metricas_por_time_estrategia(df_filtrado_estrategia,casa_fora="Home")

            times_disponiveis = df_metricas['Home'].unique()

            # Calcular e exibir as métricas atualizadas
            lucro_final, odd_media, win_rate = calcular_metricas_filtradas(df_filtrado_estrategia, times_disponiveis, casa_fora="Home")

            # Adicionar os resultados ao DataFrame de resultados
            resultado_casa.append([
                league,
                len(df_filtrado_estrategia),
                f"{home_win_percentage:.2f}%",
                ', '.join(times_disponiveis),  # Junta os nomes dos times em uma string
                f"{lucro_final:.2f}".replace('.', ','),
                f"{odd_media:.2f}".replace('.', ','),
                f"{win_rate:.2f}%",
                'Home'
            ])
    
    # Criar o DataFrame do relatório
    df_relatorio = pd.DataFrame(resultado_casa, columns=['Liga', 'Total Games', 'Home Win League %', 'Times', 'Lucro Final', 'Odd Média', 'Winrate', 'Casa/Fora'])
    return '\ufeff' + df_relatorio.to_csv(index=False, sep=';')




st.sidebar.markdown(
    """
    <div style="position: fixed; bottom: 0; width: 100%; text-align: left;">
        Desenvolvido por <a href="https://joaoluizp.github.io/portfolio_jluizp/" target="_blank" style="color: #3399ff; text-decoration: none;">João Luiz Pinheiro</a>
    </div>
    """, 
    unsafe_allow_html=True
)
st.html('style.html')


if 'df_fut' not in st.session_state:
    st.toast('Return to the "Selecionar-Confronto" tab to update the database and return to this page again.', icon=":material/report:")
    
    pass

else:
    df = st.session_state["df_fut"]

    #df 


    temporada_selecionada = st.session_state["temporada_selecionada"]
    st.sidebar.text(f"Temporada selecionada: {temporada_selecionada}")


    # Ligas
    league = sorted(df["League"].unique())
    #relatorio = gerar_relatorio_todas_as_ligas(base=df, lista_ligas=league)

    st.sidebar.download_button(
        label="Download data as CSV",
        data=gerar_relatorio_todas_as_ligas(base=df, lista_ligas=league).encode('utf-8'),
        file_name="estrategia_por_liga.csv",
        mime="text/csv",
    )

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

        st.write('')
        tab1, tab2 = st.tabs(["Em casa", "Fora de casa"]) 

        with tab1:
            #df_time_home
            home_win_count = df_filtered['Resultado_H'].value_counts().get('W', 0)
            total_games = len(df_filtered)
            home_win_percentage = round((home_win_count / total_games) * 100,2)
            
            grafico_home = graphics(base=df_time_home, realidade="mptH6p", expecativa="mxptH6p", acumulado="plH", casa_fora="Home")
            recomendacao = apostar_ou_nao(df_time=df_time_home, diff="diff_H", odd_ft="Odd_H_FT")
            verifica_lucratividade = verificar_lucratividade(df_time=df_time_home, diff="diff_H", odd_ft="Odd_H_FT", gols_home="Goals_H_FT", gols_away="Goals_A_FT", casa_fora="Home")

            ## Calculos uteis
            odd_media_home = df_time_home['Odd_H_FT'].mean()
            winrate_home = round((df_time_home['Winrate_H'].sum() / len(df_time_home)) * 100, 2)


            col11, col21, col31, col41 = st.columns([0.5, 1, 1, 1])
            col21.metric(f"**Jogos**", len(df_time_home))
            col31.metric(f"**ODD média**", round(odd_media_home, 2))
            col41.metric(f"**Winrate**", f'{winrate_home} %')

            #col111, col211, col311 = st.columns([1, 0.2, 0.2])
            st.plotly_chart(grafico_home, use_container_width=True)


            col0, col0_1 = st.columns([0.4, 0.60])
            col0_1.subheader('Estratégia (Teste)', help="""Calcula a diferença entre a expectativa do mercado e a realidade do time para cada jogo. 
                         Se a diferença for maior que 0,5, recomenda-se apostar a favor do time no próximo jogo em casa""")
            st.write("")
            st.write("")
            col11, col21, col31, col41 = st.columns([0.5, 1, 1, 0.5])
            #col11.text("Estratégia: ")
            col21.text(recomendacao)
            col31.text(verifica_lucratividade)


            ## Filtra os times em casa que estão respeitando o critério
            df_filtrado_estrategia = filtrar_jogos_estrategia(df_filtered,differ="diff_H", casa_fora="Home")
            
            if df_filtrado_estrategia.empty:
                st.write("")
                st.warning("Nenhum time dessa liga em casa atende a essa estratégia", icon="⚠️")
            
            else:
                df_filtrado_estrategia['Date'] = pd.to_datetime(df_filtrado_estrategia['Date'], errors='coerce')
                df_filtrado_estrategia = df_filtrado_estrategia.sort_values(by=['Date', 'Rodada'], ascending=True)
                # Calcular o lucro por jogo e acumular
                df_filtrado_estrategia['lucro_jogo'] = df_filtrado_estrategia.apply(calcular_lucro, axis=1)
                df_filtrado_estrategia['lucro_acumulado'] = df_filtrado_estrategia['lucro_jogo'].cumsum()  # Lucro acumulado

                # Calcular as métricas baseadas nos jogos filtrados
                df_metricas = calcular_metricas_por_time_estrategia(df_filtrado_estrategia,casa_fora="Home")


                # Seletor de times para remover
                times_disponiveis = df_metricas['Home'].unique()
                # Seletor de times
                st.write("")
                st.write("")
                times_selecionados = st.multiselect(
                    "Selecione os times para atualizar os resultados e o gráfico (Times da liga que atendem ao critério)",
                    options=times_disponiveis,
                    default=times_disponiveis  # Todos os times selecionados inicialmente
                )

                # Plotar gráfico de evolução do lucro acumulado
                fig = plot_evolucao_lucro(df_filtrado_estrategia, times_selecionados, casa_fora="Home")

                #df_filtrado_estrategia

                #st.text(f'{len(df_filtrado_estrategia)}')          

                
                # Calcular e exibir as métricas atualizadas
                lucro_final, odd_media, win_rate = calcular_metricas_filtradas(df_filtrado_estrategia, times_selecionados, casa_fora="Home")

                col0, col0_1 = st.columns([0.35, 0.65])
                col0_1.subheader('Desempenho nos últimos 5 Jogos', help="Resultados da estratégia para times que atenderam ao critério nos últimos 5 jogos em casa")
                st.write("")
                st.write("")
                col01, col11, col21, col31, col41, col51 = st.columns([0.4, 1, 1, 1, 1, 0.05])
                #col11.write("Resultados: ")
                col11.metric("Lucro Final Acumulado:", f"{lucro_final:.2f} U")
                col21.metric("Odd Média Global:", f"{odd_media:.2f}")
                col31.metric("Taxa de Win-Rate Global:", f"{win_rate:.2f}%")
                col41.metric("Home Win League:", home_win_percentage)
                st.plotly_chart(fig)


        
    



        


        with tab2:
            away_win_count = df_filtered['Resultado_A'].value_counts().get('W', 0)
            total_games = len(df_filtered)
            away_win_percentage = round((away_win_count / total_games) * 100,2)


            grafico_away = graphics(base=df_time_away, realidade="mptA6p", expecativa="mxptA6p", acumulado="plA", casa_fora="Away")
            recomendacao = apostar_ou_nao(df_time=df_time_away, diff="diff_A", odd_ft="Odd_A_FT")
            verifica_lucratividade = verificar_lucratividade(df_time=df_time_away, diff="diff_A", odd_ft="Odd_A_FT", gols_home="Goals_H_FT", gols_away="Goals_A_FT", casa_fora="Away")

            ## Calculos uteis
            odd_media_away = df_time_away['Odd_A_FT'].mean()
            winrate_away = round((df_time_away['Winrate_A'].sum() / len(df_time_away)) * 100, 2)

            col11, col21, col31, col41 = st.columns([0.5, 1, 1, 1])
            col21.metric(f"**Jogos**", len(df_time_away))
            col31.metric(f"**ODD média**", round(odd_media_away, 2))
            col41.metric(f"**Winrate**", f'{winrate_away} %')

            #col111, col211, col311 = st.columns([1, 0.2, 0.2])
            st.plotly_chart(grafico_away, use_container_width=True)

            col0, col0_1 = st.columns([0.4, 0.60])
            col0_1.subheader('Estratégia (Teste)', help="""Calcula a diferença entre a expectativa do mercado e a realidade do time para cada jogo. 
                         Se a diferença for maior que 0,5, recomenda-se apostar a favor do time no próximo jogo em casa""")
            st.write("")
            st.write("")
            col11, col21, col31, col41 = st.columns([0.5, 1, 1, 0.5])
            #col11.text("Estratégia: ")
            col21.text(recomendacao)
            col31.text(verifica_lucratividade)

            ## Filtra os times em casa que estão respeitando o critério
            df_filtrado_estrategia = filtrar_jogos_estrategia(df_filtered, differ="diff_A", casa_fora="Away")

            if df_filtrado_estrategia.empty:
                st.write("")
                st.warning("Nenhum time dessa liga fora de casa atende a essa estratégia", icon="⚠️")
            
            else:

                df_filtrado_estrategia['Date'] = pd.to_datetime(df_filtrado_estrategia['Date'], errors='coerce')
                df_filtrado_estrategia = df_filtrado_estrategia.sort_values(by=['Date', 'Rodada'], ascending=True)
                # Calcular o lucro por jogo e acumular
                df_filtrado_estrategia['lucro_jogo'] = df_filtrado_estrategia.apply(calcular_lucro_away, axis=1)
                df_filtrado_estrategia['lucro_acumulado'] = df_filtrado_estrategia['lucro_jogo'].cumsum()  # Lucro acumulado

                # Calcular as métricas baseadas nos jogos filtrados
                df_metricas = calcular_metricas_por_time_estrategia(df_filtrado_estrategia,casa_fora="Away")
        
                
                #st.write("Métricas por Time (Filtradas pela Estratégia)")
                #st.dataframe(df_metricas)

                # Seletor de times para remover
                times_disponiveis = df_metricas['Away'].unique()

                #df_filtrado_estrategia

                # Seletor de times
                st.write("")
                st.write("")
                times_selecionados = st.multiselect(
                    "Selecione os times para atualizar os resultados e o gráfico (Times da liga que atendem ao critério)",
                    options=times_disponiveis,
                    default=times_disponiveis  # Todos os times selecionados inicialmente
                )

                # Plotar gráfico de evolução do lucro acumulado
                fig = plot_evolucao_lucro(df_filtrado_estrategia, times_selecionados, casa_fora="Away")

                
                # Calcular e exibir as métricas atualizadas
                lucro_final, odd_media, win_rate = calcular_metricas_filtradas(df_filtrado_estrategia, times_selecionados, casa_fora="Away")

                col0, col0_1 = st.columns([0.35, 0.65])
                col0_1.subheader('Desempenho nos últimos 5 Jogos', help="Resultados da estratégia para times que atenderam ao critério nos últimos 5 jogos fora de casa")
                st.write("")
                st.write("")
                col01, col11, col21, col31, col41, col51 = st.columns([0.4, 1, 1, 1, 1, 0.05])
                #col11.write("Resultados: ")
                col11.metric("Lucro Final Acumulado:", f"{lucro_final:.2f} U")
                col21.metric("Odd Média Global:", f"{odd_media:.2f}")
                col31.metric("Taxa de Win-Rate Global:", f"{win_rate:.2f}%")
                col41.metric("Away Win League:", away_win_percentage)

                st.plotly_chart(fig)




    else:
        st.toast('Select a team.', icon=":material/report:")
        sleep(5)
        st.toast('Select a team.', icon=":material/report:")