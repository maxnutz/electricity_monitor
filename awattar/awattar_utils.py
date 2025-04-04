import datetime as dt
import subprocess
import pandas as pd
import urllib.request
import json
import os
from matplotlib import pyplot as plt
import configparser


class Request:
    def __init__(self, today_input):
        year = today_input.year
        month = today_input.month
        day = today_input.day
        self.today = dt.datetime(year, month, day)
        self.tomorrow = self.today + dt.timedelta(days=1)
        self.today_epocheseconds = self.today.timestamp()
        self.tomorrow_epocheseconds = self.tomorrow.timestamp()

        config = configparser.ConfigParser()
        current_file_path = os.path.abspath(__file__)
        config_file_path = os.path.join(
            os.path.dirname(os.path.dirname(current_file_path)),
            "static_files",
            "config.ini",
        )

        config.read(config_file_path)
        self.output_folder = config["DEFAULT"]["outputpath"]
        self.temp = config["DEFAULT"]["temp"]

    def get_data_from_API(self):
        """retrieve data from aWATTar-API"""
        # output = subprocess.check_output("curl \"https://api.awattar.at/v1/marketdata\"",
        #                                   stderr=subprocess.STDOUT,
        #                                   shell=True)
        # print(output.decode("UTF-8"))
        # with open(temp_folder + "temp.txt", "w") as f:
        #      f.write(output.decode("UTF-8"))
        # df = pd.json_normalize(data, "abc")
        # print(df)
        df_today = get_data_for_date(self.today_epocheseconds)
        if dt.datetime.now().hour >= 14:
            df_tomorrow = get_data_for_date(self.tomorrow_epocheseconds)
            df = pd.concat([df_today, df_tomorrow])
        else:
            df = df_today
        df["time"] = pd.to_datetime(df["start_timestamp"], unit="ms") + pd.Timedelta(
            hours=1
        )
        df["marketprice"] = df["marketprice"] / 10
        df = df[["time", "marketprice"]]
        df.set_index("time", drop=True, inplace=True)
        self.df = df

    def get_light_for_one_value(self, row):
        """evaluates pricing: returns value of light for one value:
        dark_green: price < 0
        green: price < mean of day and price < 11 and price > 0
        yellow: 0 < price < 11
        orange: price > mean of day and price > 0
        red: price > 11
        """
        day_mean = self.df.marketprice.mean()
        if row <= 0:
            return "olive"
        elif row > 0 and row < 11:
            if row < (day_mean - 0.1 * day_mean):
                return "green"
            elif row > (day_mean - 0.1 * day_mean) and row < (
                day_mean + 0.1 * day_mean
            ):
                return "yellow"
            elif row > (day_mean + 0.1 * day_mean):
                return "orange"
            else:
                raise ValueError(
                    "Algorithm for light evaluation failed in between 0 and 11"
                )
        elif row > 11:
            return "red"
        else:
            print(row)
            raise ValueError("Algorithm for light evaluation failed")

    def evaluate_pricing(self):
        """evaluate pricing and return light"""
        self.df["light"] = self.df.marketprice
        self.df.light = self.df.marketprice.apply(
            lambda x: self.get_light_for_one_value(x)
        )

    def plot(self):
        """evaluates pricing with own method
        plots data
        saves data to html file.
        returns plotly figure"""

        import plotly.express as px
        import plotly.graph_objects as go

        self.evaluate_pricing()

        fig = go.Figure(
            go.Bar(
                x=self.df.index,
                y=self.df["marketprice"],
                marker={"color": self.df["light"]},
            )
        )
        fig = fig.update_layout(
            title="Market Price aWATTar",  # Set the title text
            title_font=dict(size=24),  # Customize font size
            title_x=0.5,  # Center the title (0: left, 1: right, 0.5: center)
        )
        fig.write_html(self.output_folder + "/awattar_price_plot.html")

        return fig


def get_data_for_date(epocheseconds):
    """recieve data for one day, given in epocheseconds and returned as pandas dataframe"""
    url = (
        "https://api.awattar.at/v1/marketdata?start="
        + str(round(epocheseconds))
        + "000"
    )
    req = urllib.request.Request(url=url)
    r = urllib.request.urlopen(req).read()
    cont = json.loads(r.decode("utf-8"))
    df = pd.DataFrame(cont["data"])
    return df
