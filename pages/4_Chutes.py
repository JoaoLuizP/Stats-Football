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



col1, col2, col3 = st.columns([1, 1, 0.12])
with col1:
    st.markdown(f"#### Estatistica de chutes ⚽︎ ")
#with col3:
#    btn = st.link_button("Home", "https://footyanalyzer.streamlit.app")
    #if st.button("Home"):
    #    st.switch_page("D:\\João\\Python projects\\futebol\\st_fut\\Home.py")


if 'df_2' not in st.session_state or 'df_3' not in st.session_state:
    pass
else:
    df_filtered2 = st.session_state["df_2"]
    df_filtered3 = st.session_state["df_3"]



    if st.session_state["time_a"] != None and st.session_state["time_b"] != None:

        st.write('')
        tab1, tab2 = st.tabs([f"{st.session_state["time_a"]}", f"{st.session_state["time_b"]}"]) 

        with tab1:
            st.write('')
            st.write('')
            st.write('')

            col0, col1, col2, col3, col4 = st.columns([0.5, 1, 1, 1, 0.05])
            col0.text('Em casa: ')
            df_plot = df_filtered2[['Shots_H', 'ShotsOnTarget_H', "Away"]]

            col1.metric(f"Média de chutes ao gol feitos", round(((df_filtered2['ShotsOnTarget_H'].sum())/len(df_filtered2)),2))
            col2.metric(f"Média de chutes ao gol sofridos", round(((df_filtered2['ShotsOnTarget_A'].sum())/len(df_filtered2)),2))
            col3.metric(f"Média de chutes feitos geral", round(((df_filtered2['Shots_H'].sum())/len(df_filtered2)),2))


            st.write('')
            st.write('')
            st.bar_chart(df_plot, x="Away", use_container_width=True)


        with tab2:
            col1, col2, col3, col3_1 = st.columns([0.6, 0.3, 0.3, 0.3])
            df_plot = df_filtered3[['Shots_A', 'ShotsOnTarget_A', "Home"]]
            # Criando o gráfico de barras com personalização
            col1.bar_chart(df_plot, x="Home")
            #col2.metric(f"Total de Gols Marcados no 1º Tempo - {time_a}", df_filtered2['Goals_H_HT'].sum())
            #col3.metric(f"Total de Gols Sofridos no 1º Tempo - {time_a}", df_filtered2['Goals_A_HT'].sum())
            col2.metric(f"Média de chutes ao gol feitos", round(((df_filtered3['ShotsOnTarget_A'].sum())/len(df_filtered3)),2))
            col3.metric(f"Média de chutes ao gol sofridos", round(((df_filtered3['ShotsOnTarget_H'].sum())/len(df_filtered3)),2))
            col3_1.metric(f"Média de chutes feitos geral", round(((df_filtered3['Shots_A'].sum())/len(df_filtered3)),2)) 

    else:
        st.divider()
        with st.expander(" OBS", icon="⚠️"):
            st.write('''
                Selecione os times desejados na aba 'Home' e volte para essa aba ou outra (Gols;Cantos) para mostrar suas estatisticas na temporada e campeonato atual.
            ''')
