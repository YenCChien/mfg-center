import dash, dash_table
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import plotly.figure_factory as ff
from dateutil.relativedelta import relativedelta
import pandas as pd
import flask
import plotly.plotly as py
from plotly import graph_objs as go
import math, os
from pymongo import MongoClient
from bson.objectid import ObjectId
import numpy as np
from datetime import datetime
from mongo import *
from app import app, indicator, df_to_table

layout = [
    html.Div([
        dcc.DatePickerRange(
            id='date-picker-range',
            start_date=datetime(2018,11,12),
            end_date_placeholder_text='Select a date!'
        ),
        html.Div([
            html.Div(
                [
                    html.P("Leads count per state"),
                    dcc.Graph(
                        id="map",
                        style={"height": "90%", "width": "98%"},
                        config=dict(displayModeBar=False),
                    ),
                ],
                className="four columns chart_div"
            ),

            html.Div(
                [
                    html.P("Leads by source"),
                    dcc.Graph(
                        id="lead_source",
                        style={"height": "90%", "width": "98%"},
                        config=dict(displayModeBar=False),
                        figure=dict(data=[go.Pie(
                            labels=['a','b','c','d','e','f'],
                            values=[2,3,5,7,10,8],
                            marker={"colors": ["#264e86", "#0074e4", "#74dbef", "#eff0f4"]},
                            )], layout=dict(margin=dict(l=0, r=0, t=0, b=65), legend=dict(orientation="h")))
                    ),
                ],
                className="four columns chart_div"
            ),
            indicator(
                "#EF553B",
                "Retest Rates",
                "d_indicator",
            ),
            indicator(
                "#EF553B",
                "PASS Rates",
                "e_indicator",
            ),
            indicator(
                "#EF553B",
                "FAIL Rates",
                "f_indicator",
            ),
        ])
    ])
]