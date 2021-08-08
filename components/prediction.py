
from dash_bootstrap_components._components.Collapse import Collapse
from dash_bootstrap_components._components.Tooltip import Tooltip
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
import numpy as np

from components.utils.generate_dropdowns import input_components, load_input_dict

from components.utils.load_data import create_input_table, data_transformation

from components.utils.load_model import prediction, test_score_report

import random 

project_list=load_input_dict().keys()

prediction_layout=html.Div(
        [
            html.H1(["IBM Customers Churn Prediction", 
                                     html.Span(html.I(className="fas fa-question-circle font-lg", 
                                                      id="tooltip-churn-info"), 
                                            style={"marginLeft":"5px", "cursor":"pointer"})],
                    className="text-center bottom32 top16"), 
            dbc.Tooltip(["Click here to get informations about what is churn prediction and the evaluation metric."], target="tooltip-churn-info"),
            # dbc.Collapse(
            #     [html.Div([
            #             html.Div([
            #                 html.H3("What Is Churn Prediction?", className="font-md bold"),
            #                 html.Div([html.B("Churn predicition")," means detecting which customers are likely to cancel a subscription to a service based on how they use the service. It is a critical prediction for many businesses because acquiring new clients often costs more than retaining existing ones. Once you can identify those customers that are at risk of cancelling, you should know exactly what marketing action to take for each individual customer to maximise the chances that the customer will remain."], className="font-sm bottom16"),
            #             ]),
            #             html.Div([html.Div("KEY TAKEAWAYS", className="bold font-md bottom8"),
            #                       html.Ul([
            #                           html.Li("To this solution we are considering the metric 'PROFIT' to detect the best model.", className="bottom8"),
            #                           html.Li(["To calculate the PROFIT metric it is considering a cost of ", 
            #                                    html.B("$1000")," to each customer predicted as CHURN and an earn ", 
            #                                    html.B("$5,000")," in CLTV for each customer correctly predicted."], className="bottom8"),
            #                           html.Li(["Model evaluation metric formula: ", html.Br(), html.B("(TRUE_POSITIVE x $5000) - ((TRUE_POSITIVE+FALSE_POSITIVE) x $1000)"), ], className="bottom8"),
            #                           html.Li("The algorithm choose was Naive Bayes", className="bottom8")
            #                       ], className="font-sm")])
            #         ], className="styleChurnExplanation")
            #     ],
            #     id="collapse-info-churn",
            #     is_open=False),
            dbc.Collapse(
                [html.Div([
                        html.Div([
                            html.H3("What Is Churn Prediction?", className="font-md bold"),
                            html.Div([html.B("Churn predicition")," means detecting which customers are likely to cancel a subscription to a service based on how they use the service. It is a critical prediction for many businesses because acquiring new clients often costs more than retaining existing ones. Once you can identify those customers that are at risk of cancelling, you should know exactly what marketing action to take for each individual customer to maximise the chances that the customer will remain."], className="font-sm bottom16"),
                        ], className="card-left-info"),
                        html.Div([html.Div("KEY TAKEAWAYS", className="bold font-md bottom8"),
                                  html.Ul([
                                      html.Li("To this solution we are considering the metric 'PROFIT' to detect the best model.", className="bottom8"),
                                      html.Li(["To calculate the PROFIT metric it is considering a cost of ", 
                                               html.B("$1000")," to each customer predicted as CHURN and an earn ", 
                                               html.B("$5,000")," in CLTV for each customer correctly predicted."], className="bottom8"),
                                      html.Li(["Model evaluation metric formula: ", html.Br(), html.B("(TRUE_POSITIVE x $5000) - ((TRUE_POSITIVE+FALSE_POSITIVE) x $1000)"), ], className="bottom8"),
                                      html.Li("The algorithm choose was Naive Bayes", className="bottom8")
                                  ], className="font-sm")], className="card-right-info")
                    ], className="styleChurnExplanation")
                ],
                id="collapse-info-churn",
                is_open=False),
            html.Div(id="customer-input-list", className="bottom32"),
            html.Div(id="input-churn-sample", className="white font-sm bottom16"),
            html.Div([html.Div([html.Button(["Predict"], 
                                            id="btn-predict", 
                                            className="buttonStyle right4"),
                                  html.Button(["Load sample"], 
                                            id="btn-collapse-load-samples", 
                                            className="buttonStyle left4"),
                                     dbc.Collapse(
                                        [html.Div([
                                            html.Button(["Load one sample"], 
                                                id="btn-load-one", 
                                                className="buttonStyle-internal left4"),
                                            html.Button(["Load full dataset"], 
                                                id="btn-load-full", 
                                                className="buttonStyle-internal left4")
                                        ], className="hidden-buttons")],
                                        id="collapse",
                                        is_open=False,
                                        ),
                                  ], className="bottom16"),
                        dcc.Store("loaded-sampled"),
                        dbc.Alert(
                            id="alert-empty-inputs",
                            is_open=False,
                            duration=5000, color="danger",
                            className="alert-card-style")], 
                    className="text-center bottom16"),
            dcc.Loading(html.Div(id="prediction-result", style={"min-height":"250px"}))
        ])


