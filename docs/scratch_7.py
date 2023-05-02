# If you prefer to run the code online instead of on your computer click:
# https://github.com/Coding-with-Adam/Dash-by-Plotly#execute-code-in-browser

from dash import Dash, dcc, Output, Input  # pip install dash
import dash_bootstrap_components as dbc    # pip install dash-bootstrap-components
import plotly.express as px
import pandas as pd                        # pip install pandas
import json

# Read the stuff
london_map = json.load(open("london_boroughs.json", "r"))
london_data = pd.read_csv("london_boroughs.csv")

# Build our components
app = Dash(__name__, external_stylesheets=[dbc.themes.LUX])
mytitle = dcc.Markdown(children='')
mygraph = dcc.Graph(figure={})
dropdown = dcc.Dropdown(options=london_data.columns.values[2:],
                        value='Median Salary',  # initial value displayed when page first loads
                        clearable=False)

# Customize your own Layout
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([mytitle], width=6)
    ], justify='center'),
    dbc.Row([
        dbc.Col([mygraph], width=12)
    ]),
    dbc.Row([
        dbc.Col([dropdown], width=6)
    ], justify='center'),

], fluid=True)

# Callback allows components to interact
@app.callback(
    Output(mygraph, 'figure'),
    Output(mytitle, 'children'),
    Input(dropdown, 'value')
)
def update_graph(column_name):  # function arguments come from the component property of the Input

    print(column_name)
    print(type(column_name))
    # https://plotly.com/python/choropleth-maps/
    fig = px.choropleth_mapbox(london_data,
                               geojson=london_map,
                               locations='code',
                               featureidkey='properties.code',
                               color=column_name,
                               hover_name="area",
                               hover_data=["population_size"],
                               title="Greater London Area",
                               mapbox_style="carto-positron",
                               color_continuous_scale="Viridis",
                               # color_continuous_midpoint = 0,
                               opacity=0.8,
                               center={"lat": 51.5073359, "lon": -0.12765},
                               labels={"code": "Code", "population_size": "Population",
                                       "median_salary": "Median Salary"},
                               zoom=8.5)
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})  # just remove margin

    #fig = px.choropleth(data_frame=df,
    #                    locations='STATE',
    #                    locationmode="USA-states",
    #                    scope="usa",
    #                    height=600,
    #                    color=column_name,
    #                    animation_frame='YEAR')

    return fig, '# '+column_name  # returned objects are assigned to the component property of the Output

# Run app
if __name__=='__main__':
    app.run_server(debug=False, port=8044)

