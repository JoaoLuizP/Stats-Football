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


col1, col2, col3 = st.columns([1, 1, 0.15])
with col1:
    st.markdown(f"#### Estatistica de cantos ⛳ ")
#with col3:
#    btn = st.link_button("Chutes", "https://footyanalyzer.streamlit.app/Chutes")
    #if st.button("Chutes"):
    #    st.switch_page("D:\\João\\Python projects\\futebol\\st_fut\\pages\\4_⚽︎_Chutes.py")

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
            col0, col1, col2, col3, col4 = st.columns([0.15, 0.4, 0.4, 0.4, 1.5])
            col0.text('Em casa: ')
            col1.metric(f"Média de cantos feitos", round(((df_filtered2['Corners_H_FT'].sum())/len(df_filtered2)),2))
            col2.metric(f"Média de cantos sofridos", round(((df_filtered2['Corners_A_FT'].sum())/len(df_filtered2)),2))
            col3.metric(f"Média de cantos geral", round(((df_filtered2['TotalCorners_FT'].sum())/len(df_filtered2)),2))
            col4.area_chart(df_filtered2, x='Away', y='Corners_H_FT', x_label="Adversario", y_label="Corners Feitos")


            #df_filtered2


        with tab2:
            st.write('')
            st.write('')
            st.write('')
            col0, col1, col2, col3, col4 = st.columns([0.15, 0.4, 0.4, 0.4, 1.5])
            col0.text('Fora de casa: ')
            #col2.metric(f"Total de Gols Marcados no 1º Tempo - {time_a}", df_filtered2['Goals_H_HT'].sum())
            #col3.metric(f"Total de Gols Sofridos no 1º Tempo - {time_a}", df_filtered2['Goals_A_HT'].sum())
            col1.metric(f"Média de cantos feitos", round(((df_filtered3['Corners_A_FT'].sum())/len(df_filtered3)),2))
            col2.metric(f"Média de cantos sofridos", round(((df_filtered3['Corners_H_FT'].sum())/len(df_filtered3)),2))
            col3.metric(f"Média de cantos geral", round(((df_filtered3['TotalCorners_FT'].sum())/len(df_filtered3)),2))
            col4.area_chart(df_filtered3, x='Home', y='Corners_A_FT', x_label="Adversario", y_label="Corners Feitos")

        
    else:
        st.divider()
        with st.expander(" OBS", icon="⚠️"):
            st.write('''
                Selecione os times desejados na aba 'Home' e volte para essa aba ou outra (Gols;Chutes) para mostrar suas estatisticas na temporada e campeonato atual.
            ''')