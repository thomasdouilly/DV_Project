import altair as alt
import altair_transform as alt_transform 
### Pip function to install the module : pip install git+https://github.com/altair-viz/altair-transform.git

import streamlit as st
### Pip function to install the module : pip install streamlit

import pandas as pd

data = pd.read_excel('./data/data.xlsx', index_col = "N° auto", true_values = ['OUI'], false_values = ['NON'])

data = data[['nom', 'région administrative', 'commune', 'unité urbaine', 'séances', 'entrées 2020', 'entrées 2021', 'multiplexe']]
data['multiplexe'].replace(False, 'Miniplex', inplace = True)
data['multiplexe'].replace(True, 'Multiplex', inplace = True)

regions_list = data.groupby("région administrative").max().index.to_list()


brush = alt.selection_interval()

def main_plot(year = 2021, regions = regions_list):
    
    if year == 2021:
        y_plot = 'entrées 2021'
        pad = 4738.801911332528
    else:
        y_plot = 'entrées 2020'
        pad = 2732.255890096887
            
    
    main_plot = alt.Chart(data).mark_point().encode(
        x = alt.X('séances', scale = alt.Scale(domain = (0, 40000))),
        y = alt.Y(y_plot, scale = alt.Scale(domain = (0, 1500000))), 
        tooltip = ["nom", "région administrative"]
    ).transform_filter(alt.FieldOneOfPredicate(field='région administrative', oneOf = regions)).add_selection()
    
    
    regression_line = main_plot.transform_regression('séances', y_plot, extent = (0, 40000)).encode(color = alt.value("#FF0000")).mark_line()
    mark_plot = main_plot.encode(color = alt.condition(brush, 'multiplexe', alt.value('grey'))).mark_point()
    text = main_plot.mark_text(baseline="middle", dy = 12, fontSize = 10).encode(text="nom").transform_filter(alt.FieldGTPredicate(alt.datum.séances, gt = 1500))
    selection_line = main_plot.transform_filter(brush)
    
    final_plot = alt.layer(mark_plot + text, regression_line).configure_legend(title = '', orient='bottom')

    regression_params = alt_transform.extract_data(regression_line)
    initial_point = regression_params.iloc[0].to_list()
    final_point = regression_params.iloc[1].to_list()
    
    ratio = (final_point[1] - initial_point[1]) / (final_point[0] - initial_point[0])
    ratio_france = ((data[y_plot] + pad).sum()) / data['séances'].sum()
    
    return final_plot, ratio, ratio_france


st.set_page_config(page_title = 'Cinema Analysis')

st.markdown("""
        <style>
              
        </style>
        """, unsafe_allow_html=True)

st.markdown("""
<style>
.begin-font {
    font-size:14px;
}
.ratio-font {
    font-size:20px !important;
    text-align: center;
}
.center-font {
    font-size:14px;
    text-align: center;
}
.title {
    font-size:32px
}
.block-container {
    padding-top: 0.5rem;
    padding-bottom: 0rem;
    padding-left: 3rem;
    padding-right: 3rem;
}
.reportview-container .sidebar-content {
    padding-top: 10rem;
}
span[data-baseweb="tag"] {
  background-color: gray !important;
}
.st-af {
    font-size:12px;
}
.st-dw {
    max-width: 400px;
}
.css-1544g2n{
    padding:2rem 0.5rem 0.5rem;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<p class = title><b>How to link number of showings and number of ticket solds in French cinemas ?</b></p>', unsafe_allow_html = True)


with st.sidebar:
    year = st.slider('Year :', 2020, 2021, 2021, format = None)
    cinema_type = st.multiselect("Category of cinemas :", ['Multiplex', 'Miniplex'], ['Multiplex', 'Miniplex'])
    regions = st.multiselect("Please select the French 'Régions' to be considered in the graph :", regions_list, regions_list)

plot, ratio_selec, ratio_fr = main_plot(year, regions)
plot = plot.add_selection(brush).properties(width=700, height=600)

st.markdown('<p class = begin-font> In ' + str(year) + ', an average of :</p>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

col1.markdown("<p class = ratio-font><b>" + str(round(ratio_selec, 1)) + "</b></p>", unsafe_allow_html=True)
col1.markdown('<p class = center-font>tickets were sold for each<br>showing<br>*** SELECTION ONLY ***</p>', unsafe_allow_html=True)


col2.markdown("<p class = ratio-font><b>" + str(round(ratio_fr, 1)) + "</b></p>", unsafe_allow_html=True)
col2.markdown('<p class = center-font>tickets were sold for each<br>showing<br>*** WHOLE FRANCE ***</p>', unsafe_allow_html=True)

st.altair_chart(plot)

