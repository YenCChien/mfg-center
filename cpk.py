import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
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
            start_date=datetime.datetime.now()-relativedelta(months=1),
            end_date_placeholder_text='Select a date!'
        ),
    html.Div([
        html.Div(
	        id="leads_table",
	        className="row",
	        style={
	            "maxHeight": "600px",
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

