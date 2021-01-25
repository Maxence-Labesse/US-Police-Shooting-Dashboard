import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import plotly.graph_objs as go
import plotly.graph_objs as go
import plotly.express as px
from app import app
from python.data import Data
from assets.plots_style import *
import pandas as pd
from assets.heatmap import get_heatmap
from dash.dependencies import Input, Output

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
def plot_line_crimes(df):
    fig = px.line(df, x="month_year", y="crime", color='race', title='US Police Shooting')
    update_line_plot(fig)

    return fig


fig_line_crime = plot_line_crimes(df_crime_all)

#
df_state = df["state"].value_counts()
df_state = pd.DataFrame({"state": df_state.index, "nb": df_state.values})

fig_state = px.choropleth(locations=df_state["state"], locationmode="USA-states", color=df_state["nb"], scope="usa",
                          color_continuous_scale='Mint', height=300)

fig_state.update_layout(
    geo=dict(bgcolor="#21252C"),
    paper_bgcolor="#21252C",
    plot_bgcolor="#21252C")

#
df_race = Data.value_counts_1(df, "race")

if race in df_race['race'].unique().tolist():
    pull = [0.2 if r == race else 0 for r in df_race['race']]
else:
    pull = [0 for r in df_race['race']]

fig_race = px.pie(df_race, values='number', names='race')
update_pie_plot(fig_race)
fig_race.update_traces(pull=pull)

#
fig_heatmap = get_heatmap(df, "gender")
update_heatmap(fig_heatmap)

#
df_age = Data.age_groups(df)
df_age = Data.value_counts_1(df_age, "age_group")
df_age.sort_values(by="age_group", ascending=True, inplace=True)

fig_age = px.bar(df_age, x='age_group', y='number')
update_bar_plot(fig_age)

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

    return navbar


######################
# overview page
overview = html.Div([

    get_header(),

    get_navbar(),

    html.Div([

        html.Div([html.H6("")], className="col-1"),

        html.Div(children=[

            html.Div([
                dbc.Card(body=True, className="text-white ", children=[
                    html.H6("Total cases until today:", style={"color": "white"}),
                    html.H3(id='data_display', style={"color": "white"}),

                    html.H6("Total cases in 30 days:", className="text-danger"),
                    html.H3("test", className="text-danger"),

                    html.H6("Active cases today:", style={"color": "white"}),
                    html.H3("test", style={"color": "white"}),
                ], )
            ]),
        ], className="col-2"),

        html.Div([

            dcc.Graph(
                id='example-graph',
                figure=fig_line_crime,
                style={
                    # 'height': 400,
                    # 'width': 600,
                    # "margin-left": "auto",
                    # "margin-right": "auto",
                    # "margin-top": "auto",
                    # "margin-bottom": "auto",
                },
            ),

            html.Div(id='intermediate-value', style={'display': 'none'}),

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
            dcc.Dropdown(
                id='demo-dropdown',
                options=dd_options,
                value='Overall',
                style=
                {'width': '135px',
                 'color': '#212121',
                 'background-color': '#212121'}
            ),

            html.Div([
                dcc.Graph(figure=fig_race)], className="col-4",
                style={'margin-top': '1%'})
        ], className="col-1"),

    ], className='row'),

    html.Div([
        # html.Div([html.H3("")], className='col-1'),
        html.Div([
            html.Div([
                html.Div(children=[

                    html.Div([
                        html.H4("country"),

                        html.Div([
                            html.Div(["Header"], className="card-header"),
                            html.P([
                                "Some quick example text to build on the card title and make up the bulk of the card's content."],
                                className="card-text")

                        ], className="card text-white bg-primary mb-3"),

                        html.Div([
                            html.Div(["Header"], className="card-header"),
                            html.P([
                                "Some quick example text to build on the card title and make up the bulk of the card's content."],
                                className="card-text"),

                            html.Div([
                                dcc.Graph(figure=fig_armed)], className="col-8",
                                style={'margin-bottom': '1%', 'margin-right': '3%'
                                       })

                        ], className="card text-white bg-primary mb-3")

                    ]),

                ], className="col-3"),

                # dcc.Graph(figure=px.pie(values=random_x, names=names))
                html.Div([
                    html.Div([
                        html.Div([
                            dcc.Graph(figure=fig_state)], className="col-12",
                            style={'margin-bottom': '1%'
                                   })

                    ],
                        className="row",
                    ),

                    html.Div([
                        html.Div([
                            dcc.Graph(figure=fig_heatmap)], className="col-4",
                            style={'margin-top': '1%'}),

                        html.Div([""], className='col-2'),

                        html.Div([
                            dcc.Graph(figure=fig_age)], className="col-4",
                            style={'margin-top': '1%'})

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
"""
@app.callback(
    Output('intermediate-value', 'children'),
    Input('my-range-slider', 'value'),
    Input('demo-dropdown', 'value'))
def filter_data(value_sl, value_dd):
    # an expensive query step

    df = Data.filter_df(df_raw, years_vals=value_sl, race=value_dd)

    df.to_json(date_format='iso', orient='split')



@app.callback(
    Output('data_display', 'children'),
    Input('intermediate-value', 'children'))
def print_shape(dfjson):
    # an expensive query step

    df = pd.read_json(dfjson, orient='split')

    return "lines nb: {0:2.0f}".format(df.shape[0])
"""
