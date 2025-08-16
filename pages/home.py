import pandas as pd
import dash
from dash import Dash, html, dcc, callback, Output, Input, dash_table, no_update
import plotly.express as px
import dash_bootstrap_components as dbc

# Register the page and create url
dash.register_page(__name__, path='/')

# Create layout
layout = html.Div([

    # Create a storage component to store JSON data in the client's browser session.
    dcc.Store(id='storage', storage_type='session'),

    # Hidden div component used to trigger the initial data-loading callback.
    html.Div(id='hidden-div', style={'display': 'none'}),
    html.H3('Data used for this application'),

    # Display a loading spinner and the data table.
    dcc.Loading(id='loading', className='h-100', type='cube', children=[ 
            html.Div(id='table-container')
       ]
    ),
])

@callback(
    Output('table-container', 'children'), 
    Input('storage', 'data'))
def create_data_table(data):
    ''' Creates a Dash DataTable to present the data loaded from the storage. '''

    table = dash_table.DataTable(id='table', data=data, page_action='native', page_size=7, 
    style_table={'overflowX': 'auto'}, style_cell={'textAlign': 'left', 'padding': '10px'})
    return table

