# -*- coding: utf-8 -*-
import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import plotly.figure_factory as ff
import dash_html_components as html
from datetime import datetime
import pandas as pd
import flask, os
import plotly.plotly as py
from plotly import graph_objs as go
from pymongo import MongoClient
from bson.objectid import ObjectId
from apps import cpk
from apps.cpk import *
from mongo import *
# conn_ = MongoClient('192.168.45.38:27017')
# db_ = conn_['1521900003T0']
# collection_=db_.DsQAM

# wholeData = [i for i in collection_.find()]
# print(wholeData)

app = dash.Dash(__name__)
app.config.suppress_callback_exceptions = True

# css_directory = os.getcwd()
# stylesheets = ['dash_crm.css','all.css','typography.css','bWLwgP.css','brPBPO.css','stylesheet-oil-and-gas.css']
# static_css_route = '/assets/'

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
                    dcc.Tab(label="CPK", value="cpk_tab"),
                    dcc.Tab(label="AFI", value="afi_tab"),
                    dcc.Tab(id="cases_tab",label="B", value="b_tab"),
                ],
                value="cpk_tab",
            )
            ],
            className="row tabs_div"
            ),
        
        # Tab content
        html.Div(id="tab_content", className="row", style={"margin": "2% 3%"}),
        # html.Link(href="https://use.fontawesome.com/releases/v5.6.3/css/all.css",rel="stylesheet"),
        # html.Link(href="https://cdn.rawgit.com/plotly/dash-app-stylesheets/2d266c578d2a6e8850ebce48fdb52759b2aef506/stylesheet-oil-and-gas.css",rel="stylesheet"),
        # html.Link(href="https://fonts.googleapis.com/css?family=Dosis", rel="stylesheet"),
        # html.Link(href="https://fonts.googleapis.com/css?family=Open+Sans", rel="stylesheet"),
        # html.Link(href="https://fonts.googleapis.com/css?family=Ubuntu", rel="stylesheet"),
        # html.Link(href="https://cdn.rawgit.com/amadoukane96/8a8cfdac5d2cecad866952c52a70a50e/raw/cd5a9bf0b30856f4fc7e3812162c74bfc0ebe011/dash_crm.css", rel="stylesheet")
    ],
    className="row",
    style={"margin": "0%"},
)

def parsingRates(cond):
    conn = MongoClient('192.168.0.12:27017')
    db = conn['1521900003T0']
    colls = db.collection_names()
    getPass = 0
    for col in colls:
        if col == 'T1_Log' or col == 'Case Label Check':continue
        collection=eval('db.{}'.format(col))
        getPass += collection.find(cond).count()
    conn.close()
    return getPass

@app.callback(Output("tab_content", "children"),
             [Input("tabs", "value")],)
def render_content(tab):
    if tab == "cpk_tab":
        return cpk.layout
    elif tab == "b_tab":
        return 'No Content'
    elif tab == "afi_tab":
        return afiTab()
    else:
        return opportunities.layout


# @app.server.route('{}<stylesheet>'.format(static_css_route))
# def serve_stylesheet(stylesheet):
#     if stylesheet not in stylesheets:
#         raise Exception(
#             '"{}" is excluded from the allowed static files'.format(
#                 stylesheet
#             )
#         )
#     return flask.send_from_directory(css_directory, stylesheet)


# app.css.append_css({'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'})
# Loading screen CSS
# app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/brPBPO.css"})


# @app.callback(Output("collection_dropdown", "disabled"),
#              [Input("db_dropdown", "value")])
# def setDbName(db):
#     print('-------------{}'.format(db))
#     if db:
#         return False
#     else:
#         return True

@app.callback(Output("pass_indicator", "children"),
             [Input("date-picker-range", "start_date"),
             Input("date-picker-range", "end_date"),])
def passContent(startDate,endDate):
    # if endDate==None:return ''
    stDate = datetime.strptime(startDate, "%Y-%m-%d")
    edDate = datetime.strptime(endDate, "%Y-%m-%d")
    print(startDate,endDate)
    return parsingRates({'Time':{'$gt': stDate},'Time':{'$lt': edDate},"Result":"PASS"})

@app.callback(Output("fail_indicator", "children"),
             [Input("date-picker-range", "start_date"),
             Input("date-picker-range", "end_date"),])
def failContent(startDate,endDate):
    # if endDate==None:return ''
    stDate = datetime.strptime(startDate, "%Y-%m-%d")
    edDate = datetime.strptime(endDate, "%Y-%m-%d")
    print(startDate,endDate)
    return parsingRates({'Time':{'$gt': stDate},'Time':{'$lt': edDate},"Result":"FAIL"})

@app.callback(Output("retest_indicator", "children"),
             [Input("date-picker-range", "start_date"),
             Input("date-picker-range", "end_date"),])
def nullContent(startDate,endDate):
    # if endDate==None:return ''
    stDate = datetime.strptime(startDate, "%Y-%m-%d")
    edDate = datetime.strptime(endDate, "%Y-%m-%d")
    print(startDate,endDate)
    return parsingRates({'Time':{'$gt': stDate},'Time':{'$lt': edDate},'_id': {'$regex':'-'}})

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
    conn = MongoClient('192.168.0.12:27017')
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

if __name__ == "__main__":
    app.run_server(debug=True,host='0.0.0.0')
