
from dash_bootstrap_components._components.Collapse import Collapse
from server import app

import dash 
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State, MATCH, ALL
import pandas as pd
import json
from dash.exceptions import PreventUpdate
import time 

from components.utils.generate_dropdowns import input_components, load_input_dict

from components.utils.load_data import create_input_table

from components.utils.load_model import prediction


project_list=load_input_dict().keys()


prediction_layout=html.Div(
        [
            html.H1("IBM Customers Churn Prediction", className="text-center bottom32 top16"), 
            html.Div(id="customer-input-list", className="bottom32"),
            html.Div([html.Button(["Predict"], id="btn-predict", className="buttonStyle bottom16"),
                      dbc.Alert(
                            "You can't predict the Churn without all the features filled. Please fill all the input fields before clicking on the Predict button.",
                            id="alert-empty-inputs",
                            is_open=False,
                            duration=4000, color="danger",
                            className="alert-card-style"
                        )], 
                    className="text-center bottom16"),
            html.Div(id="prediction-result", style={"min-height":"250px"})
        ])



@app.callback(
    Output("customer-input-list", "children"),
    Input("dropdown-options", "data")
)
def generating_dropdowns(dropdown_data):

    return html.Div([
        html.Div([
            # html.H3("Churn Model "), 
            html.Div(dbc.Row(
                [
                    dbc.Col([
                        html.Div([
                            html.H3(["Demographic Features", html.Span(html.I(className="fas fa-question-circle font-sm", id="tooltip-demographic"), 
                                            style={"marginLeft":"5px"})], className="bottom16"),
                            dbc.Tooltip(
                                "Explanation about Demographic features.",
                                target="tooltip-demographic",
                            ),
                            dbc.Row([
                                dbc.Col(html.Div(
                                    [
                                        html.H4("Gender", className="font-sm"),
                                        dcc.Dropdown(id="input-Gender", 
                                                options=[{"label":val, "value":val} \
                                                    for val in dropdown_data["Gender"]])
                                    ]), lg=3, className="bottom16"),
                                dbc.Col(html.Div(
                                    [
                                        html.H4("Partner", className="font-sm"),
                                        dcc.Dropdown(id="input-Partner", 
                                                options=[{"label":val, "value":val} \
                                                    for val in dropdown_data["Partner"]],
                                                    value="No")
                                    ]), lg=3, className="bottom16"),
                                dbc.Col(html.Div(
                                    [
                                        html.H4(["Dependents", html.Span("*", style={"color":"red"})], className="font-sm"),
                                        dcc.Dropdown(id="input-Dependents", 
                                                options=[{"label":val, "value":val} \
                                                    for val in dropdown_data["Dependents"]],
                                                    value=None)
                                    ]), lg=3, className="bottom16"),
                                dbc.Col(html.Div(
                                    [
                                        html.H4("Senior Citizen", className="font-sm"),
                                        dcc.Dropdown(id="input-Senior Citizen", 
                                                    options=[{"label":val, "value":val} \
                                                        for val in dropdown_data["Senior Citizen"]], 
                                                    value="No")
                                    ]), lg=3, className="bottom16")])
                            ], className="style-input-cards")
                    ], lg=6),
                    dbc.Col([
                        html.Div([
                            html.H3(["Contract settings", html.Span(html.I(className="fas fa-question-circle font-sm", id="tooltip-contract"), 
                                            style={"marginLeft":"5px"})], className="bottom16"),
                            dbc.Tooltip(
                                "Contract Features & billing options.",
                                target="tooltip-contract",
                            ),
                            html.Div(dbc.Row(
                                [
                                    dbc.Col(html.Div(
                                        [
                                            html.H4(["Contract", html.Span("*", style={"color":"red"})], className="font-sm"),
                                            dcc.Dropdown(id="input-Contract", 
                                                    options=[{"label": "Monthly" if val == "Month-to-month" else val, "value":val} \
                                                        for val in dropdown_data["Contract"]],
                                                        value=None)
                                        ]), lg=4, className="bottom16"),
                                    dbc.Col(html.Div(
                                        [
                                            html.H4("Billing Option", className="font-sm"),
                                            dcc.Dropdown(id="input-Paperless Billing", 
                                                    options=[{"label":"Paperless" if val == "Yes" else "Paper", "value":val} \
                                                        for val in dropdown_data["Paperless Billing"]],
                                                        value="Yes")
                                        ]), lg=4, className="bottom16"),
                                    dbc.Col(html.Div(
                                        [
                                            html.H4("Payment Method", className="font-sm"),
                                            dcc.Dropdown(id="input-Payment Method", 
                                                    options=[{"label":val.replace("(automatic)", ""), "value":val} \
                                                        for val in dropdown_data["Payment Method"]],
                                                        value="Bank transfer (automatic)")
                                        ]), lg=4, className="bottom16")
                                ]
                            ))
                            ], className="style-input-cards")
                    ], lg=6)
                ]
            )),
        ], className="bottom32"),
        
        html.Div([
            # html.H3("Churn Model "), 
            html.Div(dbc.Row(
                [
                    dbc.Col([
                        html.Div([
                            html.H3(["Service Features", html.Span(html.I(className="fas fa-question-circle font-sm", id="tooltip-services"), 
                                            style={"marginLeft":"5px"})], className="bottom16"),
                            dbc.Tooltip(
                                "Explanation about the services.",
                                target="tooltip-services",
                            ),
                            html.Div([dbc.Row(
                                [
                                    dbc.Col(html.Div(
                                        [
                                            html.H4("Phone Service", className="font-sm"),
                                            dcc.Dropdown(id="input-Phone Service", 
                                                    options=[{"label":val, "value":val} \
                                                        for val in dropdown_data["Phone Service"]],
                                                        value="Yes")
                                        ]), lg=4, className="bottom16"),
                                    dbc.Col(html.Div(
                                        [
                                            html.H4("Internet Service", className="font-sm"),
                                            dcc.Dropdown(id="input-Internet Service", 
                                                        options=[{"label":val, "value":val} \
                                                            for val in dropdown_data["Internet Service"]],
                                                        value="Fiber optic")
                                        ]), lg=4, className="bottom16"),
                                    dbc.Col(html.Div(
                                        [
                                            html.Div([
                                                html.Span(html.I(className="fas fa-plus-circle"), 
                                                            style={"margin-right":"5px", "color":"#9c7d80"}),
                                                html.Span("Extra Services", className="font-sm")
                                                ], style={"cursor":"pointer", "paddingTop":"6px"}, id="load-more-button")

                                        ], style={"display":"flex", 
                                                  "align-items": "center"}),
                                            lg=2, className="bottom16", style={"display":"contents"})
                                ]),
                                dbc.Collapse([
                                    dbc.Row([
                                        dbc.Col(html.Div(
                                            [
                                                html.H4("Multiple Lines", className="font-sm"),
                                                dcc.Dropdown(id="input-Multiple Lines", 
                                                        options=[{"label":val, "value":val} \
                                                            for val in dropdown_data["Multiple Lines"]],
                                                            value="No")
                                            ]), lg=3, className="bottom16"),
                                        dbc.Col(html.Div(
                                            [
                                                html.H4("Online Security", className="font-sm"),
                                                dcc.Dropdown(id="input-Online Security", 
                                                        options=[{"label":val, "value":val} \
                                                            for val in dropdown_data["Online Security"]],
                                                            value="No")
                                            ]), lg=3, className="bottom16"),
                                        dbc.Col(html.Div(
                                            [
                                                html.H4("Online Backup", className="font-sm"),
                                                dcc.Dropdown(id="input-Online Backup", 
                                                        options=[{"label":val, "value":val} \
                                                            for val in dropdown_data["Online Backup"]],
                                                            value="No")
                                            ]), lg=3, className="bottom16"),
                                        dbc.Col(html.Div(
                                            [
                                                html.H4("Device Protection", className="font-sm"),
                                                dcc.Dropdown(id="input-Device Protection", 
                                                        options=[{"label":val, "value":val} \
                                                            for val in dropdown_data["Device Protection"]],
                                                            value="No")
                                            ]), lg=3, className="bottom16"),
                                        dbc.Col(html.Div(
                                            [
                                                html.H4("Tech Support", className="font-sm"),
                                                dcc.Dropdown(id="input-Tech Support", 
                                                        options=[{"label":val, "value":val} \
                                                            for val in dropdown_data["Tech Support"]],
                                                            value="No")
                                            ]), lg=3, className="bottom16"),
                                        dbc.Col(html.Div(
                                            [
                                                html.H4("Streaming TV", className="font-sm"),
                                                dcc.Dropdown(id="input-Streaming TV", 
                                                        options=[{"label":val, "value":val} \
                                                            for val in dropdown_data["Streaming TV"]],
                                                            value="No")
                                            ]), lg=3, className="bottom16"),
                                        dbc.Col(html.Div(
                                            [
                                                html.H4("Streaming Movies", className="font-sm"),
                                                dcc.Dropdown(id="input-Streaming Movies", 
                                                        options=[{"label":val, "value":val} \
                                                            for val in dropdown_data["Streaming Movies"]],
                                                            value="No")
                                            ]), lg=3, className="bottom16")
                                    ])
                                ], id="collapse-inputs")
                            ]),
                            ], className="style-input-cards", style={"height":"100%"})
                    ], lg=6),
                    dbc.Col([
                        html.Div([
                            html.H3(["Tenure & Charges", html.Span(html.I(className="fas fa-question-circle font-sm", id="tooltip-numericals"), 
                                            style={"marginLeft":"5px"})], className="bottom16"),
                            dbc.Tooltip(
                                "Tenure in months and Billing Charges.",
                                target="tooltip-numericals",
                            ),
                            dbc.Row(
                                [
                                    dbc.Col(html.Div(
                                        [
                                            html.H4("Tenure Months", className="font-sm"),
                                            dcc.Input(
                                                        id=f"input-Tenure Months", 
                                                        type="number",
                                                        className="width-100"
                                                    )
                                        ]), lg=3, className="bottom16"),
                                    dbc.Col(html.Div(
                                        [
                                            html.H4("Monthly Charges", className="font-sm"),
                                            dcc.Input(
                                                        id=f"input-Monthly Charges", 
                                                        type="number",
                                                        className="width-100"
                                                    )
                                        ]), lg=3, className="bottom16"),
                                    dbc.Col(html.Div(
                                        [
                                            html.H4("Total Charges", className="font-sm"),
                                            dcc.Input(
                                                        id=f"input-Total Charges", 
                                                        type="number",
                                                        className="width-100"
                                                    )
                                        ]), lg=3, className="bottom16")
                                ])
                        ], className="style-input-cards", style={"maxHeight":"156px"})
                    ], lg=6)
                ]
            )),
        ], className="bottom32"),
    ], className="bottom32")



