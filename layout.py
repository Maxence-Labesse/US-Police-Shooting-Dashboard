import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import plotly.graph_objs as go
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
import numpy as np
import dash
import dash_table
from dash_table.Format import Format, Group
import dash_table.FormatTemplate as FormatTemplate
from datetime import datetime as dt
from app import app
from python.data import Data


random_x = [100, 2000, 550]
names = ['A', 'B', 'C']


############################################

values = [1, 2, 3, 4]
label_text = ["True Positive", "False Negative", "False Positive", "True Negative"]
labels = ["TP", "FN", "FP", "TN"]
colors = ["#13c6e9", "blue", "#ff916d", "#ff744c"]

trace0 = go.Pie(
    labels=label_text,
    values=values,
    hoverinfo="label+value+percent",
    textinfo="text+value",
    text=labels,
    sort=False,
    marker=dict(colors=colors),
    insidetextfont={"color": "white"},
    rotation=90,
)

layout = go.Layout(
    title="Confusion Matrix",
    margin=dict(l=0, r=0, t=50, b=50),
    legend=dict(bgcolor="#282b38", font={"color": "#a5b1cd"}, orientation="h"),
    plot_bgcolor="#282b38",
    paper_bgcolor="#282b38",
    font={"color": "#a5b1cd"},
)

data = [trace0]

fig = go.Figure(data=data, layout=layout)

fig.update_layout(
    height=300,
    # width=400
)


#####################
# Header with logo
def get_header():
    header = dbc.Row([
        dbc.Col([

            html.H2("US Police Shooting")
        ], width={'size': 3, 'offset': 1},
            # className="h-50",
            style={'margin-top': '1%'}
        ),
        dbc.Col([
            html.Img(
                src=app.get_asset_url('flag2.png'),
                height='70 px'
            )
        ], width={'size': 3, 'offset': 3},
            style={'margin-top': '1%', 'margin-bottom': '1%'})
    ], style={'margin-top': '1%', 'margin-left': '1%', 'margin-right': '1%',
              'background-color': '#282b38'})

    return header


########################
# Navbar
def get_navbar(p='overview'):
    navbar = dbc.Row([
        dbc.Col([
            html.A(html.Button('Overview', className='btn-secondary', ),
                   href="/shooting/overview", style={'margin-top': '1%', 'margin-bottom': '1%'})
        ], width={'size': 1, 'offset': 1}),

        dbc.Col([
            html.A(html.Button('State Focus', className='btn-secondary', ),
                   href="/shooting/get_data", style={'margin-top': '1%', 'margin-bottom': '1%'})
        ], width={'size': 1, 'offset': 1})

    ], style={'margin-bottom': '1%', 'margin-left': '1%', 'margin-right': '1%',
              'background-color': '#282b38'})

    navbar_old = html.Div([
        html.Div([
            html.Ul([
                html.Li([
                    html.A(children="Overview", href="/shooting/overview")
                ], className="nav-item active"),
                html.Li([
                    html.A(children="page2", href="/shooting/get_data")
                ], className="nav-item active")
            ], className="navbar-nav mr-auto")
        ], className="collapse navbar-collapse")
    ], className='row navbar navbar-expand-lg navbar-dark bg-primary')

    return navbar


######################
# overview page
overview = html.Div([

    get_header(),

    get_navbar(),

    html.Div([
        html.Div([

            dcc.Graph(
                id='example-graph',
                style={
                    'height': 250,
                    'width': 700,
                    "margin-left": "auto",
                    "margin-right": "auto",

                },
                figure={
                    'data': [
                        {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                        {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
                    ],
                    'layout': {
                        'plot_bgcolor': '#282b38',
                        'paper_bgcolor': '#1a1c23'
                    }

                }

            )

        ],
            className='col-12'
        ),
    ], className='row'),

    html.Div([
        html.Div([html.H3("")], className='col-1'),
        html.Div([
            html.Div([
                html.Div(children=[

                    html.Div([
                        html.H4("country"),
                        dbc.Card(body=True, className="text-white ", children=[
                            html.H6("Total cases until today:", style={"color": "white"}),
                            html.H3("test", style={"color": "white"}),

                            html.H6("Total cases in 30 days:", className="text-danger"),
                            html.H3("test", className="text-danger"),

                            html.H6("Active cases today:", style={"color": "white"}),
                            html.H3("test", style={"color": "white"}),

                            html.H6("Active cases in 30 days:", className="text-danger"),
                            html.H3("test", className="text-danger"),

                            html.H6("Peak day:", style={"color": "white"}),
                            html.H3("date", style={"color": "white"}),
                            html.H6("test", style={"color": "white"})

                        ], )
                    ]),

                ], className="col-3"),

                # dcc.Graph(figure=px.pie(values=random_x, names=names))
                html.Div([
                    html.Div([
                        html.Div([
                            dcc.Graph(figure=fig)], className="col-6",
                            style={'margin-bottom': '1%'
                                   }),

                        html.Div([dcc.Graph(figure=fig)], className="col-6",
                                 style={'margin-bottom': '1%'})

                    ],
                        className="row",
                    ),

                    html.Div([
                        html.Div([
                            dcc.Graph(figure=fig)], className="col-6",
                            style={'margin-top': '1%'}),

                        html.Div([dcc.Graph(figure=fig)], className="col-6",
                                 style={'margin-top': '1%'})

                    ],
                        className="row",
                    ),

                ], className='col-9',
                    # style={'background-color': '#ABBAEA'}
                ),
            ], className='row')
        ],

            className=' jumbotron col-10', style={'background-color': '#282b38'}
        ),
        html.Div([html.H3("")], className='col-1')
    ], className='row', style={"margin-top": "1%"})

],
    # style={'background-color': '#2f3445'}
)

page2 = html.Div([

    get_header(),

    get_navbar(),

    html.Div(html.H3("test page 2")),

])

###########################
