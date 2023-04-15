import altair as alt
import pandas as pd
import streamlit as st


st.set_page_config(page_title="Dashboard Seats", page_icon=":seedling:", layout="wide")


@st.cache_data
def get_data():
    df = pd.read_csv("./data.csv")
    df = df[["unité urbaine", "fauteuils", "population unité urbaine", "pers/faut"]]
    df = df.sort_values('population unité urbaine').reset_index()
    df['index'] = df.reset_index().index
    df = df.rename(columns={
        'unité urbaine': 'Area',
        'fauteuils': 'Seats',
        'population unité urbaine': 'Population', 
        'pers/faut' : 'Number of persons per seats'
    })
    return df

st.title("Correlation between seats and population in French urban areas")


df = get_data()

max = int(max(df["Population"]))
min = 0
values = st.slider("Select value range of the population of areas:", min_value=min, value=(100000, 2000000), max_value=max)

min_val, max_val = values
df = df[(df['Population'] >= min_val) & (df['Population'] <= max_val)]

click = alt.selection_multi(fields=['Area'])
############### AREA CHART #####################
base = alt.Chart(df).encode(
    alt.X('index:O', axis=alt.Axis(title=None, labels=False))
)
area_1 = base.mark_area(opacity=0.5, color='blue').encode(
    alt.Y('Population:Q',
          axis=alt.Axis(title='Population in urban area', titleColor='blue'))
)
area_2 = base.mark_area(opacity=0.5, color='red').encode(
    alt.Y('Seats:Q',
          axis=alt.Axis(title='Seats in urban area', titleColor='red'))
)
chart_area = (area_1 + area_2).resolve_scale(
    y = 'independent'
)
chart_area = chart_area.encode(tooltip=['Area:N', 'Population:Q', 'Seats:Q', alt.Tooltip('Number of persons per seats:Q', format='.1f')])
#chart_area = chart_area.configure_axisX(labels=False)
chart_area = chart_area.properties(title='Evolution of population and number of seats by urban areas')

############### BAR CHART #####################
mean_value = int(df['Number of persons per seats'].mean())
# add mean line and label
mean_line = alt.Chart(pd.DataFrame({'mean_value': [mean_value]})).mark_rule(color='black').encode(
    y=alt.Y('mean_value:Q', axis=alt.Axis(title='Number of persons per seats', titleColor='green'))
)
mean_label = alt.Chart(pd.DataFrame({'mean_value': [mean_value]})).mark_text(color='black', dx=-517, dy=0, align='left').encode(
    y=alt.Y('mean_value:Q'),
    text=alt.Text('mean_value:Q')
)
bars = alt.Chart(df).mark_bar(color='green').encode(
    x=alt.X('Area:N', 
            axis=alt.Axis(title='Names of urban areas'),
            sort=None),
    y='Number of persons per seats:Q'
)
chart_bars = bars + mean_line + mean_label
chart_bars = chart_bars.properties(title='Number of persons by cinemas seats in urban areas')
chart_bars = chart_bars.encode(tooltip=['Area:N', 'Population:Q', 'Seats:Q', alt.Tooltip('Number of persons per seats:Q', format='.1f')])

############### TOTAL CHART #####################
# Define chart configuration options
chart_config = {
    'axis': {
        'labelFontSize': 12,
        'titleFontSize': 14,
    },
    'title': {
        'fontSize': 16,
    },
}
chart_area = chart_area.transform_filter(
    click
)
chart_bars = chart_bars.add_selection(
    click
)

# Combine charts using VConcatChart
chart = alt.vconcat(chart_area, chart_bars, spacing=10)
# Apply chart configuration to the concatenated chart object
chart = chart.configure_view(width=1000, height=200)

chart = chart.configure_title(anchor='middle')
chart = chart.configure_mark(opacity=0.8)
# Apply chart configuration to all axes and titles
chart = chart.configure_axis(**chart_config['axis'])
chart = chart.configure_title(**chart_config['title'])

##################STREAMLIT VIEW##############""

st.altair_chart(chart, use_container_width=False, theme="streamlit")

st.header('Explanations')
st.markdown('This visualisation allows to see the correlation between the number of seats in cinemas and the population in urban units. In the first graph we see that both parameters follow the same trends. On the bar chart, we see the number of people per seat. This makes it possible to detect outliers at a glance.')

st.header('Interactions')
st.markdown('The user can first play with the slider to select the size of the urban areas studied. This allows the user to zoom in or out as required. Then, by moving the mouse over the first or second graph, additional data will appear, giving details of population, number of seats and number of people per seat. On the second graph, a line is drawn with the average number of people per seat in the selected sample on the left. Finally, the user can filter the graphs by clicking on the bars of the bar plot and see only those areas in the first graph. This feature is especially useful for comparing different areas, which are selected by clicking and holding the SHIFT key.')


hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)