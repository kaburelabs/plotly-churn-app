
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
from components.utils.generate_dropdowns import input_components, load_input_dict
from components.utils.load_data import create_input_table

from components.utils.load_model import prediction


project_list=load_input_dict().keys()

app.layout=html.Div([
    html.Div(id="starting-div", 
             children=["Start"], style={"display":"none"}),
    dcc.Store(id="df-app"),
    dcc.Store(id="dropdown-options"),
    navbar,
    html.Div(
        [
            html.Div(id="dropdown-ml-inputs"),
            dcc.Loading(html.Div(id="output-content"))
        ], id="container-box", className="containerStyle")
])


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


@app.callback(
    Output("dropdown-ml-inputs", "children"),
    Input("dropdown-options", "data")
)
def getting_data(dropdown_data):

    return html.Div(
        [
            html.H1("Fill the features to get your churn prediction", className="text-center"), 
            html.Div(dbc.Row([input_components(dropdown_data,col_name)\
                        for col_name in dropdown_data.keys() \
                            if col_name not in ["CustomerID", "City"]]), className="bottom64"),
            html.Div(html.Button(["Predict"], id="btn-predict", className="buttonStyle"), className="text-center")
        ])




@app.callback(
    Output("output-content", "children"),
    Input("btn-predict", 'n_clicks'),
    [State(f"input-{input}", 'value') \
        for input in project_list \
            if input not in ["CustomerID", "City", "Churn Value"]],
    prevent_initial_call=True
)
def getting_input_parameters(btn_clicks, gender, senior_citzen, partner, \
                             dependents,tenure, phone_service, multiple_lines, internet_service,\
                             online_security, online_backup, device_protection, tech_support, \
                             streaming_tv, streaming_movies, contract, paperless_bill, payment_method, \
                             monthly_charges, total_charges):

    all_inputs=["IDdummy", "CityDummy", \
                gender, senior_citzen, partner, \
                dependents,tenure, phone_service, multiple_lines, internet_service,\
                online_security, online_backup, device_protection, tech_support, \
                streaming_tv, streaming_movies, contract, paperless_bill, payment_method, \
                monthly_charges, total_charges]

    if btn_clicks == None:
        raise PreventUpdate

    elif None in all_inputs:
        raise PreventUpdate

    else: 
        time.sleep(2)
        user_new_input = create_input_table(all_inputs)

        predictions=prediction(user_new_input)

        will_churn="The model prediction is that this customer has a high chance to Churn this time."
        will_no_churn="The model prediction is that this customer has a low chance to Churn and will not Churn this time."
        
        return f"{will_churn if int(predictions['Label'][0]) == 1 else will_no_churn}"



if __name__ == '__main__':
    app.run_server(debug=True, port="8879")

