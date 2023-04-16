import altair as alt
import altair_transform as alt_transform 
### Pip function to install the module : pip install git+https://github.com/altair-viz/altair-transform.git

import streamlit as st
### Pip function to install the module : pip install streamlit

import pandas as pd

# Data importation
data = pd.read_excel('./pages/data/data.xlsx', index_col = "N° auto", true_values = ['OUI'], false_values = ['NON'])


# Data refining
data = data[['nom', 'région administrative', 'commune', 'unité urbaine', 'séances', 'entrées 2020', 'entrées 2021', 'multiplexe']]
data['multiplexe'].replace(False, 'Miniplex', inplace = True)
data['multiplexe'].replace(True, 'Multiplex', inplace = True)

regions_list = data.groupby("région administrative").max().index.to_list()

def main_plot(year = 2021, regions = regions_list, type = ['Miniplex', 'Multiplex']):
    """main_plot

    Args:
        year (int, optional): Year to filter. Defaults to 2021.
        regions (_type_, optional): Regions to filter. Defaults to regions_list.
        type (list, optional): Type of cinemas to filter. Defaults to ['Miniplex', 'Multiplex'].

    Returns:
        The altair plot as well as the ratios (global and specific)
    """
    
    # Considering two possible cases for year
    if year == 2021:
        y_plot = 'entrées 2021'
        pad = 4738.801911332528
    else:
        y_plot = 'entrées 2020'
        pad = 2732.255890096887
            
    
    # Computation of main plot
    main_plot = alt.Chart(data, title = 'French cinemas according to number of showings and tickets sold in ' + str(year)).mark_point().encode(
        x = alt.X('séances', scale = alt.Scale(domain = (0, 40000)), title = 'Number of showings'),
        y = alt.Y(y_plot, scale = alt.Scale(domain = (0, 1500000)), title = 'Number of tickets sold in ' + str(year)), 
        tooltip = [alt.Tooltip("nom", title = 'Cinema name'), alt.Tooltip('commune', title = 'City'), alt.Tooltip("région administrative", title = 'French region'), alt.Tooltip("séances", title = "Number of showings"), alt.Tooltip(y_plot, title = "Ticket solds in " + str(year))]
    ).transform_filter(alt.FieldOneOfPredicate(field='région administrative', oneOf = regions)).transform_filter(alt.FieldOneOfPredicate(field='multiplexe', oneOf = type)).add_selection()
    
    # Calculation of regression line
    regression_line = main_plot.transform_regression('séances', y_plot, extent = (0, 40000)).encode(color = alt.value("#FF0000")).mark_line()
    mark_plot = main_plot.encode(color = alt.Color('multiplexe', legend = alt.Legend(title = "Cinema category", orient = "bottom"))).mark_point()
    text = main_plot.mark_text(baseline="middle", dy = 12, fontSize = 9).encode(text="nom").transform_filter(alt.FieldGTPredicate(alt.datum.séances, gt = 1500)) 

    # Adding layer to compute final plot    
    final_plot = alt.layer(mark_plot + text, regression_line)

    # Calculations to compute ratio
    regression_params = alt_transform.extract_data(regression_line)
    initial_point = regression_params.iloc[0].to_list()
    final_point = regression_params.iloc[1].to_list()
    
    ratio = (final_point[1] - initial_point[1]) / (final_point[0] - initial_point[0])
    ratio_france = ((data[y_plot] + pad).sum()) / data['séances'].sum()
    
    return final_plot, ratio, ratio_france


# Streamlit initialization page
st.set_page_config(page_title = 'French cinema analysis', page_icon="🎥")

# Refining of some paragraph classes
st.markdown("""
        <style>
              
        </style>
        """, unsafe_allow_html=True)

st.markdown("""
<style>
.begin-font {
    font-size:20px;
}
.ratio-font {
    font-size:32px !important;
    text-align: center;
}
.center-font {
    font-size:20px;
    text-align: center;
}
.title {
    font-size:40px
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
.st-be {
    padding-top:0px;
}
.css-1544g2n{
    padding:2rem 0.5rem 0.5rem;
}
.css-10y5sf6 {
    font-size:0px
}
</style>
""", unsafe_allow_html=True)

st.markdown('<p class = title><b>Increasing the number of showings is often profitable for a French cinema</b></p>', unsafe_allow_html = True)

# Creation of customization menu
with st.sidebar:
    st.sidebar.title('Graph personnalization')
    year = st.slider('Year :', 2020, 2021, 2021, format = None)
    cinema_type = st.multiselect("Category of cinemas :", ['Multiplex', 'Miniplex'], ['Multiplex', 'Miniplex'])
    regions = st.multiselect("French 'Régions' :", regions_list, regions_list)

plot, ratio_selec, ratio_fr = main_plot(year, regions, cinema_type)
plot = plot.properties(width=600, height=425)


# Creation of the two tabs of the main plot
tab1, tab2 = st.tabs(["Summary", "Data"])

with tab1:
    st.markdown('<p class = begin-font> In ' + str(year) + ', an average of :</p>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    col1.markdown("<p class = ratio-font><b>" + str(round(ratio_selec, 1)) + "</b></p>", unsafe_allow_html=True)
    col1.markdown('<p class = center-font>tickets were sold for each<br>showing<br>--- FILTERED CINEMAS ---</p>', unsafe_allow_html=True)


    col2.markdown("<p class = ratio-font><b>" + str(round(ratio_fr, 1)) + "</b></p>", unsafe_allow_html=True)
    col2.markdown('<p class = center-font>tickets were sold for each<br>showing<br>--- ALL CINEMAS ---</p>', unsafe_allow_html=True)

with tab2:
    st.altair_chart(plot, theme = None)

