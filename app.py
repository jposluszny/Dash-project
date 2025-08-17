import pandas as pd
import dash
from dash import Dash, html, dcc, callback, Output, Input, dash_table, no_update
import plotly.express as px
import dash_bootstrap_components as dbc

# Initialize the app with a Dash Bootstrap theme and external stylesheets
external_stylesheets = [dbc.themes.CERULEAN, 'styles.css']
app = Dash(__name__, use_pages=True, external_stylesheets=external_stylesheets)

# Variable used for deployment
server = app.server

path = 'assets/data.csv'

# Read the csv file and create data frame
df = pd.read_csv(path)

# Create a navigation bar using Bootstrap components
navbar = dbc.NavbarSimple(
    children=[

        # Generate navigation links for each registered page
        dbc.NavItem(dbc.NavLink(f'{page["name"]}', href=page['relative_path']))
        for page in dash.page_registry.values()
    ],
    color='primary',
    dark=True,
)

# App layout, including the navigation bar and a container for subpages
app.layout = html.Div(children=[

    # Create a storage component to store JSON data in the client's browser session.
    dcc.Store(id='storage', storage_type='session'),

    # Get the current URL, used to trigger callback to load data to client's browser
    # regardless the url
    dcc.Location(id='url', refresh=False),

    # Add the navbar to the layout
    navbar,

    # This is where the content of the individual pages will be rendered
    dbc.Container([
        dbc.Row([
            dash.page_container
        ], className='mt-3'),
    ]),
])

@callback(
    Output('storage', 'data'), 
    Input('url', 'pathname'))
def load_data_to_store(value):
    ''' Stores data in the client's browser session. '''

    return df.to_dict('records')

if __name__ == '__main__':
    app.run(debug=True)
