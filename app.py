import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
	html.H6("Change the value in the text box to see callbacks in action!"),
	html.Div(["Origin: ",
		dcc.Dropdown(
			id='origin',
			options=[
				{'label': 'France', 'value': './Data/OriginFrance.csv'}
			],	
			value= './Data/OriginFrance.csv'
		)
	]),
	html.Div(["Destination: ",
		dcc.Dropdown(
			id='destination',
			options=[
				{'label': 'France', 'value': 'France'},
				{'label': 'International', 'value': 'International'}
			],
			value='France'
		)
	]),
	html.Div(["Type of letter: ",
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
    html.Div(id='priceoutput'),
])


@app.callback(
    Output(component_id='priceoutput', component_property='children'),
    Input('origin', 'value'),
	Input('destination', 'value'),
	Input('lettertype', 'value')
)

def price(origin, destination, lettertype):
    df = pd.read_csv(origin)
    return df[df['Max_weight'] == df.loc[df['Max_weight']>=56,'Max_weight'].min()].loc[df['Destination']==destination][lettertype].item()
    
if __name__ == '__main__':
    app.run_server(debug=True)
