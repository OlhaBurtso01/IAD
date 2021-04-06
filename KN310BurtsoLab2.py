import io
import cartoframes
import requests
from bs4 import BeautifulSoup
import pandas as pd
import plotly.express as px
import plotly
import plotly.graph_objs as go
import plotly.express as px
from plotly.subplots import make_subplots

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import pickle
import geopandas as gpd

# URL = 'https://nszu.gov.ua/covid/dashboard'
URL = 'https://raw.githubusercontent.com/VasiaPiven/covid19_ua/master/covid19_by_settlement_dynamics.csv'
url2 = 'https://raw.githubusercontent.com/VasiaPiven/covid19_ua/master/covid19_by_settlement_actual.csv'


# HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
#                          'Chrome/86.0.4240.111 Safari/537.36',
#            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,'
#                      '*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'}


def get_html(url, params=None):
    # response = requests.get(url, headers=HEADERS, params=params)
    response = requests.get(url, params=params).content
    return response


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    # items = soup.find_all('iframe', src = 'https://app.powerbi.com/view?r=eyJrIjoiN2M1MTY1MDktZTY5Mi00OTE0LWFiMDAtMjM4NTY0YWU2MmI3IiwidCI6IjI4OGJmYmNmLTVhYjItNDk2MS04YTM5LTg2MDYxYWFhY2Q4NiIsImMiOjl9')
    # items = soup.find_all('div', class_='container')
    items = soup.find_all('a', href='/VasiaPiven/covid19_ua/blob/master/covid19_by_settlement_dynamics.csv?raw=true')
    print(items)


def parse():
    html = get_html(URL)
    if html.status_code == 200:
        get_content(html)
    else:
        print('Error')


# # parse()
# df = pd.read_csv(URL)
# # змінюємо формат дати
# df['zvit_date'] = pd.to_datetime(df['zvit_date'], format='%Y.%b.%d')
# df = df.set_index("zvit_date")

# s = get_html(url2)
# df = pd.read_csv(io.StringIO(s.decode('utf-8')))
df = pd.read_csv('covid19_by_settlement_dynamics.csv', delimiter=',')
# df['zvit_date'] = pd.to_datetime(df['zvit_date'])
# виводимо останні 100 рядків датафрейму
# print(df.tail(100).to_string())
# виводимо типи даних для перевірки чи всі дані добре відформатовані
print("\n\n", df.dtypes)


def data_by_area(df, name_obl):
    oblast = df.loc[df['registration_area'] == name_obl]
    print("\n\n", oblast.head(100).to_string())


def group_data(df):
    obl_gr_date = df.groupby('zvit_date').sum()
    print("\n\n", obl_gr_date.to_string())
    return obl_gr_date


def by_oblast(df):
    sum_data_by_area = df.groupby('registration_area').sum()
    print("\n\n", sum_data_by_area.to_string())
    # print(obl_gr_date['total_susp'])
    #

    mean_data_by_area = df.groupby('registration_area').median()
    # print("\n\n", mean_data_by_area.to_string())

    sum_data_by_area.update(mean_data_by_area['registration_settlement_lng'])
    sum_data_by_area.update(mean_data_by_area['registration_settlement_lat'])
    print(sum_data_by_area.to_string())

    # fig = px.scatter_mapbox(sum_data_by_area, lat="registration_settlement_lat", lon="registration_settlement_lng",
    #                         hover_name=sum_data_by_area.index, hover_data=["total_susp", "total_confirm"],
    #                         color_discrete_sequence=["orange"], zoom=3, height=800)
    #
    fig = px.scatter_mapbox(sum_data_by_area, lat="registration_settlement_lat", lon="registration_settlement_lng",
                            hover_name=sum_data_by_area.index,
                            hover_data=["total_susp", "total_confirm", "total_death", "total_recover"],
                            color="total_confirm", size="total_susp",
                            color_continuous_scale=px.colors.cyclical.IceFire, size_max=50, zoom=6, height=800)

    fig.update_layout(
        mapbox_style="white-bg",
        mapbox_layers=[
            {
                "below": 'traces',
                "sourcetype": "raster",
                # "sourceattribution": "OpenStreetMap Ukraine Mapbox GL Map",
                "source": [
                    "https://basemap.nationalmap.gov/arcgis/rest/services/USGSImageryTopo/MapServer/tile/{z}/{y}/{x}"
                ]
            }
        ])
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    fig.show()
    return sum_data_by_area


def by_city(df):
    fig = px.scatter_mapbox(df, lat="registration_settlement_lat", lon="registration_settlement_lng",
                            hover_name="registration_settlement",
                            hover_data=["registration_area", "total_susp", "total_confirm", "total_death",
                                        "total_recover"],
                            color="total_confirm", size="total_susp",
                            color_continuous_scale=px.colors.diverging.RdBu, zoom=6, height=800)

    fig.update_layout(
        mapbox_style="white-bg",
        mapbox_layers=[
            {
                "below": 'traces',
                "sourcetype": "raster",
                # "sourceattribution": "Ukraine Geological Survey",
                "source": [
                    "https://basemap.nationalmap.gov/arcgis/rest/services/USGSImageryTopo/MapServer/tile/{z}/{y}/{x}"
                ]
            }
        ])
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    fig.show()
    return df


