import pandas as pd
import dash
from dash import Dash, html, dcc, callback, Output, Input, dash_table, no_update
import plotly.express as px
import dash_bootstrap_components as dbc

# Registration of the page and creation of the URL path.
dash.register_page(__name__, path='/mapping')

# Creating the page layout.
layout = html.Div([

    # dcc.Store is used to store data on the browser side.
    # We use it to pass data between callbacks without reloading.
    dcc.Store(id='storage'),

    # dcc.Loading is a component that displays a loading spinner,
    dcc.Loading(id='loading', className='h-100', type='cube', children=[ 

        # Main row for the graph container.
        dbc.Row( children=[
            dbc.Col(id='graph-container', width=12),
        ]),
       ]
    ),
]),


# Callback that generates the graph based on data.
# Output: 'graph-container', which is the element where the graph will be displayed.
# Input: 'storage', which is the data from dcc.Store memory.
@callback(
    Output('graph-container', 'children'),
    Input('storage', 'data'),
)
def create_graph(data):

    # Checking if data has been passed.
    if data:
        # Converting data from dcc.Store to a Pandas DataFrame.
        df = pd.DataFrame(data)
        
        # Creating a scatter map chart.
        fig = px.scatter_map(
            df, 
            lon='lon', 
            lat='lat', 
            color='region', 
            size='loan_amount', 
            zoom=7, 
            size_max=40,
            title='Distribution of Loan Amounts Among Regions', 
            height=500
        )
        # Setting a unified background color for the chart.
        fig.update_layout(paper_bgcolor='#F0F0F0')

        # Creating a row containing the chart.
        # dbc.Col with a width of 12 makes the chart take up the full column width.
        row = dbc.Row(className='mt-3', children=[
                dbc.Col(dcc.Graph(id='graph', className='w-100', figure=fig), width=12),
            ]),
        return row
    
    # Returning 'no_update' if there is no data. This prevents errors and unnecessary updates.
    return no_update
