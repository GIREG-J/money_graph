'''
Dash app to follow the money expenditure


$ set FLASK_APP=app.py
$ python -m flask run --host=0.0.0.0
'''

import datetime
import sqlite3
import flask
from multiprocessing import cpu_count

import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
# cf.getThemes()
import cufflinks as cf
cf.go_offline()
cf.set_config_file(theme='white')  # world_readable=True
import pandas as pd

from alpha_vantage.foreignexchange import ForeignExchange

# read the API key
f = open('YOUR_API_KEY.txt', 'r')
cc = ForeignExchange(key=f.readline())
f.close()

# connect to sqlite database and read data
connect = sqlite3.connect('money_test.db')
c = connect.cursor()
c.execute(
    'CREATE TABLE IF NOT EXISTS money_eur(datetime TEXT, comment TEXT, value REAL, currency TEXT, paidby TEXT)'
)
c.execute(
    'CREATE TABLE IF NOT EXISTS money_log(datetime TEXT, comment TEXT, value REAL, currency TEXT, paidby TEXT)'
)
# pd.DataFrame(columns=['comment', 'value', 'currency', 'paid_by']).to_sql(
#     name='money_eur', con=connect, if_exists='append')
# pd.DataFrame(columns=['comment', 'value', 'currency', 'paid_by']).to_sql(
#     name='money_log', con=connect, if_exists='append')
df = pd.read_sql(
    sql='SELECT * FROM money_eur', con=connect, index_col='datetime')
df['cumulated'] = df.value.cumsum()
lab = {key: val for key, val in zip(df.index, df.comment)}
connect.close()

# create new entry


def add_entry(comment, value, curr, paidby):
    return pd.DataFrame(
        [[comment, value, curr, paidby]],
        columns=['comment', 'value', 'currency', 'paidby'],
        index=[datetime.datetime.now()])


def api_currency(cur):
    rate, _ = cc.get_currency_exchange_rate(
        from_currency=cur, to_currency='EUR')
    return float(rate['5. Exchange Rate'])


server = flask.Flask(__name__)
app = dash.Dash(__name__, server=server)
app.css.append_css({
    "external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"
})
app.layout = html.Div(
    children=[
        html.H1(children='Money expenditures'),
        dcc.Input(id='comment', placeholder='What?', type='text'),
        dcc.Input(id='value', placeholder='How much?', type='number', min=0),
        dcc.Dropdown(
            id='currency',
            options=[{
                'label': 'Euro',
                'value': 'EUR'
            }, {
                'label': 'New Taiwan Dollar',
                'value': 'TWD'
            }, {
                'label': 'US Dollar',
                'value': 'USD'
            }, {
                'label': 'British Pound',
                'value': 'GBP'
            }],
            value='EUR'),
        dcc.Dropdown(
            id='paidby',
            options=[{
                'label': 'Gireg',
                'value': 'gireg'
            }, {
                'label': 'Shou-Ping',
                'value': 'shou-ping'
            }],
            value='gireg'),
        html.Button('Submit', id='button'),
        dcc.Graph(
            id='graph',
            figure=df[['value', 'cumulated']].iplot(
                xTitle='Date',
                yTitle='Amount [EUR]',
                annotations=lab,
                asFigure=True,
                fill=True))
    ],
    style={'columnCount': 1})


@app.callback(
    Output('graph', 'figure'), [Input('button', 'n_clicks')], [
        State('comment', 'value'),
        State('value', 'value'),
        State('currency', 'value'),
        State('paidby', 'value')
    ])
def update_output(n_clicks, com, value, curr, paidby):
    if None not in [com, value, curr, paidby]:
        connect = sqlite3.connect('money_test.db')
        add_entry(com, value, curr, paidby).to_sql(
            name='money_log',
            con=connect,
            if_exists='append',
            index=True,
            index_label='datetime')
        add_entry(com,
                  api_currency(curr) * value, 'EUR', paidby).to_sql(
                      name='money_eur',
                      con=connect,
                      if_exists='append',
                      index=True,
                      index_label='datetime')
        dftemp = pd.read_sql(
            sql='SELECT * FROM money_eur', con=connect, index_col='datetime')
        lab = {key: val for key, val in zip(dftemp.index, dftemp.comment)}
        dftemp['cumulated'] = dftemp.value.cumsum()
        connect.close()
        return dftemp[['value', 'cumulated']].iplot(
            xTitle='Date',
            yTitle='Amount [EUR]',
            annotations=lab,
            asFigure=True,
            fill=True)


if __name__ == '__main__':
    app.run_server(debug=False, processes=cpu_count())
    # webbrowser.open('http://127.0.0.1:8050/')