def stat_on_map(url):
    s = get_html(url)
    df = pd.read_csv(io.StringIO(s.decode('utf-8')))
    # df['zvit_date'] = pd.to_datetime(df['zvit_date'])
    # виводимо останні 100 рядків датафрейму
    # print(df.tail(100).to_string())
    while True:
        print("Можете переглянути статистику на карті\n"
              "Виберіть 1, якщо хочете побачити статистику по областях\n"
              "Виберіть 2, якщо хочете побачити статистику по населених пунктах")
        city_vs_oblast = input()
        if city_vs_oblast == '1':
            result = by_oblast(df)
            result.to_excel('oblast_total1.xlsx')
            continue
        elif city_vs_oblast == '2':
            result = by_city(df)
            result.to_excel('city_total1.xlsx')
            continue
        else:
            return


def statistic_by_oblast(df, name_obl):
    # oblast = df[df['registration_area'] == 'Чернівецька']
    oblast = df.loc[df['registration_area'] == name_obl]
    obl_gr_date = oblast.groupby('zvit_date').sum()
    print(oblast.to_string())
    print(obl_gr_date.to_string())

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=obl_gr_date.index, y=obl_gr_date['new_susp'], name='Нові підозри'))
    fig.add_trace(go.Scatter(x=obl_gr_date.index, y=obl_gr_date['new_confirm'], name='Нові підтверджені'))
    fig.add_trace(
        go.Scatter(x=obl_gr_date.index, y=obl_gr_date['active_confirm'], mode='lines+markers', name='Активні випадки'))
    fig.add_trace(go.Scatter(x=obl_gr_date.index, y=obl_gr_date['new_death'], name='Нові летальні'))
    fig.add_trace(go.Scatter(x=obl_gr_date.index, y=obl_gr_date['new_recover'], name='Нові одужавші'))
    fig.update_layout(legend_orientation="h",
                      legend=dict(x=.5, xanchor="center"),
                      hovermode="x",
                      title="Поденна статистика по області",
                      xaxis_title="Дата",
                      yaxis_title="Кількість випадків",
                      margin=dict(l=0, r=0, t=30, b=0))
    fig.update_traces(hoverinfo="all", hovertemplate="Дата: %{x}<br>Кількість випадків: %{y}")
    fig.show()
    return obl_gr_date


def oblasti(df):
    name1 = input('Введіть 1 область: ')
    name2 = input('Введіть 2 область: ')
    oblast1 = df[df['registration_area'] == name1].groupby('zvit_date').sum()
    oblast2 = df[df['registration_area'] == name2].groupby('zvit_date').sum()
    # region1 = data_frame.loc[data_frame['registration_area'] == regions[reg1]]
    # sum_by_date_1 = region1.groupby('zvit_date').sum()
    # region2 = data_frame.loc[data_frame['registration_area'] == regions[reg2]]
    # sum_by_date_2 = region2.groupby('zvit_date').sum()
    print(oblast1)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=oblast1.index, y=oblast1['active_confirm'], mode='lines+markers',
                             name=name1 + ' область: активні випадки'))
    fig.add_trace(go.Scatter(x=oblast2.index, y=oblast2['active_confirm'], mode='lines+markers',
                             name=name2 + ' область: активні випадки'))
    fig.update_layout(legend_orientation="h",
                      legend=dict(x=.5, xanchor="center"),
                      hovermode="x",
                      title="Поденна статистика по області",
                      xaxis_title="Дата",
                      yaxis_title="Кількість випадків",
                      margin=dict(l=0, r=0, t=30, b=0))
    fig.update_traces(hoverinfo="all", hovertemplate="Дата: %{x}<br>Кількість випадків: %{y}")
    fig.show()
    # return oblast1.join(oblast2[oblast2.index])


def choise2():
    while True:
        print("\n\n"
              "Виберіть дію, яку ви хочете зробити:\n"
              "1 - Вибрати дані по одній з областей України\n"
              "2 - Згрупувати дані по ознаці “однакова дата” за операцією SUM\n"
              "3 - Побудувати динаміку активних, підозрілих, підтверджених, летальних, госпіталізованих хворих\n"
              "4 - Провести порівняльний аналіз захворівших по різним областям\n"
              "5 - Вивести статистичні дані па Україні на географічну карту\n")
        choise = input()
        if choise == '1':
            obl = str(input('Введіть область: '))
            data_by_area(df, obl)
        elif choise == '2':
            result = group_data(df)
            result.to_excel('1.xlsx')
        elif choise == '3':
            obl = str(input('Введіть область: '))
            result = statistic_by_oblast(df, obl)
            result.to_excel('statistic_by_oblast_by_date.xlsx')
            continue
        elif choise == '4':
            oblasti(df)
            # result.to_excel('2_area.xlsx')
            continue
        elif choise == '5':
            stat_on_map(url2)
        else:
            exit()


choise2()
