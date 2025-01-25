import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Title and intro
st.title("Dashboard Penyewaan Sepeda")
st.markdown("""
Dashboard interaktif untuk menganalisis pengaruh cuaca dan musim terhadap penyewaan sepeda.
""")

# Load dataset
df = pd.read_csv("day.csv")

# Sidebar Filter
st.sidebar.header("Filter Data")
selected_weather = st.sidebar.selectbox(
    "Pilih Kondisi Cuaca:", ["Semua", "Cerah", "Mendung", "Buruk"]
)
selected_season = st.sidebar.selectbox(
    "Pilih Musim:", ["Semua", "Spring", "Summer", "Fall", "Winter"]
)

# Filter data berdasarkan input
filtered_df = df.copy()

if selected_weather != "Semua":
    weather_map = {"Cerah": 1, "Mendung": 2, "Buruk": 3}
    filtered_df = filtered_df[filtered_df["weathersit"] == weather_map[selected_weather]]

if selected_season != "Semua":
    season_map = {"Spring": 1, "Summer": 2, "Fall": 3, "Winter": 4}
    filtered_df = filtered_df[filtered_df["season"] == season_map[selected_season]]

# Grafik Cuaca
if st.checkbox("Tampilkan Pengaruh Cuaca terhadap Penyewaan Sepeda"):
    weather_effect = filtered_df.groupby("weathersit")["cnt"].mean()
    
    # Mapping for weather labels and colors
    weather_mapping = {
        1: ("Cerah", "yellow"),
        2: ("Mendung", "orange"),
        3: ("Buruk", "chocolate"),
    }
    
    # Filter the mapping based on data in `weather_effect`
    available_weather = weather_effect.index.tolist()
    weather_labels = [weather_mapping[weather][0] for weather in available_weather]
    weather_colors = [weather_mapping[weather][1] for weather in available_weather]
    
    # Plotting
    fig1, ax1 = plt.subplots()
    weather_effect.plot(kind="bar", color=weather_colors, ax=ax1)
    ax1.set_title("Pengaruh Cuaca terhadap Penyewaan Sepeda")
    ax1.set_xlabel("Kondisi Cuaca")
    ax1.set_ylabel("Rata-rata Penyewaan")
    ax1.set_xticks(range(len(weather_effect)))
    ax1.set_xticklabels(weather_labels, rotation=0)
    st.pyplot(fig1)

# Grafik Musim
if st.checkbox("Tampilkan Rata-rata Penyewaan Sepeda per Musim"):
    season_effect = filtered_df.groupby("season")["cnt"].mean()
    
    # Mapping for season colors and labels
    season_mapping = {
        1: ("Spring", "green"),
        2: ("Summer", "yellow"),
        3: ("Fall", "orange"),
        4: ("Winter", "blue"),
    }
    
    # Filter the mapping based on data in `season_effect`
    available_seasons = season_effect.index.tolist()
    season_labels = [season_mapping[season][0] for season in available_seasons]
    season_colors = [season_mapping[season][1] for season in available_seasons]
    
    # Plotting
    fig2, ax2 = plt.subplots()
    season_effect.plot(kind="bar", color=season_colors, ax=ax2)
    ax2.set_title("Rata-rata Penyewaan Sepeda per Musim")
    ax2.set_xlabel("Musim")
    ax2.set_ylabel("Rata-rata Penyewaan")
    ax2.set_xticks(range(len(season_effect)))
    ax2.set_xticklabels(season_labels, rotation=0)
    st.pyplot(fig2)
