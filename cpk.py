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
        dcc.DatePickerRange(
            id='date-picker',
            start_date=datetime.now()-relativedelta(months=1),
            end_date_placeholder_text='Select a date!'
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
                            labels=['a','b','c','d','e','f'],
                            values=[2,3,5,7,10,8],
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
                        style={"height": "90%", "width": "98%"},
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
    	        style={
    	            "maxHeight": "300px",
    	            "overflowY": "scroll",
    	            "padding": "4",
    	            "marginTop": "10",
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

