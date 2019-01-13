import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import plotly.figure_factory as ff
import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd
import flask
import plotly.plotly as py
from plotly import graph_objs as go
import math
from pymongo import MongoClient
from bson.objectid import ObjectId
from app import app
import numpy as np
from datetime import datetime
from mongo import *

mPass = []
for m in range(1,13):
    mPass.append(monthPass(m))

retestDic = getErrorCount(datetime(2018,1,1),datetime(2018,12,31))
# retestDic = {'E116': 2, 'A111': 3, 'R164': 5, 'R103': 8, 'A112': 10, 'E110': 12, 'R143': 15, 'R102': 18, 'J80': 19, 'R162': 0, 'L000': 5, 'E104': 6, 'S004': 7, 'R122': 9, 'C002': 7, 'R145': 0, 'A113': 3, 'D004': 3, 'R104': 0}
initTb = cpkinitalTable(datetime(2018,10,12),datetime(2018,10,13))[0:12]


def indicator(color, text, id_value):
    return html.Div(
        [
            html.P(
                text,
                className="twelve columns indicator_text"
            ),
            html.P(
                id = id_value,
                className="indicator_value"
            ),
        ],
        className="four columns indicator",
    )

def cpkTab():
    return html.Div([
        html.Div([
            html.Div(
                dcc.DatePickerRange(
                    id='date-picker',
                    start_date=datetime.now()-relativedelta(months=1),
                    end_date_placeholder_text='End Date',
                ),
                className="two columns",
                style={'width': '18%'}
            ),

            html.Div(
                dcc.Dropdown(
                    id="db_dropdown",
                    options=getdbList(),
                    placeholder='Select DataBase',
                    value="",
                    clearable=False,
                ),
                className="two columns",
                # style={'width': '70%'}
            ),

            html.Div(
                dcc.Dropdown(
                    id="collection_dropdown",
                    options=getcollectionList(),
                    placeholder='Select Collection',
                    value="",
                    clearable=False,
                ),
                className="two columns",
                # style={'width': '70%'}
            ),
        ],
        className="row",
        style={"marginBottom": "10"},
        ),
        html.Div([
            html.Div(
                [
                    html.P("Leads count per state"),
                    dcc.Graph(
                        id='displot',
                        style={"height": "90%", "width": "98%"},
                        figure=ff.create_distplot([np.random.randn(100),np.random.randn(100)], ['2018','2019'], bin_size=.5),
                        config=dict(displayModeBar=False)
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
                            labels=list(retestDic.keys()),
                            values=list(retestDic.values()),
                            marker={"colors": ["#264e86", "#0074e4", "#74dbef", "#eff0f4"]},
                            )], layout=dict(margin=dict(l=0, r=0, t=0, b=65), legend=dict(orientation="h")))
                    ),
                ],
                className="four columns chart_div"
            ),

            html.Div(
                [
                    html.P("Leads count per state"),
                    dcc.Graph(
                        id="map",
                        style={"height": "80%", "width": "80%"},
                        config=dict(displayModeBar=False),
                        figure=dict(
                            data=[go.Bar(
                            x=mPass,
                            y=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'],
                            name= 'SF',
                            orientation = 'h'
                        )],
                        layout=dict(barmode='stack',margin=dict(l=100,r=25,b=20,t=0,pad=4),paper_bgcolor='white',plot_bgcolor='white')
                        )
                    ),
                ],
                className="four columns chart_div"
            ),

            html.Div(
                id="leads_table",
                className="row",
                children=[df_to_table(initTb)],
                style={
                    "maxHeight": "400px",
                    "overflowY": "scroll",
                    "padding": "10",
                    "marginTop": "5",
                    "backgroundColor":"white",
                    "border": "1px solid #C8D4E3",
                    "borderRadius": "3px"
                },
            ),
        ])
    ])

def df_to_table(df):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in df.columns])] +
        
        # Body
        [
            html.Tr(
                [
                    html.Td(df.iloc[i][col])
                    for col in df.columns
                ]
            )
            for i in range(len(df))
        ]
    )

