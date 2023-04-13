import altair as alt
import altair_transform as alt_transform 
### Pip function to install the module : pip install git+https://github.com/altair-viz/altair-transform.git

import streamlit as st
### Pip function to install the module : pip install streamlit


import panel as pn
import numpy as np
import pandas as pd
import csv

data = pd.read_excel('./data/data.xlsx', index_col = "N° auto", true_values = ['OUI'], false_values = ['NON'])

data = data[['nom', 'région administrative', 'commune', 'unité urbaine', 'séances', 'entrées 2020', 'entrées 2021', 'multiplexe']]

regions_list = data.groupby("région administrative").max().index.to_list()

def main_plot(year = 2021, regions = regions_list):
    
    if year == 2021:
        y_plot = 'entrées 2021'
    else:
        y_plot = 'entrées 2020'
        
    main_plot = alt.Chart(data).mark_point().encode(
        x = alt.X('séances', scale = alt.Scale(domain = (0, 25000))),
        y = alt.Y(y_plot, scale = alt.Scale(domain = (0, 600000))), 
        tooltip = ["nom", "région administrative"]
    ).transform_filter(alt.FieldOneOfPredicate(field='région administrative', oneOf = regions))
    
    regression_line = main_plot.transform_regression('séances', y_plot, extent = (0, 25000)).encode(color=alt.value("#FF0000")).mark_line()
    mark_plot = main_plot.encode(color = alt.Color('multiplexe', legend = alt.Legend(title = '', orient='bottom', direction='horizontal', titleAnchor='middle', values = ['Miniplex', 'Multiplex']))).mark_point()
    text = main_plot.mark_text(baseline="middle", dy = 12, fontSize = 10).encode(text="nom").transform_filter(alt.FieldGTPredicate(alt.datum.séances, gt = 1500))

    final_plot = alt.layer(mark_plot + text, regression_line).properties(width=800, height=500).interactive()

    regression_params = alt_transform.extract_data(regression_line)
    initial_point = regression_params.iloc[0].to_list()
    final_point = regression_params.iloc[1].to_list()
    ratio = (final_point[1] - initial_point[1]) / (final_point[0] - initial_point[0])
    
    print(ratio)
    
    return final_plot


"""
pn.extension()

year = pn.widgets.IntSlider(name='Year', value=2021, start=2020, end=2021, width = 100, align = 'center')

regions = pn.widgets.CheckButtonGroup(name='French région', value = regions_list, options = regions_list, orientation = 'vertical', button_type = 'primary')

def update(event):
    if event.cls.name == 'All':
        regions.value = regions_list
    if event.cls.name == 'None':
        regions.value = []

regions_all = pn.widgets.Button(name='All', button_type='primary')
regions_none = pn.widgets.Button(name='None', button_type='primary')

regions_all.on_click(update)
regions_none.on_click(update)

interactive_plot = pn.bind(main_plot, year = year, regions = regions)
dataviz_app = pn.Row(pn.Column(year, interactive_plot), pn.Column(pn.Row(regions_all, regions_none), regions))
dataviz_app.show()
"""


st.title('How to link number of showings and number of ticket solds in French cinemas ?')

year = st.slider('Year', 2020, 2021, 2020, format = None)
#regions = st.multiselect("Please select the French 'Régions' to be considered in the graph :", [], regions_list)

#plot = main_plot(year, regions)

#st.altair_chart(plot)

