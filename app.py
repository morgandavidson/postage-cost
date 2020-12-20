# Libraries
#     - Data wrangling

import pandas as pd


# - Dashboarding

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Style

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# HTML Layout

app.layout = html.Div(id='root-div',children=[
    html.H3(children='Postal Cost Calculator'),
    html.Div(id='weight-div', children=[
        html.H6(children='Weight'),

        html.Div(children='Number of sheets:'),
            dcc.Input(id='sheets', value=1, type='number'),

        html.Div(children='Sheet height in cm:'),
            dcc.Input(id='height', value=29.7, type='number'), ' (A4 paper height = 29.7)',

        html.Div(children='Sheet width in cm:'),
            dcc.Input(id='width', value=21, type='number'), ' (A4 paper width = 21cm)',

        html.Div(children='Sheet grammage in grams:'),
            dcc.Input(id='grammage', value=80, type='number'),

        html.Div(children='Envelop size:'),
            dcc.Dropdown(
                id='envelop',   
                options=[
     	            {'label': '11.4 x 16.2cm', 'value': '3.2'},
                    {'label': '11 x 22cm', 'value': '4.5'},
                    {'label': '16.2 x 22.9cm', 'value': '7.5'},
                    {'label': '22,9x32,4cm', 'value': '14.6'}
                ],
                value='4.5'
            )
    ]),
    html.Div(id='cost-div', children=[
        html.H6(children='Cost'),

        html.Div(children='Origin:'),
            dcc.Dropdown(
                id='origin',
                options=[
                    {'label': 'France', 'value': './Data/OriginFrance.csv'}
                ],
                value='./Data/OriginFrance.csv'
            ),

        html.Div(children='Destination:'),
            dcc.Dropdown(
                id='destination',
                options=[
                    {'label': 'France', 'value': 'France'},
                    {'label': 'International', 'value': 'International'}
                ],
                value='France'
            ),

        html.Div(children='Type of letter:'),
            dcc.Dropdown(
                id='lettertype',	   
                options=[
                    {'label': 'Lettre prioritaire', 'value':'Lettre_prioritaire'},
                    {'label': 'Lettre verte', 'value':'Lettre_verte'},
                    {'label': 'Lettre suivie', 'value':'Lettre_suivie'},
                    {'label': 'Ecopli', 'value':'Ecopli'},
                    {'label': 'Recommandé R1', 'value':'Recommandé_R1'},
                    {'label': 'Recommandé R2', 'value':'Recommandé_R2'},
                    {'label': 'Recommandé R3', 'value':'Recommandé_R3'}
                ],
                value='Lettre_verte'
            )


    ]),
 ])

# Main

if __name__ == '__main__':
    app.run_server(debug=True)
