import pandas as pd
from matplotlib import pyplot as plt

BAY_AREA = ['Alameda', 'Contra Costa', 'Marin', 'Napa', 'San Francisco', 'San Mateo', 'Santa Clara', 'Solano', 'Sonoma']


def main():
    df = pd.read_csv("https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv", header=0)
    ca_df_mar = df[(df['state'] == 'California') & (df['date'] > '2020-02-28')]
    by_county_by_date = ca_df_mar.pivot_table(index='date', columns='county', values='cases', fill_value=0)[BAY_AREA]
    by_county_by_date_diff = by_county_by_date.diff().iloc[1:]
    by_county_by_date_diff.plot(kind="bar", stacked=True, figsize=(15, 6),
                                title='Daily new cases by county in SF bay area')
    plt.savefig("./sf-bayarea-stacked-bar.png")


if __name__ == '__main__':
    main()