@app.callback(
    Output("collapse", "is_open"),
    [Input("btn-collapse-load-samples", "n_clicks"),
     Input("btn-load-one", "n_clicks"),
     Input("btn-predict", "n_clicks"),
     Input("btn-load-full", "n_clicks")],
    [State("collapse", "is_open")],
)
def toggle_collapse(n_collapse, loaded, predict, load_full, is_open):

    ctx = dash.callback_context

    if not ctx.triggered:
        raise PreventUpdate
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if button_id == "btn-collapse-load-samples":
        return not is_open

    elif button_id == "btn-predict":
        if is_open==True:
            return False
        else: 
            return dash.no_update

    elif button_id == "btn-load-one":
        if is_open==True:
            return False
        else: 
            return dash.no_update

    elif button_id == "btn-load-full":
        if is_open==True:
            return False
        else: 
            return dash.no_update

    return is_open


@app.callback(
    Output("customer-input-list", "children"),
    Input("dropdown-options", "data")
)
def generating_dropdowns(dropdown_data):

    return html.Div([
        html.Div([
            html.Div(dbc.Row(
                [
                    dbc.Col([
                        html.Div([
                            html.H3(["Demographic Features", 
                                     html.Span(html.I(className="fas fa-question-circle font-sm", 
                                                      id="tooltip-demographic"), 
                                            style={"marginLeft":"5px"})], className="bottom16 font-lg"),
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
                                                    value="No",
                                                    clearable=False)
                                    ]), lg=3, className="bottom16"),
                                dbc.Col(html.Div(
                                    [
                                        html.H4(["Dependents", html.Span("*", style={"color":"red"})], className="font-sm"),
                                        dcc.Dropdown(id="input-Dependents", 
                                                options=[{"label":val, "value":val} \
                                                    for val in dropdown_data["Dependents"]],
                                                    value=None,
                                                    clearable=False)
                                    ]), lg=3, className="bottom16"),
                                dbc.Col(html.Div(
                                    [
                                        html.H4("Senior Citizen", className="font-sm"),
                                        dcc.Dropdown(id="input-Senior Citizen", 
                                                    options=[{"label":val, "value":val} \
                                                        for val in dropdown_data["Senior Citizen"]], 
                                                    value="No",
                                                    clearable=False)
                                    ]), lg=3, className="bottom16")])
                            ], className="style-input-cards")
                    ], lg=6),
                    dbc.Col([
                        html.Div([
                            html.H3(["Contract settings", html.Span(html.I(className="fas fa-question-circle font-sm", id="tooltip-contract"), 
                                            style={"marginLeft":"5px"})], className="bottom16 font-lg"),
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
                                                        value=None,
                                                        clearable=False,
                                                        placeholder="Monhtly, yearly...")
                                        ]), lg=4, className="bottom16"),
                                    dbc.Col(html.Div(
                                        [
                                            html.H4("Billing Option", className="font-sm"),
                                            dcc.Dropdown(id="input-Paperless Billing", 
                                                    options=[{"label":"Paperless" if val == "Yes" else "Paper", "value":val} \
                                                        for val in dropdown_data["Paperless Billing"]],
                                                        value="Yes",
                                                        clearable=False)
                                        ]), lg=4, className="bottom16"),
                                    dbc.Col(html.Div(
                                        [
                                            html.H4("Payment Method", className="font-sm"),
                                            dcc.Dropdown(id="input-Payment Method", 
                                                    options=[{"label":val.replace("(automatic)", ""), "value":val} \
                                                        for val in dropdown_data["Payment Method"]],
                                                        value="Bank transfer (automatic)",
                                                        clearable=False)
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
                                            style={"marginLeft":"5px"})], className="bottom16 font-lg"),
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
                                                        value="Yes",
                                                        clearable=False)
                                        ]), lg=4, className="bottom16"),
                                    dbc.Col(html.Div(
                                        [
                                            html.H4("Internet Service", className="font-sm"),
                                            dcc.Dropdown(id="input-Internet Service", 
                                                        options=[{"label":val, "value":val} \
                                                            for val in dropdown_data["Internet Service"]],
                                                        value="Fiber optic",
                                                        clearable=False)
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
                                    html.Div(
                                        dbc.Row([
                                            dbc.Col(html.Div(
                                                [
                                                    html.H4("Multiple Lines", className="font-sm"),
                                                    dcc.Dropdown(id="input-Multiple Lines", 
                                                            options=[{"label":val, "value":val} \
                                                                for val in dropdown_data["Multiple Lines"]],
                                                                value="No",
                                                            clearable=False)
                                                ]), lg=3, className="bottom16"),
                                            dbc.Col(html.Div(
                                                [
                                                    html.H4("Online Security", className="font-sm"),
                                                    dcc.Dropdown(id="input-Online Security", 
                                                            options=[{"label":val, "value":val} \
                                                                for val in dropdown_data["Online Security"]],
                                                                value="No",
                                                            clearable=False)
                                                ]), lg=3, className="bottom16"),
                                            dbc.Col(html.Div(
                                                [
                                                    html.H4("Online Backup", className="font-sm"),
                                                    dcc.Dropdown(id="input-Online Backup", 
                                                            options=[{"label":val, "value":val} \
                                                                for val in dropdown_data["Online Backup"]],
                                                                value="No",
                                                            clearable=False)
                                                ]), lg=3, className="bottom16"),
                                            dbc.Col(html.Div(
                                                [
                                                    html.H4("Device Protection", className="font-sm"),
                                                    dcc.Dropdown(id="input-Device Protection", 
                                                            options=[{"label":val, "value":val} \
                                                                for val in dropdown_data["Device Protection"]],
                                                                value="No",
                                                            clearable=False)
                                                ]), lg=3, className="bottom16"),
                                            dbc.Col(html.Div(
                                                [
                                                    html.H4("Tech Support", className="font-sm"),
                                                    dcc.Dropdown(id="input-Tech Support", 
                                                            options=[{"label":val, "value":val} \
                                                                for val in dropdown_data["Tech Support"]],
                                                                value="No",
                                                            clearable=False)
                                                ]), lg=3, className="bottom16"),
                                            dbc.Col(html.Div(
                                                [
                                                    html.H4("Streaming TV", className="font-sm"),
                                                    dcc.Dropdown(id="input-Streaming TV", 
                                                            options=[{"label":val, "value":val} \
                                                                for val in dropdown_data["Streaming TV"]],
                                                                value="No",
                                                            clearable=False)
                                                ]), lg=3, className="bottom16"),
                                            dbc.Col(html.Div(
                                                [
                                                    html.H4("Streaming Movies", className="font-sm"),
                                                    dcc.Dropdown(id="input-Streaming Movies", 
                                                            options=[{"label":val, "value":val} \
                                                                for val in dropdown_data["Streaming Movies"]],
                                                                value="No",
                                                            clearable=False)
                                                ]), lg=3, className="bottom16")
                                        ]), className="extra-inputs-layout"
                                    )
                                ], id="collapse-inputs")
                            ]),
                            ], className="style-input-cards", style={"height":"100%"})
                    ], lg=6),
                    dbc.Col([
                        html.Div([
                            html.H3(["Tenure & Charges", html.Span(html.I(className="fas fa-question-circle font-sm", id="tooltip-numericals"), 
                                            style={"marginLeft":"5px"})], className="bottom16 font-lg"),
                            dbc.Tooltip(
                                "Tenure in months and Billing Charges.",
                                target="tooltip-numericals",
                            ),
                            dbc.Row(
                                [
                                    dbc.Col(html.Div(
                                        [
                                            html.H4(["Tenure Months", html.Span("*", style={"color":"red"})], className="font-sm"),
                                            dcc.Input(
                                                        id=f"input-Tenure Months", 
                                                        type="number",
                                                        className="width-100"
                                                    )
                                        ]), lg=3, className="bottom16"),
                                    dbc.Col(html.Div(
                                        [
                                            html.H4(["Monthly Charges", html.Span("*", style={"color":"red"})], className="font-sm"),
                                            dcc.Input(
                                                        id=f"input-Monthly Charges", 
                                                        type="number",
                                                        className="width-100"
                                                    )
                                        ]), lg=3, className="bottom16"),
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
def collapse_inputs(n, btn_pred, is_open):
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
    Output("alert-empty-inputs", "children"),
    Output("alert-empty-inputs", "is_open"),
    Input("btn-predict", 'n_clicks'),
    Input("btn-load-one", "n_clicks"),
    Input("btn-load-full", "n_clicks"),
    [State(f"input-{input}", 'value') \
        for input in project_list \
            if input not in ["CustomerID", "City", "Churn Value", "Total Charges"]],
    prevent_initial_call=True)
def getting_input_parameters(btn_predict, btn_load_one, btn_load_all, gender, senior_citzen, partner, \
                             dependents,tenure, phone_service, multiple_lines, internet_service,\
                             online_security, online_backup, device_protection, tech_support, \
                             streaming_tv, streaming_movies, contract, paperless_bill, payment_method, \
                             monthly_charges):

    all_inputs=["IDdummy", \
                gender, senior_citzen, partner, \
                dependents,tenure, phone_service, multiple_lines, internet_service,\
                online_security, online_backup, device_protection, tech_support, \
                streaming_tv, streaming_movies, contract, paperless_bill, payment_method, \
                monthly_charges]

    ctx = dash.callback_context

    if not ctx.triggered:
        raise PreventUpdate
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if button_id == "btn-load-one":
        return None, dash.no_update, False

    if button_id == "btn-load-full":
        
        time.sleep(5)
        
        test_df = pd.read_csv("assets/data/telco-test.csv")
        churn_vals=test_df["Churn Value"].copy()
        test_df = data_transformation(test_df)  
        predict_unseen = prediction(test_df)
        test_df["Churn Value"]=churn_vals

        score_unseen = test_score_report(test_df, predict_unseen)

        dash_result_component = html.Div([
                    f"The potential profit generated by the model in a base of ", html.B(f"{test_df.shape[0]}")," customers is ", html.B(f"${score_unseen['Profit'].values[0]:,}"), ". With a recall of ", html.B(f"{round(score_unseen['Recall'].values[0],4)*100}%")," that means that the model predicted correctly ", html.B(f"{len(np.where((test_df['Churn Value'] == 1) & (predict_unseen['Label'] == 1))[0])}"), " over ", html.B(f"{len(np.where((test_df['Churn Value'] == 1))[0])}"), " customer who left the company services."
                ], className="load-full-layout font-md"
            )

        return dash_result_component, dash.no_update, False

    else: 

        if None in all_inputs:

            user_new_input = create_input_table(all_inputs)

            list_empty=[i for i in user_new_input.columns if user_new_input[i].isnull().any()]
            
            string_list=", ".join([val for val in list_empty])

            alert_string="You can't leva empty fields. Please, fill the ", html.Span(string_list, style={"font-weight":"bold"}), " fields before clicking on Predict button again."

            return dash.no_update, alert_string, True

        time.sleep(4)

        user_new_input = create_input_table(all_inputs)

        user_new_input=data_transformation(user_new_input)

        predictions=prediction(user_new_input)

        will_churn="The model predicted that this customer will churn."
        will_no_churn="The model predicted that this customer will not churn."

        return  dbc.Alert(f"{will_churn if int(predictions['Label'][0]) == 1 else will_no_churn}", className="alert-card-style"), dash.no_update, False


@app.callback(
    [Output(f"input-{input}", 'value') \
        for input in list(project_list) \
            if input not in ["CustomerID", "City", "Churn Value", "Total Charges"]],
    [Output("loaded-sampled", "data")],
     Input("btn-load-one", "n_clicks"), prevent_initial_call=True
            )
def loading_value_from_test_data(btn_load):

    ctx = dash.callback_context

    if not ctx.triggered:
        raise PreventUpdate
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    test_df=pd.read_csv("assets/data/telco-test.csv")
    churn_label=test_df["Churn Value"].values
    unseen_data=test_df[['CustomerID', 'City', 'Gender', 'Senior Citizen', 'Partner',
              'Dependents', 'Tenure Months', 'Phone Service', 'Multiple Lines',
              'Internet Service', 'Online Security', 'Online Backup',
              'Device Protection', 'Tech Support', 'Streaming TV', 'Streaming Movies',
              'Contract', 'Paperless Billing', 'Payment Method', 'Monthly Charges']]
    
    rand_idx=random.randint(0, len(unseen_data))
    random_sample_data=unseen_data.iloc[rand_idx].tolist()
    
    return random_sample_data[2:] + [random_sample_data+[churn_label[rand_idx]]]


@app.callback(
    Output("input-churn-sample", "children"),
    [Input("loaded-sampled", "data")],
    [Input(f"input-{input}", 'value') \
        for input in project_list \
            if input not in ["CustomerID", "City", "Churn Value", "Total Charges"]],
    
    prevent_initial_call=True
)
def loaded_and_inputs(loaded_sample, gender, senior_citzen, partner, \
                             dependents,tenure, phone_service, multiple_lines, internet_service,\
                             online_security, online_backup, device_protection, tech_support, \
                             streaming_tv, streaming_movies, contract, paperless_bill, payment_method, \
                             monthly_charges):

    features_list=[gender, senior_citzen, partner, \
                             dependents,tenure, phone_service, multiple_lines, internet_service,\
                             online_security, online_backup, device_protection, tech_support, \
                             streaming_tv, streaming_movies, contract, paperless_bill, payment_method, \
                             monthly_charges]

    if None in features_list:
        raise PreventUpdate

    elif loaded_sample is None:
        raise PreventUpdate

    elif loaded_sample[2:-1] != features_list:
        return None

    else:
        text_loaded=f"The loaded sample IS A CHURN - ID sample {loaded_sample[0]}" if loaded_sample[-1] == 1 else f"The loaded sample IS NOT A CHURN - ID sample {loaded_sample[0]}"

        return html.Div(html.Div(text_loaded, className="white font-sm"), className="backgroundLoaded")


@app.callback(
    Output("collapse-info-churn", "is_open"),
    Input("tooltip-churn-info", "n_clicks"),
    State("collapse-info-churn", "is_open")
)
def collapse_info(n, is_open):
    if n:
        return not is_open
    return is_open