@app.callback(
    Output("collapse-inputs", "is_open"),
    Input("load-more-button", "n_clicks"),
    Input("btn-predict", "n_clicks"),
    State("collapse-inputs", "is_open"),
)
def toggle_left(n, btn_pred, is_open):
    ctx = dash.callback_context

    if not ctx.triggered:
        raise PreventUpdate
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if button_id == "load-more-button":
        return not is_open

    elif button_id == "btn-predict":
        if is_open==True:
            return False
        else: 
            return dash.no_update
    return is_open


@app.callback(
    Output("prediction-result", "children"),
    Output("alert-empty-inputs", "is_open"),
    Input("btn-predict", 'n_clicks'),
    [State(f"input-{input}", 'value') \
        for input in project_list \
            if input not in ["CustomerID", "City", "Churn Value"]],
    prevent_initial_call=True)
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
        return dash.no_update, True

    else: 

        time.sleep(2)

        user_new_input = create_input_table(all_inputs)

        predictions=prediction(user_new_input)

        will_churn="The model prediction is that this customer has a high chance to Churn this time."
        will_no_churn="The model prediction is that this customer has a low chance to Churn and will not Churn this time."

        return  dbc.Alert(f"{will_churn if int(predictions['Label'][0]) == 1 else will_no_churn}", className="alert-card-style"), False
  
