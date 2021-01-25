from python.data import Data
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import dash
import dash_table
from dash_table.Format import Format, Group, Scheme
import dash_table.FormatTemplate as FormatTemplate
from datetime import datetime as dt
from app import app
from dash.dependencies import Input, Output

data = Data()
data.get_data()

#################
# preprocessing #
#################
data.df = data.df.assign(date_bis=pd.to_datetime(data.df['date']))
data.df = data.df.assign(year=data.df['date_bis'].dt.year)
data.df = data.df.assign(week=data.df['date_bis'].apply(lambda x: x.isocalendar()[1]))
data.df = data.df.assign(crime=1)
data.df = data.df.assign(month_year=data.df['date_bis'].dt.strftime('%y%m'))
data.df = data.df.loc[data.df["month_year"] != '2006']


# Callbacks

@app.callback(
    # Output('intermediate-value', 'children'),
    Output('intermediate-value', 'children'),
    Input('my-range-slider', 'value'),
    Input('demo-dropdown', 'value'))
def filter_data(value_sl, value_dd):
    # an expensive query step

    print(value_sl)
    print(value_dd)
    df = Data.filter_df(data.df, years_vals=value_sl, race=value_dd)

    return df.to_json(date_format='iso', orient='split')


@app.callback(
    Output('data_display', 'children'),
    Input('intermediate-value', 'children'))
def print_shape(dfjson):
    # an expensive query step

    df = pd.read_json(dfjson, orient='split')
    print(df.shape)

    return "lines nb: {0:2.0f}".format(df.shape[0])
