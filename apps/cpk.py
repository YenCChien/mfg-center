import dash, dash_table
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import plotly.figure_factory as ff
from dateutil.relativedelta import relativedelta
import pandas as pd
import dash_cytoscape as cyto
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

mPass = []
for m in range(1,13):
    mPass.append(monthPass(m))

retestDic = getErrorCount(datetime(2018,10,10),datetime(2018,10,13))
eCodeReference = pd.read_csv(os.path.join(os.getcwd(),'MFG Test Script Error Code_20181015.csv'))
# retestDic = {'E110': 98, 'E104': 3, 'J80': 4, 'Others': 64, 'E120': 16, 'E108': 14, 'C002': 3, 'E102': 1}
# initTb = cpkinitalTable(datetime(2018,10,13),datetime(2018,10,14))

# print(initTb)

def modal():
    return html.Div(
        html.Div(
            [
                html.Div(
                    [   
                        # modal header
                        html.Div(
                            [
                                html.Span(
                                    "Error Code",
                                    style={
                                        "color": "#506784",
                                        "fontWeight": "bold",
                                        "fontSize": "20",
                                    },
                                ),
                                html.Span(
                                    "×",
                                    id="leads_modal_close",
                                    n_clicks=0,
                                    style={
                                        "float": "right",
                                        "cursor": "pointer",
                                        "marginTop": "0",
                                        "marginBottom": "17",
                                    },
                                ),
                            ],
                            className="row",
                            style={"borderBottom": "1px solid #C8D4E3"},
                        ),

                        # modal form
                        html.Div(
                            [
                                dash_table.DataTable(
                                id='table',
                                columns=[{"name": i, "id": i} for i in eCodeReference.columns],
                                data=eCodeReference.to_dict("rows"),
                            )]
                        )
                    ],
                    className="modal-content",
                    style={"textAlign": "center"},
                )
            ],
            className="modal",
        ),
        id="leads_modal",
        style={"display": 'none'},
    )

layout = [
    html.Div([
        html.Div([
            html.Div(
                dcc.Dropdown(
                    id="db_dropdown",
                    options=getdbList(),
                    placeholder='All DataBase',
                    value="",
                    clearable=False,
                    # disabled=True
                ),
                className="two columns",
                style={'width': '10%'}
            ),

            html.Div(
                dcc.Dropdown(
                    id="collection_dropdown",
                    options=getcollectionList(),
                    placeholder='All Collection',
                    value="",
                    clearable=False,
                    # disabled=True
                ),
                className="two columns",
                style={'width': '10%'}
            ),

            html.Div(
                dcc.DatePickerRange(
                    id='date-picker',
                    start_date=datetime(2018,11,12),
                    end_date_placeholder_text='End Date',
                    updatemode='singledate'
                ),
                className="two columns",
                style={'width': '18%','float':'right'}
            ),

            html.Div(
                html.Span(
                    "Error Code",
                    id="new_case",
                    n_clicks=0,
                    className="button button--primary add",
                ),
                className="two columns",
                style={"float": "right"},
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
        ],
        className="row",
        style={"marginTop": "5"},
        ),
        html.Div(
            id="leads_table",
            className="row",
            children=[df_to_table(cpkinitalTable(datetime(2018,10,12),datetime(2018,10,13),'1521900003T0','DsQAM'))],
            style={
                "maxHeight": "550px",
                "overflowY": "scroll",
                "padding": "10",
                "marginTop": "5",
                "backgroundColor":"white",
                "border": "1px solid #C8D4E3",
                "borderRadius": "3px"
            },
        ),
        modal(),
        html.Div([
            html.Div(
                cyto.Cytoscape(
                    id='HT_T101',
                    layout={'name': 'preset'},
                    style={'width': '50%', 'height': '300px'},
                    stylesheet=[
                        {
                            'selector': 'node',
                            'style': {'content': 'data(label)'}
                        },
                        {
                            'selector': '.countries',
                            'style': {'width': 5}
                        },
                        {
                            'selector': '.cities',
                            'style': {'line-style': 'dashed'}
                        }
                    ],
                    elements=[
                        # Parent Nodes
                        {
                            'data': {'id': 'us', 'label': 'HT_T101'}
                        },

                        # Children Nodes
                        {
                            'data': {'id': '1', 'label': '1', 'parent': 'us'},
                            'position': {'x': 100, 'y': 200}
                        },
                        {
                            'data': {'id': '2', 'label': '2', 'parent': 'us'},
                            'position': {'x': 150, 'y': 200}
                        },
                        {
                            'data': {'id': '3', 'label': '3', 'parent': 'us'},
                            'position': {'x': 200, 'y': 200}
                        },
                        {
                            'data': {'id': '4', 'label': '4', 'parent': 'us'},
                            'position': {'x': 250, 'y': 200}
                        },
                        {
                            'data': {'id': '5', 'label': '5', 'parent': 'us'},
                            'position': {'x': 300, 'y': 200}
                        },
                        {
                            'data': {'id': '6', 'label': '6', 'parent': 'us'},
                            'position': {'x': 350, 'y': 200}
                        },
                        {
                            'data': {'id': '7', 'label': '7', 'parent': 'us'},
                            'position': {'x': 400, 'y': 200}
                        },
                        {
                            'data': {'id': '8', 'label': '8', 'parent': 'us'},
                            'position': {'x': 450, 'y': 200}
                        },

                        # Edges
                        # {
                        #     'data': {'source': '1', 'target': '2'},
                        #     'classes': 'countries'
                        # },
                        # {
                        #     'data': {'source': '2', 'target': '3'},
                        #     'classes': 'countries'
                        # },
                        # {
                        #     'data': {'source': '3', 'target': '4'},
                        #     'classes': 'countries'
                        # },
                        # {
                        #     'data': {'source': '4', 'target': '5'},
                        #     'classes': 'countries'
                        # },
                        # {
                        #     'data': {'source': '4', 'target': '5'},
                        #     'classes': 'countries'
                        # },
                        # {
                        #     'data': {'source': '4', 'target': '5'},
                        #     'classes': 'countries'
                        # },
                        # {
                        #     'data': {'source': '4', 'target': '5'},
                        #     'classes': 'countries'
                        # },
                    ]
                )
            )
        ]),
    ])
]

