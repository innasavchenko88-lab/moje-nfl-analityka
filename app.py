import os
import subprocess
import sys

# Funkcja wymuszająca instalację bibliotek, jeśli ich brakuje
def install_packages():
    try:
        import nfl_data_py
        import plotly
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "nfl_data_py", "plotly", "pandas"])

# Uruchom instalację przed importami
install_packages()

# Teraz standardowe importy
import streamlit as st
import nfl_data_py as nfl
import pandas as pd
import plotly.express as px

st.title("🏈 NFL Analytics Pro")

# Pobieranie danych (tylko 1 sezon na testy)
@st.cache_data
def load_data():
    seasons = [2024]
    with st.spinner("Pobieranie danych z serwerów NFL... Proszę czekać."):
        pbp = nfl.import_pbp_data(seasons)
    return pbp

try:
    data = load_data()
    st.success("Dane załadowane pomyślnie!")
    st.write(f"Liczba przeanalizowanych akcji: {len(data)}")
    
    # Prosty wykres na start
    offense = data.groupby('posteam')['epa'].mean().reset_index()
    fig = px.bar(offense, x='posteam', y='epa', title="Efektywność Ataku (EPA) 2024")
    st.plotly_chart(fig)

except Exception as e:
    st.error(f"Wystąpił problem z danymi: {e}")
