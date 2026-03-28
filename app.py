import streamlit as st
import nfl_data_py as nfl
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="NFL Analytics Lite", layout="wide")

st.title("🏈 NFL Analytics - Sezon 2024")

# Funkcja ładowania lżejszych danych (statystyki sezonowe zamiast play-by-play)
@st.cache_data
def load_seasonal_data():
    # Pobieramy gotowe statystyki graczy/drużyn - to zajmuje kilka sekund i mało RAM
    data = nfl.import_seasonal_data()
    return data

try:
    with st.spinner("Ładowanie statystyk..."):
        df = load_seasonal_data()
    
    # Filtrujemy tylko ostatni sezon
    df_2024 = df[df['season'] == 2024].copy()
    
    st.success("Statystyki załadowane!")

    # --- WIZUALIZACJA: TOP 10 QB wg TD ---
    st.subheader("Top 10 Quarterbacków (Podania TD)")
    top_qbs = df_2024.sort_values(by='passing_tds', ascending=False).head(10)
    
    fig = px.bar(top_qbs, x='player_name', y='passing_tds', 
                 color='passing_tds', title="Liderzy TD - Sezon 2024")
    st.plotly_chart(fig, use_container_width=True)

    # --- TABELA DANYCH ---
    st.subheader("Przeglądaj dane zawodników")
    st.dataframe(df_2024[['player_name', 'recent_team', 'passing_yards', 'passing_tds', 'rushing_yards']].head(50))

except Exception as e:
    st.error(f"Problem z serwerem danych: {e}")
    st.info("Spróbuj odświeżyć stronę za chwilę.")

