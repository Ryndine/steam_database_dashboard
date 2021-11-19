import dash
import dash_bootstrap_components as dbc

#Instantiates the Dash app and identify the server
app = dash.Dash(
    __name__, 
    external_stylesheets=[dbc.themes.BOOTSTRAP], 
    external_scripts=['https://d3js.org/d3.v4.js', 'https://cdn.jsdelivr.net/npm/d3-chord@3']
    )
    
server = app.server