# -*- coding: utf-8 -*-
import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import plotly.figure_factory as ff
import dash_html_components as html
from datetime import datetime
import pandas as pd
import flask

server = flask.Flask(__name__)
app = dash.Dash(__name__,server=server)
app.config.suppress_callback_exceptions = True

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
