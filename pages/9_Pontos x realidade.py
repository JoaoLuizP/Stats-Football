import pandas as pd
import streamlit as st
from connection import next_games
from connection import base
import datetime
import matplotlib.pyplot as plt
import seaborn as sns  
import numpy as np
from time import sleep

st.sidebar.markdown(
    """
    <div style="position: fixed; bottom: 0; width: 100%; text-align: left;">
        Desenvolvido por <a href="https://joaoluizp.github.io/portfolio_jluizp/" target="_blank" style="color: #3399ff; text-decoration: none;">João Luiz Pinheiro</a>
    </div>
    """, 
    unsafe_allow_html=True
)
st.html('style.html')


df_data = st.session_state["df_fut"]



temporada_selecionada = st.session_state["temporada_selecionada"]
st.sidebar.text(f"Temporada selecionada: {temporada_selecionada}")


# Ligas
league = sorted(df_data["League"].unique())
leagues = st.selectbox("League", league, index=None, placeholder="Choose League") # Dropdown 
df_filtered = df_data[df_data["League"] == leagues]

# Times
time_liga = sorted(df_filtered["Home"].unique())
time_a = st.selectbox("Team", time_liga, index=None, placeholder="Choose Team")

if time_a != None:

    df_time_home = df_data[df_data["Home"] == time_a]

    df_time_away = df_data[df_data["Away"] == time_a]

else:
    st.toast('Select a team.', icon=":material/report:")
    sleep(5)
    st.toast('Select a team.', icon=":material/report:")