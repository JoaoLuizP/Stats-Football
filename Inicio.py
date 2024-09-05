import streamlit as st


# --- PAGE SETUP ---


home_page = st.Page(
    page="pages/Home.py",
    title="Selecionar confronto",
    icon=":material/bar_chart:"
)

gols_page = st.Page(
    page="pages/2_Gols.py",
    title="Gols",
    icon=":material/sports_soccer:"
)

cantos_page = st.Page(
    page="pages/3_Cantos.py",
    title="Cantos",
    icon=":material/golf_course:"
)

chutes_page = st.Page(
    page="pages/4_Chutes.py",
    title="Chutes",
    icon=":material/footprint:"
)


#### ============== ###

top_ligas_page = st.Page(
    page="pages/5_Tops ligas.py",
    title="Tops ligas",
    icon=":material/edit:"
)

top_teams_page = st.Page(
    page="pages/6_Tops teams.py",
    title="Tops teams",
    icon=":material/edit:"
)

ranking_por_liga_page = st.Page(
    page="pages/7_Ranking por liga.py",
    title="Ranking por liga",
    icon=":material/edit:"
)

jogos_do_dia_page = st.Page(
    page="pages/8_Jogos do dia.py",
    title="Jogos do dia",
    icon=":material/edit:"
)


# ---- NAVIGATION SETUP ----
pg = st.navigation(
    {
        "Home": [home_page, gols_page, cantos_page, chutes_page],
        "Análise": [top_ligas_page, top_teams_page, ranking_por_liga_page],
        "Jogos do dia": [jogos_do_dia_page]
  }
)

# --- SHARED ON ALL PAGES ---
#st.logo("assets/logo.png")

st.set_page_config(layout="wide", initial_sidebar_state="expanded") # Setar a pagina


st.sidebar.markdown(
    """
    <div style="position: fixed; bottom: 0; width: 100%; text-align: left;">
        Made with by <a href="https://joaoluizp.github.io/portfolio_jluizp/" target="_blank" style="color: #3399ff; text-decoration: none;">João Luiz Pinheiro</a>
    </div>
    """, 
    unsafe_allow_html=True
)

pg.run()

