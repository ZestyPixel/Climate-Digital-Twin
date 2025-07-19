import streamlit as st
import pandas as pd
import plotly.express as px
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="Climate Digital Twin", layout="wide")

# Title
st.title("🌍 Climate Digital Twin: Haridwar to Bhagalpur")

# Sidebar slider
year = st.slider("Select Year", 2000, 2050, step=5)

# Load climate data
df = pd.read_csv("data/rainfall_temp.csv", encoding='utf-8-sig')
df.columns = df.columns.str.strip()  # removes hidden spaces/BOM
st.write("Columns:", df.columns.tolist())

selected_row = df[df["Year"] == year]

# Charts
st.header("📈 Climate Trends")
col1, col2 = st.columns(2)

with col1:
    fig1 = px.line(df, x="Year", y="Rainfall_mm", title="Rainfall Over Time (mm)")
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    fig2 = px.line(df, x="Year", y="Temperature_C", title="Temperature Over Time (°C)")
    st.plotly_chart(fig2, use_container_width=True)

# Metrics
st.subheader(f"📊 Climate Projections for {year}")
st.metric("Rainfall (mm)", int(selected_row['Rainfall_mm']))
st.metric("Temperature (°C)", float(selected_row['Temperature_C']))

# Map Placeholder
st.header("🗺️ Ganga River Map Placeholder")
m = folium.Map(location=[26.5, 83.0], zoom_start=6)
folium.Marker(location=[29.95, 78.17], popup="Haridwar").add_to(m)
folium.Marker(location=[25.25, 87.00], popup="Bhagalpur").add_to(m)
st_data = st_folium(m, width=1000)

# Footer
st.markdown("---")
st.caption("Prototype | Climate Digital Twin | Riverathon 1.0")
