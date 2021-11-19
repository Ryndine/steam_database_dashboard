import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import flask
from flask.templating import render_template
import plotly.express as px
import plotly.graph_objects as go
import json
from q_functions_split import db_interface
from layouts import dashapp
# steamdb = db_interface('steamdata.db')
steamdb = db_interface('D:\steam\steamdata.db')


steamdb.set_query(text='select * from games_genres')
genres = steamdb.get_df().Genre.unique()

geojson = json.loads(open("resources\countries.geojson", 'r').read())

flaskapp = flask.Flask(__name__)
dashapp = dash.Dash(__name__, server=flaskapp, url_base_pathname='/')

@flaskapp.route('/')
def home():
    return flask.redirect(dashapp)

# dashapp.layout = html.Div([
#     html.P("maperino:"),
#     dcc.Dropdown(
#         id='genre', 
#         options=[{'value': x, 'label': x} 
#                  for x in genres],
#         value=genres[0]
#         # ,labelStyle={'display': 'inline-block'}
#     ),
#     dcc.Graph(id="choropleth"),
#     dcc.Graph(id='bar')
# ])


@dashapp.callback(
    Output("choropleth", "figure"), 
    [Input("genre", "value")])
def display_choropleth(genre):
    query = f"select * from vw_genre_ownership_by_country where genre = '{genre}';"
    steamdb.set_query(text = query)
    df = steamdb.get_df()
    max_value = df['genre_owners'].max()

    fig = px.choropleth_mapbox(
        df, 
        geojson=geojson, 
        color='genre_owners',
        locations="countrycode", 
        featureidkey="id",
        center={"lat": 0.0, "lon": 0.0}, 
        zoom=1,
        range_color=[0, max_value],
        mapbox_style='open-street-map',
        title='Owners'

    )
    fig.update_layout(
        margin={"r":0,"t":0,"l":0,"b":0},
        coloraxis_colorbar=dict(title="Owners", x=-.06)
    )
    
    return fig

@dashapp.callback(
    Output("bar", "figure"), 
    [Input("genre", "value")])
def display_bargraph(genre):
    query = f"select * from vw_genre_ownership_by_country where genre = '{genre}';"
    steamdb.set_query(text = query)
    df = steamdb.get_df()
    max_value = df['genre_owners'].max()
    xval = df['countrycode']
    yval = df['genre_owners']
    # country = df['countrycode']

    fig = px.bar(
        df,
        x=xval,
        y=yval,
        log_y=True,
    )

    return fig

if __name__ == '__main__':
    flaskapp.run(host='0.0.0.0', port='8000', debug=False)
    # app.run_server(debug=True)
