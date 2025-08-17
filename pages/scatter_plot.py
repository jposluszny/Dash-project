import pandas as pd
import dash
from dash import Dash, html, dcc, callback, Output, Input, dash_table, no_update
import plotly.express as px
import dash_bootstrap_components as dbc

# Register the page and create url
dash.register_page(__name__, path='/scatter-plot')


# Create layout
layout = html.Div([

    # Create a storage component to store JSON data in the client's browser session.
    dcc.Store(id='storage'),

    # Define the spinner, the dropdown and the charts.
    dcc.Loading(id='loading', className='h-100',type='cube', children=[ 
        dbc.Row(children=[
            dbc.Col(className='col-12', children=[
                dcc.Dropdown(
                    id='dropdown',
                    options=['Agriculture'],
                    className='w-100', 
                    placeholder='Select sector ...',
                    value='Agriculture'
                ),
        ]),

            dbc.Row(className='m-4', children=[
                dbc.Col(dcc.Graph(id='scatter-plot', figure={}), className='col-md-6'),
                dbc.Col(dcc.Graph(id='pie-chart', figure={}), className='col-md-6'),
        ]),
       ]
    ),
]),
]),

# Callback to dynamically update dropdown options based on the data
@callback(
    Output('dropdown', 'options'),
    Input('storage', 'data')
)
def update_dropdown_options(data):
    """
    Updates the options in the dropdown menu based on the unique sectors in the DataFrame.
    The data is retrieved from the dcc.Store component.
    """

    if data:
        df = pd.DataFrame(data)            
        return [{'label': i, 'value': i} for i in df['sector'].unique()]
    return no_update

# Callback to update the scatter plot
@callback(
    Output('scatter-plot', 'figure'),
    Input('storage', 'data'),
    Input('dropdown', 'value'),
)
def update_scatter_plot(data, value):
    """
    Updates the scatter plot based on the selected sector from the dropdown.
    - `data`: The DataFrame from the dcc.Store.
    - `value`: The selected sector value from the dropdown.
    The plot shows funded amount vs lender count, colored by the day of the week.
    """

    if data and value:
        df = pd.DataFrame(data)
        dff = df[df.sector == value]
        fig = px.scatter(dff, x='funded_amount', y='lender_count', labels={
                     'funded_amount': 'Funded Amount',
                     'lender_count': 'Lender Count'},
            title=f'Funded Amount vs Lender Count for {value} sector', color='day')
        return fig
    return no_update

# Callback to update the pie chart
@callback(
    Output('pie-chart', 'figure'),
    Input('storage', 'data'),
    Input('dropdown', 'value'),
)
def update_pie_chart(data, value):
    """
    Updates the pie chart based on the selected sector from the dropdown.
    - `data`: The DataFrame from the dcc.Store.
    - `value`: The selected sector value from the dropdown.
    The chart shows the distribution of funded amounts by the day of the week.
    """

    if data and value:
        df = pd.DataFrame(data)
        dff = df[df.sector == value]
        fig = px.pie(dff, names='day', values='funded_amount', 
            title=f'Funded Amount vs Day for {value} sector')
        return fig
    return no_update
