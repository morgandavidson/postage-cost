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
    return html.Div(
        children=[
            dcc.Markdown('Select country of destination'),
            dcc.Dropdown(id='destinations_out'

            )
        ]
    )

# Letter type

def letter_func():

    return html.Div(
        children=[
            dcc.Markdown('Select letter type'),
            dcc.Dropdown(
                id='letter_out'
            )
        ]
    )

# Deployment

server = app.server

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

# letter type options

@app.callback(
    Output('letter_out', 'options'),
    Output('letter_out', 'value'),
    Input('origin_div', 'value')	    
)
def letter_type_options(path):
    df = pd.read_csv(path)
    valuevalues = list(df.columns.values)
    valuevalues.remove('Destination')
    valuevalues.remove('Max_weight')
    del valuevalues[len(valuevalues)-1]
    labelvalues = [v.replace('_', ' ') for v in valuevalues]
    l = [{'label':i,'value':j} for i,j in zip(labelvalues, valuevalues)]
    return l, list(l[1].values())[1]

# Destinations options

@app.callback(
    Output('destinations_out', 'options'),
    Output('destinations_out', 'value'),
    Input('origin_div', 'value')	    
)
def destination_options(path):
    df = pd.read_csv(path)
    return [{'label': i, 'value': i} for i in df['Destination'].drop_duplicates()], df['Destination'].drop_duplicates()[0]

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
    Input('origin_div','value'),
    Input('weightoutput_div', 'children'),
    Input('destinations_out', 'value'),
    Input('letter_out', 'value')
)
def cost(origin_div, weightoutput, destination_div, letter_out):
    df = pd.read_csv(origin_div)
    x = df[df['Max_weight'] == df.loc[df['Max_weight']>=weightoutput,'Max_weight'].min()].loc[df['Destination']==destination_div][letter_out].item()
    return ('Cost is {}'.format(x))

# Main

if __name__ == '__main__':
    app.run_server(debug=True)
