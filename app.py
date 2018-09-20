# -*- coding: utf-8 -*-
import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
from datetime import datetime
import pandas as pd
import flask
import plotly.plotly as py
from plotly import graph_objs as go
import math

app = dash.Dash()

app.layout = html.Div(
    [
        # header
        html.Div([
            html.Span("D70-MFG Center", className='app-title'),
            # html.Div(
            #     html.Img(src='https://github.com/YenCChien/mfg-center/blob/master/img/logo.png',height="100%")
            #     ,style={"float":"right","height":"100%"})
            ],
            className="row header"
            ),
        # tabs
        html.Div([
            dcc.Tabs(
                id="tabs",
                style={"height":"20","verticalAlign":"middle"},
                children=[
                    dcc.Tab(label="A", value="a_tab"),
                    dcc.Tab(label="AFI", value="afi_tab"),
                    dcc.Tab(id="cases_tab",label="B", value="b_tab"),
                ],
                value="afi_tab",
            )
            ],
            className="row tabs_div"
            ),
        
        # Tab content
        html.Div(id="tab_content", className="row", style={"margin": "2% 3%"}),
        html.Link(href="https://use.fontawesome.com/releases/v5.2.0/css/all.css",rel="stylesheet"),
        html.Link(href="https://cdn.rawgit.com/plotly/dash-app-stylesheets/2d266c578d2a6e8850ebce48fdb52759b2aef506/stylesheet-oil-and-gas.css",rel="stylesheet"),
        html.Link(href="https://fonts.googleapis.com/css?family=Dosis", rel="stylesheet"),
        html.Link(href="https://fonts.googleapis.com/css?family=Open+Sans", rel="stylesheet"),
        html.Link(href="https://fonts.googleapis.com/css?family=Ubuntu", rel="stylesheet"),
        html.Link(href="https://cdn.rawgit.com/amadoukane96/8a8cfdac5d2cecad866952c52a70a50e/raw/cd5a9bf0b30856f4fc7e3812162c74bfc0ebe011/dash_crm.css", rel="stylesheet")
    ],
    className="row",
    style={"margin": "0%"},
)

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

def afiTab():
    return html.Div([
            dcc.DatePickerRange(
                id='date-picker-range',
                start_date=datetime.now(),
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
                "Conversion Rates",
                "right_leads_indicator",
            ),

            ])
        ])

@app.callback(Output("tab_content", "children"), [Input("tabs", "value")])
def render_content(tab):
    if tab == "a_tab":
        return 'No Content'
    elif tab == "b_tab":
        return 'No Content'
    elif tab == "afi_tab":
        return afiTab()
    else:
        return opportunities.layout

if __name__ == "__main__":
    app.run_server(debug=True)