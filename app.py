import streamlit as st
import pandas as pd
import plotly.express as px
import folium
from streamlit_folium import st_folium
import geopandas as gpd

st.set_page_config(page_title="Climate Digital Twin", layout="wide")

st.title("Climate Digital Twin: Ganga River (India)")

# Loading data
df = pd.read_csv("data/predicted_rainfall_temp.csv", encoding='utf-8-sig')
df.columns = df.columns.str.strip()

# Year Selector
min_year = int(df["Year"].min())
max_year = int(df["Year"].max())
year = st.slider("Select Year", min_year, max_year, step=1)

selected_row = df[df["Year"] == year].iloc[0]

# Climate Metrics
st.subheader(f"Climate for {year} ({selected_row['Source']})")
st.metric("Rainfall (mm)", f"{selected_row['Rainfall_mm']:.2f}")
st.metric("Temperature (°C)", f"{selected_row['Temperature_C']:.2f}")

# Climate Trend Graphs
st.header("Climate Trends")

col1, col2 = st.columns(2)

st.subheader("Rainfall Over Time (mm)")
fig1 = px.line(df, x="Year", y="Rainfall_mm", title="Rainfall Over Time (mm)")
st.plotly_chart(fig1, use_container_width=True)

st.subheader("🌡️ Temperature Over Time (°C)")
fig2 = px.line(df, x="Year", y="Temperature_C", title="Temperature Over Time (°C)")
st.plotly_chart(fig2, use_container_width=True)




# Map Visualization
st.header("Ganga River Map(India)")

gdf = gpd.read_file("data/ganga_stretch.geojson")

m = folium.Map(location=[26.5, 83.0], zoom_start=6)

folium.GeoJson(
    gdf,
    name="Ganga Stretch",
    style_function=lambda x: {
        "color": "blue",
        "weight": 4,
        "opacity": 0.8
    }
).add_to(m)

folium.LayerControl().add_to(m)
st_data = st_folium(m, width=1000)
