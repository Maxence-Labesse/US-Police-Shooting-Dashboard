import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import plotly.express as px
from app import app
from python.data import Data
from assets.plots_style import *

years_val = [2016, 2019]
race = 'Black'

data = Data()
data.get_data()
df_raw = Data.preprocess(data.df)
df = Data.filter_df(df_raw, years_val)
df_crime_all = Data.groupby_df_one(df, "month_year", "crime")

dd_options = [{'label': i, 'value': i} for i in df["race"].unique().tolist()]
dd_options.append({'label': 'Overall', 'value': 'Overall'})

#
df_armed = Data.value_counts_1(df, "armed")
fig_armed = px.pie(df_armed, values='number', names='armed')
update_pie_plot(fig_armed)


############################################


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
        ], width={'size': 3, 'offset': 5},
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

    return navbar


######################
# overview page
overview = html.Div([

    get_header(),

    get_navbar(),

    html.Div([

        # html.Div([html.H6("")], className="col-1"),

        html.Div(children=[
            html.Div([
                html.H6("Select race:"),
                dcc.Dropdown(
                    id='demo-dropdown',
                    options=dd_options,
                    value='Overall',
                    style={'width': '100px',
                           'color': '#212121',
                           'background-color': '#212121',
                           'margin-left': '5%'
                           }
                )], className='row'),
            html.H3(),

            html.Div([
                dbc.Card(body=True, className="text-white ", children=[
                    html.H6(id="period-print", style={"color": "white"}),
                    html.H6(id="race-print", style={"color": "white"}),
                    html.H6(id="victim-print", style={"color": "white"}),
                ], style={"border": "solid #3E3F40"})
            ]),

        ], className="col-2", style={"margin-left": "5%"}),

        html.Div([

            dcc.Graph(
                id='crime-line-graph',
                style={"border": "solid #3E3F40"
                       },
            ),

            html.Div(id='intermediate-value', style={'display': 'none'}),
            html.H3(),
            html.Div([
                dcc.RangeSlider(
                    id='my-range-slider',
                    min=df_raw['year'].min(),
                    max=df_raw['year'].max(),
                    step=1,
                    value=[df_raw['year'].min(), df_raw['year'].max()],
                    marks={
                        2015: '2015',
                        2016: '2016',
                        2017: '2017',
                        2018: '2018',
                        2019: '2019',
                        2020: '2020'}
                ),
            ], style={"margin_top": "2%"})

        ],
            className='col-6'
        ),

        html.Div(children=[

            html.Div([
                dcc.Graph(id="pie_race")],
                style={"border": "solid #3E3F40"
                       })
        ], className="col-3"),

    ], className='row'),

    html.Div([
        # html.Div([html.H3("")], className='col-1'),
        html.Div([
            html.Div([
                html.Div(children=[

                    html.Div([

                        html.Div([
                            html.Div(["Intervention infos"], className="card-header"),
                            html.H6(""),
                            html.H6(id="taser-text",
                                    style={"color": "white", "margin-left": "2%", "margin-right": "2%"}),
                            html.H6(""),
                            html.H6(id="bodycam-text",
                                    style={"color": "white", "margin-left": "2%", "margin-right": "2%"}),

                        ], className="card text-white bg-primary mb-3", style={"border": "solid #3E3F40"}),

                        html.Div([
                            html.Div(["Victim behavior"], className="card-header"),
                            html.H6(""),
                            html.H6(id="illness-text",
                                    style={"color": "white", "margin-left": "2%", "margin-right": "2%"}),
                            html.H6(""),
                            html.H6(id="threat-text",
                                    style={"color": "white", "margin-left": "2%", "margin-right": "2%"}),
                            html.H6(""),
                            html.H6(id="flee-text",
                                    style={"color": "white", "margin-left": "2%", "margin-right": "2%"}),

                            html.Div([
                                dcc.Graph(id='armed-pie', style={"border": "solid #3E3F40"})], className="col-11",
                                style={'margin': 'auto', 'margin-bottom': '2%'
                                       })

                        ], className="card text-white bg-primary mb-3", style={"border": "solid #3E3F40"})

                    ]),

                ], className="col-3"),

                # dcc.Graph(figure=px.pie(values=random_x, names=names))
                html.Div([
                    html.Div([
                        html.Div([
                            dcc.Graph(id="state-map", style={"border": "solid #3E3F40"})], className="col-12")
                    ],
                        className="row",
                    ),

                    html.Div([
                        html.Div([
                            dcc.Graph(id="gender-heatmap", style={"border": "solid #3E3F40"})], className="col-5",
                            style={'margin-top': '1%', 'margin-right': '1%'}),

                        html.Div([
                            dcc.Graph(id="bar-age", style={"border": "solid #3E3F40"})], className="col-5",
                            style={'margin-top': '1%', 'margin-left': '1%'})

                    ],
                        className="row",
                    ),

                ], className='col-9',
                    # style={'background-color': '#ABBAEA'}
                ),
            ], className='row')
        ],

            className=' jumbotron col-11',
            style={'background-color': '#282b38', 'margin-left': "2%", 'margin-right': '2%'}
        ),
        # html.Div([html.H3("")], className='col-1')
    ], className='row', style={"margin-top": "1%"}),

],
    # style={'background-color': '#2f3445'}
)

page2 = html.Div([

    get_header(),

    get_navbar(),

    html.Div(html.H3("test page 2")),

])

