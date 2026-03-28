import streamlit as st
import pandas as pd

# Najpierw sprawdzamy, czy biblioteka w ogóle jest dostępna
try:
    import nfl_data_py as nfl
    import plotly.express as px
    library_status = True
except ImportError:
    library_status = False

st.title("🏈 NFL Analytics - Status Systemu")

if not library_status:
    st.error("Biblioteka 'nfl_data_py' nie została jeszcze zainstalowana. Proszę czekać na zakończenie 'Pieczenia ciasta' (Logs).")
else:
    st.success("Wszystkie biblioteki załadowane!")
    
    @st.cache_data
    def simple_load():
        # Pobieramy tylko mały zestaw danych na test (statystyki sezonowe)
        return nfl.import_seasonal_data()

    try:
        df = simple_load()
        st.write(f"Połączono z bazą NFL! Znaleziono {len(df)} rekordów.")
        
        # Szybki wykres liderów jardów
        top_yards = df[df['season'] == 2024].sort_values('passing_yards', ascending=False).head(10)
        fig = px.bar(top_yards, x='player_name', y='passing_yards', title="Liderzy Jardów 2024")
        st.plotly_chart(fig)
    except Exception as e:
        st.warning(f"Czekam na dane z serwera NFL... ({e})")
