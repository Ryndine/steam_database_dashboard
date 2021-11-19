
from dash_bootstrap_components._components.CardBody import CardBody
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from app import app
import plotly.express as px
from q_functions_split import db_interface
from dash.dependencies import Input, Output
import json

# Data
# steamdb = db_interface('steamdata.db')
steamdb = db_interface('D:\steam\steamdata.db')


steamdb.set_query(text='select * from games_genres')
genres = steamdb.get_df().Genre.unique()

geojson = json.loads(open("resources\countries.geojson", 'r').read())

# Styles & Colors

# NAVBAR_STYLE = {
#     "position": "fixed",
#     "top": 0,
#     "left": 0,
#     "bottom": 0,
#     "width": "8rem",
#     "padding": "2rem 1rem",
#     "background-color": "#f8f9fa",
# }

CONTENT_STYLE = {
    "top":0,
    "margin-top":'2rem',
    "margin-left": "2rem",
    "margin-right": "2rem",
}

# Auxiliary Components Here

options = [{'value': x, 'label': x} for x in genres]
# items = [dbc.DropdownMenuItem(i) for i in options] #remove curly brackets on this line

dropdown = dbc.Row(
    [
        dbc.Col(dcc.Dropdown(
            id='genre', 
            options=[{'value': x, 'label': x} 
                    for x in genres],
            value=genres[0]
            ),
        ),
    ],
    no_gutters=True,
)

def nav_bar():
    """
    Creates Navigation bar
    """
    navbar = dbc.Navbar(
        [
            html.A(
                dbc.Row(
                    [
                        # dbc.Col(html.Img(src=PLOTLY_LOGO, height='30px')),
                        dbc.Col(dbc.NavbarBrand('Steam Analysis Dashboard', className='ml-2')),
                    ],
                    align='center',
                    no_gutters=True,
                ),
            ),
            dbc.Col(dropdown, id="navbar-collapse"
            ),
        ],
        color="dark",
        dark=True,
    )   
    return navbar

# Graph 1 - Choropleth Map
@app.callback(
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
        height=225
    )
    fig.update_layout(
        margin={"r":0,"t":0,"l":0,"b":0},
        coloraxis_colorbar=dict(title=" ")
    )
    
    return fig

# Graph 2 - Country Bar Graph
@app.callback(
    Output("bar", "figure"), 
    [Input("genre", "value")])

def display_bargraph(genre):
    query = f"select * from vw_genre_ownership_by_country where genre = '{genre}';"
    steamdb.set_query(text = query)
    df = steamdb.get_df()
    
    xval = df['countrycode']
    yval = df['genre_owners']
    # country = df['countrycode']

    fig = px.bar(
        df,
        x=xval,
        y=yval,
        log_y=True,
        height=300,
        color='genre_owners',
        color_discrete_sequence=px.colors.sequential.Plasma,
        labels=dict(genre_owners=" ")
    )

    fig.update_layout(
        margin={"r":0,"t":0,"l":0,"b":0},
        coloraxis_showscale=False
    )

    fig.update_yaxes(side="right")

    return fig

# Graph 3 - Melissa's Graph
pie_query = f"select * from vw_genre_achieve;"
steamdb.set_query(text = pie_query)
pie_df = steamdb.get_df()
pie_labels = pie_df['Genre']
pie_values = pie_df['achievements_percentages']
pie_fig = px.pie(
    pie_df, 
    values=pie_values, 
    names=pie_labels,
    height=225,
    color_discrete_sequence=px.colors.sequential.Plasma
)

pie_fig.update_traces(textposition='inside', textinfo='percent+label')

pie_fig.update_layout(
    showlegend=False,
    margin={"r":0,"t":0,"l":0,"b":0},
)

# Page Layouts
first_card = dbc.CardBody(
        [
            html.P("Video Game Sales by Country", className="card-title"),
            dcc.Graph(id="choropleth")
        ],
    ),

second_card = dbc.CardBody(
        [
            html.P("Achievement Completion by Genre", className="card-title"),
            dcc.Graph(figure=pie_fig)
        ],
    ),

third_card = dbc.CardBody(
        [
            html.P("Video Game Sales by Country", className="card-title"),
            dcc.Graph(id='bar'),
        ],
    ),

fourth_card = dbc.CardBody(
        [
            html.P("Correlations of Relationships by Genre"),
            html.Div(id="chordchart")
        ],
    ),

layout1 = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Card(first_card),
                    ],
                    width=8,
                    align = "center",
                ),
                dbc.Col(
                    [
                        dbc.Card(second_card),
                    ],
                    width=4,
                    align = "center",
                ),
            ],
            # no_gutters=True,
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Card(third_card),
                    ],   
                    width=8,
                    align = "center",
                ),
                dbc.Col(
                    [
                        dbc.Card(fourth_card),
                    ],   
                    width=4,
                    align = "center",
                ),
            ],
            # no_gutters=True,
            style={'margin-top': '25px'},
        ),
    ],
)


layout2 = html.Div(
    [
        html.H2('Page 2'),
        html.Hr(),
        dbc.Container(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.H4('Country'),
                                html.Hr(),
                                dcc.Dropdown(
                                    id='page2-dropdown',
                                    options=[
                                        {'label': '{}'.format(i), 'value': i} for i in [
                                        'United States', 'Canada', 'Mexico'
                                        ]
        ]
                                ),
                                html.Div(id='selected-dropdown')
                            ],
                            width=6
                        ),
                        dbc.Col(
                            [
                                html.H4('Fruit'),
                                html.Hr(),
                                dcc.RadioItems(
                                    id='page2-buttons',
                                    options = [
                                        {'label':'{}'.format(i), 'value': i} for i in [
                                        'Yes ', 'No ', 'Maybe '
                                        ]
                                    ]
                                ),
                                html.Div(id='selected-button')
                            ],
                        )
                    ]
                ),
            ]
        )
    ])
