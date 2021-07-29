import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
import json

def input_components(opt_dict, column_name):
    
    if column_name not in ["Total Charges", "Monthly Charges", "Tenure Months"]:
        input_component=dbc.Col(
            html.Div([
                html.Div(column_name, className="bold"),
                dcc.Dropdown(id=f"input-{column_name}", 
                            options=[{"label":opt, "value": opt} for opt in opt_dict[column_name]])
            ]), lg=2
        )
    else:

        if "Tenure Months" == column_name:
            input_component=dbc.Col(
                html.Div([
                    html.Div(column_name, className="bold"),
                    dcc.Input(
                                id=f"input-{column_name}", type="number", placeholder="input with range",
                                min=opt_dict[column_name][0], max=opt_dict[column_name][1]
                            ),
                ]), lg=2
            )
        else:           
            input_component=dbc.Col(
                html.Div([
                    html.Div(column_name, className="bold"),
                    dcc.Input(
                                id=f"input-{column_name}", 
                                type="number"
                            )
                ]), lg=2
            )
    
    return input_component

def load_input_dict(path='assets/data/inputs_options.json'):

    # Opening JSON file
    f = open(path)

    # returns JSON object as 
    # a dictionary
    input_data = json.load(f)

    # Closing file
    f.close()

    return input_data["features"]