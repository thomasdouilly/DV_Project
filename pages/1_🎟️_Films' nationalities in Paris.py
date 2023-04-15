import pandas as pd
import json
import numpy as np
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="French cinema analysis", page_icon="🎥", layout="wide")
st.title("Dashboard - Films' nationalities")

raw_data = pd.read_excel("pages/data/data.xlsx")
paris_arrondissement = raw_data[raw_data['code INSEE'].str.contains('^751', regex=True)].groupby('code INSEE').mean()
proportions = paris_arrondissement.reset_index()[['code INSEE', 'PdM en entrées des films français','PdM en entrées des films américains',
    'PdM en entrées des films européens', 'PdM en entrées des autres films', 'population de la commune']]

# Load the GeoJSON file with the district boundaries and coordinates
with open('pages/data/data.json', 'r') as f:
    geojson = json.load(f)

coordinates_ardsmt = {}
contours_ardsmt = {}
for feature in geojson['features']:
    district = feature['properties']['c_arinsee']
    contours = feature['geometry']['coordinates']
    if district != 75107:
        coordinates_ardsmt[str(district)] = tuple(feature['properties']['geom_x_y'].values())
        contours_ardsmt[str(district)] = np.array(contours)[0]

sorted_dict = dict(sorted(coordinates_ardsmt.items(), key=lambda x: x[0]))
site_lat = [x[1] for x in list(sorted_dict.values())]
site_lon = [x[0] for x in list(sorted_dict.values())]

sorted_dict_contours = dict(sorted(contours_ardsmt.items(), key=lambda x: x[0]))
contours_lat = [x[:, 1] for x in list(sorted_dict_contours.values())]
contours_lon = [x[:, 0] for x in list(sorted_dict_contours.values())]

french = list(proportions['PdM en entrées des films français'])
euro = list(proportions['PdM en entrées des films européens'])
american = list(proportions['PdM en entrées des films américains'])
other = list(proportions['PdM en entrées des autres films'])

fig = go.Figure()
offset = 15e-4
scale = 16e-5

fig.add_trace(go.Scattermapbox(lat=contours_lat[0], lon=contours_lon[0], mode='lines',
	line=go.scattermapbox.Line(
	  width=1,
	  color='lightgrey',
	),
	hoverinfo='none', showlegend=False
))
    
fig.add_trace(go.Scattermapbox(
	lat=[str(site_lat[0]), str(site_lat[0]+(french[0]*scale))],
	lon=[str(site_lon[0]-(3*offset)), str(site_lon[0]-(3*offset))],
	mode='lines',
	line=go.scattermapbox.Line(
	  width=6,
	  color='rgb(87, 117, 144)',
	),
	text=f'Market share in entries: {np.round(french[0], 2)}%', hoverinfo='text',
	legendgrouptitle_text="French films", legendgroup="g1", name='Click here'
))

fig.add_trace(go.Scattermapbox(
	lat=[str(site_lat[0]), str(site_lat[0]+(euro[0]*scale))],
	lon=[str(site_lon[0]-(offset)), str(site_lon[0]-(offset))],
	mode='lines',
	line=go.scattermapbox.Line(
	  width=6,
	  color='rgb(240, 138, 75)',
	),
	text=f'Market share in entries: {np.round(euro[0], 2)}%', hoverinfo='text',
	legendgrouptitle_text="European films", legendgroup="g2", name='Click here'
))

fig.add_trace(go.Scattermapbox(
	lat=[str(site_lat[0]), str(site_lat[0]+(american[0]*scale))],
	lon=[str(site_lon[0]+(offset)), str(site_lon[0]+(offset))],
	mode='lines',
	line=go.scattermapbox.Line(
	  width=6,
	  color='rgb(232, 211, 63)',
	),
	text=f'Market share in entries: {np.round(american[0], 2)}%', hoverinfo='text',
	legendgrouptitle_text="American films", legendgroup="g3", name='Click here'
))

fig.add_trace(go.Scattermapbox(
	lat=[str(site_lat[0]), str(site_lat[0]+(other[0]*scale))],
	lon=[str(site_lon[0]+(3*offset)), str(site_lon[0]+(3*offset))],
	mode='lines',
	line=go.scattermapbox.Line(
	  width=6,
	  color='rgb(193, 171, 166)',
	),
	text=f'Market share in entries: {np.round(other[0], 2)}%', hoverinfo='text',
	legendgrouptitle_text="Other films", legendgroup="g4", name='Click here'
))

for i in range(1, len(site_lon)):

    fig.add_trace(go.Scattermapbox(lat=contours_lat[i], lon=contours_lon[i], mode='lines',
		line=go.scattermapbox.Line(
		  width=1,
		  color='lightgrey',
		),
		hoverinfo='none', showlegend=False
  	))
    
    fig.add_trace(go.Scattermapbox(
		lat=[str(site_lat[i]), str(site_lat[i]+(french[i]*scale))],
		lon=[str(site_lon[i]-(3*offset)), str(site_lon[i]-(3*offset))],
		mode='lines',
		line=go.scattermapbox.Line(
		  width=6,
		  color='rgb(87, 117, 144)',
		),
		text=f'Market share in entries: {np.round(french[i], 2)}%', hoverinfo='text',
		legendgrouptitle_text="French films", legendgroup="g1", showlegend=False
	))
    
    fig.add_trace(go.Scattermapbox(
		lat=[str(site_lat[i]), str(site_lat[i]+(euro[i]*scale))],
		lon=[str(site_lon[i]-(offset)), str(site_lon[i]-(offset))],
		mode='lines',
		line=go.scattermapbox.Line(
		  width=6,
		  color='rgb(240, 138, 75)',
		),
		text=f'Market share in entries: {np.round(euro[i], 2)}%', hoverinfo='text',
		legendgrouptitle_text="European films", legendgroup="g2", showlegend=False
	))
    
    fig.add_trace(go.Scattermapbox(
		lat=[str(site_lat[i]), str(site_lat[i]+(american[i]*scale))],
		lon=[str(site_lon[i]+(offset)), str(site_lon[i]+(offset))],
		mode='lines',
		line=go.scattermapbox.Line(
		  width=6,
		  color='rgb(232, 211, 63)',
		),
		text=f'Market share in entries: {np.round(american[i], 2)}%', hoverinfo='text',
		legendgrouptitle_text="American films", legendgroup="g3", showlegend=False
	))
    
    fig.add_trace(go.Scattermapbox(
		lat=[str(site_lat[i]), str(site_lat[i]+(other[i]*scale))],
		lon=[str(site_lon[i]+(3*offset)), str(site_lon[i]+(3*offset))],
		mode='lines',
		line=go.scattermapbox.Line(
		  width=6,
		  color='rgb(193, 171, 166)',
		),
		text=f'Market share in entries: {np.round(other[i], 2)}%', hoverinfo='text',
		legendgrouptitle_text="Other films", legendgroup="g4", showlegend=False
	))

fig.update_layout(
    title="Entries proportion depending on the film's nationality for each district (Paris)",
    autosize=True,
    hovermode='closest',
    showlegend=True,
    mapbox=dict(
	    accesstoken='pk.eyJ1IjoidWdvZGVteSIsImEiOiJjbGdpMDVzcTYwZ2N5M2NsZnBvMTRibnZjIn0.lPnU800P1LbpoFakLkyqtw',
	    center={'lat': 48.8566, 'lon': 2.3522},
	    zoom=11,
	    style='light'
    ),
)

st.plotly_chart(fig, use_container_width=True)

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)