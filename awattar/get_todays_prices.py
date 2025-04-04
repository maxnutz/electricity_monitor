""" Retrieves elctricity prices for today, evaluates and saves output to file """

from awattar_utils import Request
import datetime as dt

# get todays day
today = dt.datetime.now()
# init Class and get data from api
price_data = Request(today)
price_data.get_data_from_API()
# get hours with minimal prices

# plot prices
plotly_plot = price_data.plot()
# save to file and plot
