import pandas as pd
import plotly.express as px  
import streamlit as st
import geopandas
import matplotlib.pyplot as plt
import json
import numpy as np


st.set_page_config(page_title="French cinema analysis", page_icon="🎥", layout="wide")

st.title("Tickets sold per seat by department in France, 2021")


@st.cache_data
def get_data():
    # Get values and geographical data
    value_df = pd.read_excel("pages/data/data_martin.xlsx")
    geo_df = geopandas.read_file('pages/data/departements_martin.geojson')
    df = geo_df.merge(value_df, on='code', how='left').set_index('code')

    # Get european countries for background 
    eu_df = geopandas.read_file("pages/data/eu_countries.geojson")
    return df, eu_df


df, eu_df = get_data()

# Slider to select the range of values to display
values = st.slider("Select range of values to be displayed on the chart below:", min_value=0, value=(0, 150), max_value=150)
min_val, max_val = values
map_df = df.loc[(df.value >= min_val) & (df.value <= max_val)]

# Europe countries as background for the figure
fig = px.choropleth_mapbox(eu_df, geojson=eu_df.geometry, locations=eu_df.index, color=40*np.ones_like(eu_df.index),
                        color_continuous_scale="Viridis",
                        range_color=(0, 150),
                        mapbox_style='white-bg',
                        center={'lat': 46.5, 'lon': 2},
                        zoom=4.1,
                        opacity=0.1,
                        hover_name='ADMIN') #.update(layout_showlegend=False)

# French departments
fig2 = px.choropleth_mapbox(map_df, geojson=map_df.geometry, locations=map_df.index, color=map_df.value,
                        color_continuous_scale="Viridis",
                        range_color=(0, 150),
                        mapbox_style='white-bg',
                        center={'lat': 46.5, 'lon': 2},
                        zoom=4.1,
                        opacity=1,
                        labels={'value':'Tickets sold per seat'},
                        hover_name='nom')

# Superpose maps
fig.add_trace(fig2.data[0])
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, coloraxis_colorbar=dict(title="", orientation='h', y=1, len=1.055, thickness=40))
fig.update_geos(fitbounds="locations", visible=True)

# Display chart
st.plotly_chart(fig, use_container_width=True)



hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)