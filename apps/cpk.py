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
            # className="row",
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
            html.Div([
                cyto.Cytoscape(
                    id='HT_T101',
                    layout={
                        'name': 'grid',
                        'rows': '3',
                    },
                    style={'width': '100%', 'height': '300px'},
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
                            # 'data': {'id': 'us', 'label': 'HT_T101'}
                            'data': {'id': 'us'}
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
                ),
                indicator(
                    "#EF553B",
                    "Retest Rates",
                    "a_indicator",
                ),
                indicator(
                    "#EF553B",
                    "PASS Rates",
                    "b_indicator",
                ),
                indicator(
                    "#EF553B",
                    "FAIL Rates",
                    "c_indicator",
                ),
            ]),
            # html.Div([
                
            # ],
            # className="four columns indicator",
            # )
        ]),
    ])
]

@app.callback(Output("displot", "figure"),
             [Input("date-picker", "end_date"),],
             [State("date-picker", "start_date"),
             State("db_dropdown", "value"),
             State("collection_dropdown","value")])
def displot(endDate,startDate,db_,coll):
    # if endDate==None: return
    stime = time.time()
    stDate = datetime.strptime(startDate, "%Y-%m-%d")
    edDate = datetime.strptime(endDate, "%Y-%m-%d")
    conn = MongoClient('192.168.45.42:27017')
    db = conn[db_]
    collection=db[coll]
    # getPass = [i for i in collection.find({'Time':{'$gt': stDate,'$lt': edDate},"Result":"PASS"})]
    # getPass = [i for i in wholeData if i['Result']=='PASS' and (stDate < i['Time'] < edDate)]
    df = pd.DataFrame([i for i in collection.find({'Time':{'$gt': stDate,'$lt': edDate},"Result":"PASS"})])
    df = df.fillna(0)
    if coll == 'DsQAM' or coll == 'UsQAM':
        df = df.drop(['Frequency','ChResult','MeasurePwr','Result','ReportPwr'], axis=1)
        cols = df.columns.tolist()
        colSorted = cols[:-4]
    elif coll == 'DsMER' or coll == 'UsSNR':
        if coll == 'DsMER':
            df = df.drop(['Frequency','ChResult','RxMer','Result','Time','Station-id','TestTime','Criteria'], axis=1)
        elif coll == 'UsSNR':
            df = df.drop(['Frequency','ChResult','UsSnr','Result','Time','Station-id','TestTime','Criteria'], axis=1)
        cols = df.columns.tolist()
        colSorted = cols[:-1]
    dataList = []
    for x in colSorted:
        dataList.append(df[x])    
    # print(dataList,colSorted)
    print('Displot During Time : {}'.format(time.time()-stime))
    return ff.create_distplot(dataList, colSorted,show_curve=False, bin_size=.5,show_rug=False)

@app.callback(Output("leads_table", "children"),
             [Input("date-picker", "end_date"),],
             [State("date-picker", "start_date"),
             State("db_dropdown", "value"),
             State("collection_dropdown", "value"),])
def tables(endDate,startDate,db,coll):
    # print(type(startDate),startDate,endDate)
    # if endDate==None:
    #     stDate = '2018-11-13'
    #     endDate = '2018-11-14' 
    print(startDate,endDate)
    stDate = datetime.strptime(startDate, "%Y-%m-%d")
    edDate = datetime.strptime(endDate, "%Y-%m-%d")
    print("---------------",stDate,edDate)
    return df_to_table(cpkinitalTable(stDate,edDate,db,coll))
    # return df_to_table(df[["_id","Station-id","Time","333000000_R","339000000_R","345000000_R","351000000_R","357000000_R",
    #         "363000000_R","369000000_R","375000000_R","381000000_R","387000000_R","393000000_R","399000000_R","405000000_R",
    #         "411000000_R","417000000_R","423000000_R"]])

@app.callback(Output("lead_source", "figure"),
             [Input("date-picker", "end_date"),],
             [State("date-picker", "start_date"),])
def reTestRatio(endDate,startDate):
    # if endDate==None:return
    stDate = datetime.strptime(startDate, "%Y-%m-%d")
    edDate = datetime.strptime(endDate, "%Y-%m-%d")
    r = getErrorCount(stDate,edDate)
    # print(r)
    trace = go.Pie(
                labels=list(r.keys()),
                values=list(r.values()),
                marker={"colors": ["#264e86", "#0074e4", "#74dbef", "#eff0f4"]},
            )
    layout=dict(margin=dict(l=0, r=0, t=0, b=65), legend=dict(orientation="h"))
    return dict(data=[trace], layout=layout)

@app.callback(Output("leads_modal", "style"), 
             [Input("new_case", "n_clicks")])
def display_cases_modal_callback(n):
    print('-------------------'+str(n))
    if n > 0:
        print('block')
        return {"display": "block"}
    print('none')
    return {"display": "none"}

@app.callback(Output("new_case", "n_clicks"),
             [Input("leads_modal_close", "n_clicks")])
def close_modal_callback(n):
    print(n)
    return 0