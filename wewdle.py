import dash
from dash.dependencies import Input, Output, State
from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
import pandas as pd
from pandas import DataFrame
import plotly.graph_objects as go

users = [
    {'label': 'Adam', 'value': 'adam'},
    {'label': 'Alex J', 'value': 'alexj'},
    {'label': 'Alex T', 'value': 'alext'},
    {'label': 'Brady', 'value': 'brady'},
    {'label': 'Jordan', 'value': 'jordan'},
    {'label': 'Julian', 'value': 'julian'},
    {'label': 'Krymden', 'value': 'krymden'},
    {'label': 'Max', 'value': 'max'},
    {'label': 'Mike', 'value': 'mike'},
    {'label': 'Nick', 'value': 'nick'},
    {'label': 'Randy', 'value': 'randy'},
    {'label': 'Ryan', 'value': 'ryan'},
    {'label': 'Sam', 'value': 'sam'},
    {'label': 'Tanner', 'value': 'tanner'},
    {'label': 'Tim', 'value': 'tim'},
    {'label': 'Trevor', 'value': 'trevor'}
]


df = pd.read_csv('wewdle.csv')

wordle = df[df['game'] == 'Wordle']
lewdle = df[df['game'] == 'Lewdle']

avg_wordle = sum(wordle['score']) / len(wordle)
avg_lewdle = sum(lewdle['score']) / len(lewdle)

TRACE_wordle_hist = (go.Histogram(x=wordle['score'], name='Wordle'))
TRACE_lewdle_hist = (go.Histogram(x=lewdle['score'], name='Lewdle'))

TRACE_wordle_avg = (go.Indicator(
    value=avg_wordle
    , mode='number'
    , title = {'text':'Avg Wordle'}))

TRACE_lewdle_avg = (go.Indicator(
    value=avg_lewdle
    , mode='number'
    , title = {'text':'Avg Lewdle'}))

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])

app.layout = html.Div([
    dbc.Row(
        [dbc.Col(html.Div(
            dcc.Graph(
                id='avg_wordle',
                figure={
                    'data':[TRACE_wordle_avg]
                }
            )
        )
        , width=5),
        dbc.Col(html.Div(
            dcc.Graph(
                id='histo',
                figure={
                    'data':[TRACE_lewdle_hist, TRACE_wordle_hist],
                    'layout': go.Layout({'title':'Lewdle vs Wordle',
                                        'showlegend':True})
                }
            )
        )
        , width=5)]
    ),
    dbc.Row(
        [dbc.Col(html.Div(
            dcc.Graph(
                id='avg_lewdle',
                figure={
                    'data':[TRACE_lewdle_avg]
                }
            )
        )
        , width=5),
        dbc.Col(html.Div([
            dcc.Textarea(
                id='textarea-state-example',
                value='Share Score from Wordle/Lewdle here!',
                style={'width': '100%', 'height': 200},
            ),
            dcc.Dropdown(
                id='user-dropdown',
                options=users,
                placeholder='Select your Name',
                value='select_user'),
            html.Button('Submit', id='textarea-state-example-button', n_clicks=0),
            html.Div(id='textarea-state-example-output', style={'whiteSpace': 'pre-line'})]
        )
        , width=4)]
    )
])

@app.callback(
    Output('textarea-state-example-output', 'children'),
    Input('textarea-state-example-button', 'n_clicks'),
    State('textarea-state-example', 'value'),
    Input('user-dropdown', 'value2')
)
def update_output(n_clicks, value, value2):
    if n_clicks > 0 & value2 == 'select_user':
        return 'Select a user, please!'
    if n_clicks > 0 & value2 != 'Select User':
        return 'You have entered: \n{}'.format(value)

# def update_df(n_clicks, value, user):
#     if n_clicks > 0:
#         global df 
#         split = value.loc[]
#         df = df.append(value, ignore_index=True)
#         #return df

if __name__ == '__main__':
    app.run_server(debug=True)