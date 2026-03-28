import nfl_data_py as nfl
import pandas as pd
import plotly.express as px
import streamlit as st

# Konfiguracja strony
st.set_page_config(page_title="NFL Analytics Pro", layout="wide")

@st.cache_data
def load_data():
    seasons = [2023, 2024, 2025]
    pbp = nfl.import_pbp_data(seasons)
    # Obliczanie podstawowych metryk
    weekly = pbp.groupby(['season', 'week', 'posteam'])['epa'].mean().reset_index()
    weekly.columns = ['Season', 'Week', 'Team', 'EPA']
    return pbp, weekly

pbp, weekly_data = load_data()

# --- MENU BOCZNE ---
st.sidebar.title("NFL Analytics Engine")
mode = st.sidebar.radio("Wybierz tryb:", ["Global Dashboard", "Porównanie Head-to-Head"])

# --- WARIANT 1: GLOBAL DASHBOARD (WIZUALIZACJA CAŁEJ LIGI) ---
if mode == "Global Dashboard":
    st.header("Ranking Efektywności Ligi (EPA/Play)")
    
    # Obliczanie Ataku i Obrony
    off = pbp.groupby('posteam')['epa'].mean().reset_index()
    dfn = pbp.groupby('defteam')['epa'].mean().reset_index()
    combined = pd.merge(off, dfn, left_on='posteam', right_on='defteam')
    combined.columns = ['Team', 'Off_EPA', 'Def_Team', 'Def_EPA']
    
    fig_quad = px.scatter(combined, x="Off_EPA", y="Def_EPA", text="Team", 
                          title="Gdzie znajduje się Twoja drużyna?", height=600)
    fig_quad.update_yaxes(autorange="reversed") # Niskie EPA obrony = Lepiej
    fig_quad.add_hline(y=combined['Def_EPA'].mean(), line_dash="dot")
    fig_quad.add_vline(x=combined['Off_EPA'].mean(), line_dash="dot")
    st.plotly_chart(fig_quad, use_container_width=True)

# --- WARIANT 2: HEAD-TO-HEAD (BEZPOŚREDNIE STARCIE) ---
else:
    st.header("Analiza Przedmeczowa: Head-to-Head")
    
    col1, col2 = st.columns(2)
    with col1:
        team_a = st.selectbox("Wybierz Drużynę 1 (Gospodarz):", sorted(weekly_data['Team'].unique()))
    with col2:
        team_b = st.selectbox("Wybierz Drużynę 2 (Gość):", sorted(weekly_data['Team'].unique()))
    
    # Wykres Trendów dla obu drużyn
    h2h_data = weekly_data[weekly_data['Team'].isin([team_a, team_b])].copy()
    h2h_data['Rolling_EPA'] = h2h_data.groupby('Team')['EPA'].transform(lambda x: x.rolling(3).mean())
    
    fig_h2h = px.line(h2h_data, x="Week", y="Rolling_EPA", color="Team", 
                      title=f"Trend Formy: {team_a} vs {team_b} (Ostatnie 3 mecze)",
                      markers=True)
    st.plotly_chart(fig_h2h, use_container_width=True)
    
    # Porównanie statystyczne w tabeli
    st.subheader("Kluczowe metryki starcia")
    stats_a = combined[combined['Team'] == team_a] if 'combined' in locals() else off[off['posteam'] == team_a]
    # (Tutaj możesz dodać więcej metryk jak Red Zone Eff, 3rd Down Conv)
    st.write(f"Analiza sugeruje: Jeśli trend {team_a} rośnie, a {team_b} spada – szukaj zakładu na gospodarzy.")


