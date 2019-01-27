'''import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import flask
import os
import pandas as pd


app = dash.Dash()

app.layout = html.Div([
    html.A(id='download-link', children='Download File'),
    dcc.Dropdown(
        id='dropdown',
        options=[{'label': i, 'value': i} for i in ['NYC', 'LA' 'SF']],
        value='NYC',
        clearable=False
    )
])

@app.callback(Output('download-link', 'href'),
              [Input('dropdown', 'value')])
def update_href(dropdown_value):
    df = pd.DataFrame({dropdown_value: [1, 2, 3]})
    relative_filename = os.path.join(
        'downloads',
        # '{}-download.xlsx'.format(dropdown_value)
        '{}.rar'.format(dropdown_value)
    )
    absolute_filename = os.path.join(os.getcwd(), relative_filename)
    writer = pd.ExcelWriter(absolute_filename)
    df.to_excel(writer, 'Sheet1')
    writer.save()
    return '/{}'.format(relative_filename)


@app.server.route('/downloads/<path:path>')
def serve_static(path):
    root_dir = os.getcwd()
    return flask.send_from_directory(
        os.path.join(root_dir, 'downloads'), path
    )

if __name__ == '__main__':
    app.run_server(debug=True)
'''
import dash
import os
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_core_components as dcc
from flask import send_file
app = dash.Dash()

app.layout = html.Div([

    html.A(
        'Download Zip',
        id='download-zip',
        download = "example.zip",
        href="",
        target="_blank",
        n_clicks = 0
        )
    ])

@app.callback(
    Output('download-zip', 'href'),
    [Input('download-zip', 'n_clicks')])

def generate_report_url(n_clicks):

    return '/dash/urldownload'

@app.server.route('/dash/urldownload')

def generate_report_url():

    return send_file(os.path.join(os.getcwd(), 'downloads\\')+'example.zip', attachment_filename = 'example.zip', as_attachment = True)

if __name__ == '__main__':
    app.run_server(debug = True)