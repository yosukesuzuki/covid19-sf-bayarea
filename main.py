import io
import random
from flask import Flask, Response
import pandas as pd
import matplotlib
matplotlib.use("Agg")
from matplotlib import pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

BAY_AREA = ['Alameda', 'Contra Costa', 'Marin', 'Napa', 'San Francisco', 'San Mateo', 'Santa Clara', 'Solano', 'Sonoma']
COUNTY_DATA_SOURCE = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv"

app = Flask(__name__)

"""
def create_chart():
    df = pd.read_csv(COUNTY_DATA_SOURCE, header=0)
    ca_df_mar = df[(df['state'] == 'California') & (df['date'] > '2020-02-28')]
    by_county_by_date = ca_df_mar.pivot_table(index='date', columns='county', values='cases', fill_value=0)[BAY_AREA]
    by_county_by_date_diff = by_county_by_date.diff().iloc[1:]
    by_county_by_date_diff.plot(kind="bar", stacked=True, figsize=(15, 6),
                                title='Daily new cases by county in SF bay area')
    plt.print_png(output)
"""


@app.route('/plot.png')
def plot_png():
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    df = pd.read_csv(COUNTY_DATA_SOURCE, header=0)
    ca_df_mar = df[(df['state'] == 'California') & (df['date'] > '2020-02-28')]
    by_county_by_date = ca_df_mar.pivot_table(index='date', columns='county', values='cases', fill_value=0)[BAY_AREA]
    by_county_by_date_diff = by_county_by_date.diff().iloc[1:]
    by_county_by_date_diff.plot(ax=ax, kind="bar", stacked=True, figsize=(15, 6),
                                title='Daily new cases by county in SF bay area')
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')


if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
