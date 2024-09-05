import streamlit as st


# --- PAGE SETUP ---


home_page = st.Page(
    page="Home.py",
    title="Selecionar confronto",
    icon=":material/bar_chart:"
)

gols_page = st.Page(
    page="funcionalidades/2_Gols.py",
    title="Gols",
    icon=":material/sports_soccer:"
)

cantos_page = st.Page(
    page="funcionalidades/3_Cantos.py",
    title="Cantos",
    icon=":material/golf_course:"
)

chutes_page = st.Page(
    page="funcionalidades/4_Chutes.py",
    title="Chutes",
    icon=":material/footprint:"
)


#### ============== ###

top_ligas_page = st.Page(
    page="funcionalidades/5_Tops ligas.py",
    title="Tops ligas",
    icon=":material/edit:"
)

top_teams_page = st.Page(
    page="funcionalidades/6_Tops teams.py",
    title="Tops teams",
    icon=":material/edit:"
)

ranking_por_liga_page = st.Page(
    page="funcionalidades/7_Ranking por liga.py",
    title="Ranking por liga",
    icon=":material/edit:"
)

jogos_do_dia_page = st.Page(
    page="funcionalidades/8_Jogos do dia.py",
    title="Jogos do dia",
    icon=":material/edit:"
)


# ---- NAVIGATION SETUP ----
pg = st.navigation(
    {
        "Home": [home_page, gols_page, cantos_page, chutes_page],
        "Análise": [top_ligas_page, top_teams_page, ranking_por_liga_page, jogos_do_dia_page],
        "Resumo": []
    }
)

# --- SHARED ON ALL PAGES ---
st.set_page_config(layout="wide", initial_sidebar_state="expanded") # Setar a pagina
st.html('style.html')


st.sidebar.markdown(
    """
    <div style="position: fixed; bottom: 0; width: 100%; text-align: left;">
        Made with by <a href="https://joaoluizp.github.io/portfolio_jluizp/" target="_blank" style="color: #3399ff; text-decoration: none;">João Luiz Pinheiro</a>
    </div>
    """, 
    unsafe_allow_html=True
)

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            .css-1rs6os {visibility: hidden;}
            .css-17ziqus {visibility: hidden;}
            """
            
st.markdown(hide_st_style,unsafe_allow_html=True)


pg.run()

