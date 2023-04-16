import pandas as pd
import plotly.express as px  
import streamlit as st
import geopandas
import matplotlib.pyplot as plt
import json
import numpy as np


st.set_page_config(page_title="French cinema analysis", page_icon="🎥", layout="wide")


@st.cache_data
def get_data():
    value_df = pd.read_excel("pages/data/data_martin.xlsx")
    geo_df = geopandas.read_file('pages/data/departements_martin.geojson')
    df = geo_df.merge(value_df, on='code', how='left').set_index('code')

    #countries_df = geopandas.read_file("pages/data/eu_countries.geojson")
    #countries = ["France", "Spain", "Belgium", "Italy", "Luxembourg", "Switzerland", "Germany", "Portugal", "Austria", "Netherlands", "Croatia", 'Czech Republic', "Slovenia", 'Andorra','Liechtenstein', 'United Kingdom', "Hungary", "Poland", "Slovakia", 'Bosnia and Herzegovina', "Montenegro", 'Republic of Serbia']
    #eu_df = countries_df[countries_df.ADMIN.isin(countries)] #.set_index("ADMIN")
    eu_df = geopandas.read_file("pages/data/eu_countries.geojson")
    return df, eu_df

st.title("Dashboard")


df, eu_df = get_data()

max = 150
min = 0
values = st.slider("Select value range:", min_value=min, value=(min, max), max_value=max)

min_val, max_val = values
map_df = df.loc[(df.value >= min_val) & (df.value <= max_val)]

fig = px.choropleth_mapbox(eu_df, geojson=eu_df.geometry, locations=eu_df.index, color=np.zeros_like(eu_df.index),
                        color_continuous_scale="Viridis",
                        center={'lat': 46.5, 'lon': 2},
                        mapbox_style='white-bg',
                        range_color=(25, 110),
                        zoom=4.3,
                        opacity=0.1,
                        hover_name='ADMIN') #.update(layout_showlegend=False)

fig2 = px.choropleth_mapbox(map_df, geojson=map_df.geometry, locations=map_df.index, color=map_df.value,
                        color_continuous_scale="Viridis",
                        range_color=(25, 110),
                        mapbox_style='white-bg',
                        zoom=4.3,
                        center={'lat': 46.5, 'lon': 2},
                        labels={'value':'Number'},
                        #hover_data={'code':False},
                        hover_name='nom', 
                        opacity=1)

fig.add_trace(fig2.data[0])
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.update_geos(fitbounds="locations", visible=True)

st.plotly_chart(fig, use_container_width=True)



hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)