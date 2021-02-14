from python.data import Data
import pandas as pd
from app import app
from dash.dependencies import Input, Output
from assets.plots_style import *
import plotly.express as px
from assets.heatmap import get_heatmap

data = Data()
data.get_data()

#################
# preprocessing #
#################
data.df = Data.preprocess(data.df)


# Callbacks
@app.callback(
    # Output('intermediate-value', 'children'),
    Output('intermediate-value', 'children'),
    Output('period-print', "children"),
    Output('race-print', "children"),
    Output('victim-print', "children"),
    Input('my-range-slider', 'value'),
    Input('demo-dropdown', 'value'))
def filter_data(value_sl, value_dd):
    # an expensive query step

    df = Data.filter_df(data.df, years_vals=value_sl, race=value_dd)

    dfjson = df.to_json(date_format='iso', orient='split')
    str_period = "Period: {} -> {}".format(value_sl[0], value_sl[1])
    str_race = "Race: {}".format(value_dd)
    str_victim = "People shot: {}".format(len(df))

    return dfjson, str_period, str_race, str_victim


@app.callback(
    Output('crime-line-graph', 'figure'),
    Input('intermediate-value', 'children'))
def update_crime_line_graph(dfjson):
    # an expensive query step
    df = pd.read_json(dfjson, orient='split')

    df_crime_all = Data.groupby_df_two(df, "month_year", "race", "crime")

    fig = px.line(df_crime_all, x="month_year", y="crime", color='race', title='US Police Shooting')
    update_line_plot(fig)

    return fig


@app.callback(
    Output('pie_race', 'figure'),
    Input('my-range-slider', 'value'),
    Input('demo-dropdown', 'value'))
def update_race_pie(value_sl, value_dd):
    df = Data.filter_df(data.df, years_vals=value_sl)
    df_race = Data.value_counts_1(df, "race")

    if value_dd in df_race['race'].unique().tolist():
        pull = [0.2 if r == value_dd else 0 for r in df_race['race']]
    else:
        pull = [0 for r in df_race['race']]

    fig_race = px.pie(df_race, values='number', names='race', title="Victims race")
    update_pie_plot(fig_race)
    fig_race.update_traces(pull=pull)

    return fig_race


@app.callback(
    Output('state-map', 'figure'),
    Input('intermediate-value', 'children'))
def update_state_graph(dfjson):
    df = pd.read_json(dfjson, orient='split')
    df_state = df["state"].value_counts()
    df_state = pd.DataFrame({"state": df_state.index, "nb": df_state.values})

    fig_state = px.choropleth(locations=df_state["state"], locationmode="USA-states", color=df_state["nb"], scope="usa",
                              color_continuous_scale='Mint', height=300)

    update_map(fig_state)

    return fig_state


@app.callback(
    Output('gender-heatmap', 'figure'),
    Input('intermediate-value', 'children'))
def update_gender_heatmap(dfjson):
    df = pd.read_json(dfjson, orient='split')

    fig_heatmap = get_heatmap(df, "gender")
    update_heatmap(fig_heatmap)

    return fig_heatmap


@app.callback(
    Output('bar-age', 'figure'),
    Input('intermediate-value', 'children'))
def update_age_bar(dfjson):
    df = pd.read_json(dfjson, orient='split')
    df_age = Data.age_groups(df)
    df_age = Data.value_counts_1(df_age, "age_group")
    df_age.sort_values(by="age_group", ascending=True, inplace=True)

    fig_age = px.bar(df_age, x='age_group', y='number', title='Victims age')
    update_bar_plot(fig_age)

    return fig_age


@app.callback(
    Output('armed-pie', 'figure'),
    Input('intermediate-value', 'children'))
def update_armed_pie(dfjson):
    df = pd.read_json(dfjson, orient='split')
    df_armed = Data.value_counts_1(df, "armed")
    fig_armed = px.pie(df_armed, values='number', names='armed', title='Victim weapon')
    update_pie_plot(fig_armed)
    fig_armed.update_layout(
        paper_bgcolor="#212121",
        plot_bgcolor="#212121")

    return fig_armed


@app.callback(
    Output('taser-text', 'children'),
    Output('bodycam-text', 'children'),
    Input('intermediate-value', 'children')
)
def get_intervention_info(dfjson):
    df = pd.read_json(dfjson, orient='split')
    pc_taser = df["manner_of_death"].value_counts(-1).loc["shot and Tasered"] * 100
    pc_body_cam = df["body_camera"].value_counts(-1).loc[True] * 100

    str_taser = "Taser has been used for {0:2.0f}% of the deaths".format(pc_taser)
    str_bodycam = "{0:2.0f}% of the policemen wore a body camera".format(pc_body_cam)

    return str_taser, str_bodycam


@app.callback(
    Output('illness-text', 'children'),
    Output('threat-text', 'children'),
    Output('flee-text', 'children'),
    Input('intermediate-value', 'children')
)
def get_victim_behavior(dfjson):
    df = pd.read_json(dfjson, orient='split')
    pc_mental_illness = df["signs_of_mental_illness"].value_counts(-1).loc[True] * 100
    pc_attack = df["threat_level"].value_counts(-1).loc["attack"] * 100
    pc_flee_car = df["flee"].value_counts(-1).loc["Car"] * 100
    pc_flee_foot = df["flee"].value_counts(-1).loc["Foot"] * 100

    str_illness = "{0:2.0f}% of the victims presented some signs of mental illness".format(pc_mental_illness)
    str_threat = "{0:2.0f}% of them were attacking the police".format(pc_attack)
    str_flee = "{0:2.0f}% of the victims were trying to flee by car{0:2.0f}% or by foot {0:2.0f}%" \
        .format(pc_flee_car + pc_flee_foot, pc_flee_car, pc_flee_foot)

    return str_illness, str_threat, str_flee


"""

    ########
    # Test #
    ########
    @app.callback(
        Output('table', 'data'),
        Output('table', 'columns'),
        Input('intermediate-value', 'children'))


def update_table(dfjson):
    df = pd.read_json(dfjson, orient='split')

    df_bis = Data.groupby_df_one(df, "month_year", "crime")
    l_col = df_bis.columns

    data = df_bis.to_dict('records')
    columns = [{'id': c, 'name': c} for c in l_col]

    return data, columns


"""
