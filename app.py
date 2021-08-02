
from server import app

import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State, MATCH, ALL
import pandas as pd
import json
from dash.exceptions import PreventUpdate

import time

from components.utils.navbar import navbar

from components.prediction import prediction_layout

server = app.server

app.layout=html.Div([
    html.Div(id="starting-div", 
             children=["Start"], style={"display":"none"}),
    dcc.Store(id="df-app"),
    dcc.Store(id="dropdown-options"),
    dcc.Location(id="url"),
    navbar,
    html.Div(
        [
            html.Div(id="output-content")
        ], 
        id="container-box", 
        className="containerStyle")
])

@app.callback(
    Output("df-app", "data"),
    Input("starting-div", "children")
)
def getting_data(start_app):

    telco_df = pd.read_csv("assets/data/IBM-2020.csv")

    return telco_df.to_json(date_format='iso', orient='split')


@app.callback(
    Output("dropdown-options", "data"),
    Input("starting-div", "children")
)
def getting_data(app_data):

    # Opening JSON file
    f = open('assets/data/inputs_options.json')

    # returns JSON object as 
    # a dictionary
    input_data = json.load(f)

    # Closing file
    f.close()

    return  input_data["features"]


# add callback for toggling the collapse on small screens
@app.callback(
    Output("navbar-collapse", "is_open"),
    [Input("navbar-toggler", "n_clicks")],
    [State("navbar-collapse", "is_open")],
)
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


@app.callback(
    Output("output-content", "children"),
    Input("url", "pathname")
)
def getting_data(app_pathname):

    if app_pathname == "/":
        return prediction_layout

    else:
        raise PreventUpdate



if __name__ == '__main__':
    app.run_server(debug=True, port="8879")

