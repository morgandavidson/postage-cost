# Libraries
#    - Data wrangling

import pandas as pd


# - Dashboarding

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Style

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Loading Pandas DataFrame

df = pd.read_csv('./data/OriginFrance2021.csv')
#df = pd.DataFrame.from_dict(test)
envelop_data = pd.read_csv('./data/envelop_data.csv')

# Envelop size

def envelop_func():

    return html.Div(
        children=[
            dcc.Markdown('Select envelop size'),
            dcc.Dropdown(
                id='envelop_div',
                options=[{'label': i, 'value': j} for i,j in zip(envelop_data['size'], envelop_data['weight'])],
                value=4.5
            )
        ]
    )

# Origin

def origin_func():
    return html.Div(
        children=[
            dcc.Markdown('Select country of departure'),
            dcc.Dropdown(
                id='origin_div',
                options=[{'label': 'France', 'value': './data/OriginFrance2021.csv'}],
                value='./data/OriginFrance2021.csv'
            )
        ]
    )

# Destination

def destination_func():
    #df = id='country_table'
    #path = dcc.Store(id='country_table')
    #df = pd.read_csv(path)
    #df = pd.read_csv(id='country_table')
    return html.Div(
        children=[
            dcc.Markdown('Select country of destination'),
            dcc.Dropdown(
                id='destination_div',
                options=[{'label': i, 'value': i} for i in df['Destination'].drop_duplicates()],
                value=df['Destination'].drop_duplicates()[0]
            )
        ]
    )

# Letter type (France)

def letter_func():

    return html.Div(
        children=[
            dcc.Markdown('Select letter type'),
            dcc.Dropdown(
                id='letter_div',
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
        ]
    )

# HTML Layout

app.layout = html.Div(id='root_div', className="row", children=[
      html.H3(children='Postal Cost Calculator'),
      html.Div(id='weight_div', className="three columns", children=[
          html.H6(id='dummy_div',
	      children=['Weight is ', html.Span(id='weightoutput_div'), ' grams']
	  ),
          html.Div(children='Number of sheets:'),
              dcc.Input(id='sheets_div', value=1, type='number'),
     
          html.Div(children='Sheet height in cm:'),
              dcc.Input(id='height_div', value=29.7, type='number'), ' (A4 paper height = 29.7)',
     
          html.Div(children='Sheet width in cm:'),
              dcc.Input(id='width_div', value=21, type='number'), ' (A4 paper width = 21cm)',
     
          html.Div(children='Sheet grammage in grams:'),
              dcc.Input(id='grammage_div', value=80, type='number'),
         
          html.Div(children=[envelop_func()]),
      ]),

      html.Div(id='cost_div', className="three columns", children=[
          html.H6(id='costoutput_div'),
          html.Div(children=[origin_func()]),
          html.Div(children=[destination_func()]),
          html.Div(children=[letter_func()]),
#	  html.Div(id='costoutput_div')
      ]),
   ])

# Weight

@app.callback(
    Output('weightoutput_div', 'children'),
    Input('sheets_div', 'value'),
    Input('height_div', 'value'),	 
    Input('width_div', 'value'),
    Input('grammage_div', 'value'),     
    Input('envelop_div', 'value')	    
)

def weight(sheets_div, height_div, width_div, grammage_div, envelop_div):
    x = (sheets_div * height_div * width_div * (grammage_div/10000)) + envelop_div
    return round(x+.5)
   # x = round(x+.5)
   # return ('Weight: {} grams'.format(x))

# Cost

@app.callback(
    Output('costoutput_div', 'children'),
    Input('weightoutput_div', 'children'),
    Input('destination_div', 'value'),
    Input('letter_div', 'value')
)
def cost(weightoutput, destination_div, letter_div):
    x = df[df['Max_weight'] == df.loc[df['Max_weight']>=weightoutput,'Max_weight'].min()].loc[df['Destination']==destination_div][letter_div].item()
    return ('Cost is {}'.format(x))

# Main

if __name__ == '__main__':
    app.run_server(debug=True)
