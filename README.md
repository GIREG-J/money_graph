# Money Expenditure Web App

This is a web app using Dash and Sqlite to follow the money's expenditures

## Functionalities
- Submit expenditure with personalized:
  - Amount
  - Currency
  - User
- Graphic visualization
  - Amount over time
  - Cumulated

## Requirements

- [Dash](https://dash.plot.ly/)
- [Plotly](https://plot.ly/python/)
- [Pandas](https://pandas.pydata.org/)
- [Cufflinks](https://github.com/santosjorge/cufflinks)
- An  [Alpha Vantage](https://www.alphavantage.co/) currency API key

## Installation

### Run locally

In Windows's command line run:
```
$ set FLASK_APP=app.py
$ python -m flask run
```
or run:
```
$ python -m flask run --host=0.0.0.0
```
if you trust the users on your network.

### Deploy
See how to deploy a Flask app on the [Flask documentation](http://flask.pocoo.org/docs/1.0/deploying/#deployment)
