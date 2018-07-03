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

```
$ git clone https://github.com/GIREG-J/money_graph.git
```

## Run on your machine

In Windows's command line run:
```
$ cd money_graph
$ set FLASK_APP=app.py
$ python -m flask run
```

## Run on your local network
**Only you trust the users on your network**

```
$ cd money_graph
$ python -m flask run --host=0.0.0.0
```

### Deploy
See how to deploy a Flask app on the [Flask documentation](http://flask.pocoo.org/docs/1.0/deploying/#deployment)
