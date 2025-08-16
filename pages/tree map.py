import pandas as pd
import dash
from dash import Dash, html, dcc, callback, Output, Input, dash_table, no_update
import plotly.express as px
import dash_bootstrap_components as dbc

# Register the page and create url
dash.register_page(__name__, path='/tree-map')

# Create layout
layout = html.Div([
    dcc.Store(id='storage'),
    dbc.Row(id='hidden-div', children=[
        ]),

    # Display a loading spinner and graphs.
    dcc.Loading(id='loading', className='h-100',type='cube', children=[ 
        # Main row for the graph container, spanning the full width
        dbc.Row(className='m-4', children=[
            dbc.Col(id='graphs-container', width=12),
        ]),
       ]
    ),
]),


@callback(
    Output('graphs-container', 'children'),
    Input('storage', 'data'),
    Input('hidden-div', 'children'),
)
def create_graphs(data, value):
    """
    Creates Sunburst and Treemap charts based on the data.
    The data is loaded from dcc.Store.
    """
    if data:
        # The data is already a DataFrame, no need to convert from JSON
        df = pd.DataFrame(data)
        
        # Create a Sunburst chart
        # This shows the hierarchical distribution of loan amounts by region and sector.
        fig1 = px.sunburst(df, 
                           path=['region', 'sector'], 
                           values='loan_amount',
                           title='Distribution of Loan Amounts by Region and Sector',
                           height=500
                          )
        # Set a unified background color for the chart
        fig1.update_layout(paper_bgcolor='#F0F0F0')

        
        # Create a Treemap chart
        # This shows the hierarchical distribution of funded amounts by region and sector.
        fig2 = px.treemap(df, 
                          path=['region', 'sector'], 
                          values='funded_amount',
                          title='Distribution of Funded Amounts by Region and Sector',
                          height=500
                         )

        # Set a unified background color for the chart
        fig2.update_layout(paper_bgcolor='#F0F0F0')

        # Arrange the charts within rows and columns for a clean layout
        row = dbc.Row(children=[
            dbc.Row(children=[
                dbc.Col(dcc.Graph(id='graph1', className='w-100', figure=fig1), width=12),
            ]),
            dbc.Row(className='mt-3', children=[
                dbc.Col(dcc.Graph(id='graph2', className='w-100', figure=fig2), width=12),
            ]),
        ])
        return row
    return no_update
