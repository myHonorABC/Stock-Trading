import pandas as pd
from matplotlib import pyplot as plt
from ballstock_download import download_data
import baostock as bs
import datetime
from buy_and_sell import get_stock_datas
from virtual_stock_strategy import days_overrise, days_overrise_other,days_overrise_other_today, days_overrise1, surplus_line1, surplus_line1_low, \
    surplus_line2, surplus_line3, surplus_line3_low, surplus_line3_high, double_average_line1, days_overrise2_ac, days_overrise2, surplus_line_sun


stock_datas = pd.read_csv('./stk_data/virtual_currency/sxp.csv')
start_date = datetime.datetime.strptime('20200928', '%Y%m%d')
end_date = datetime.datetime.strptime('20201104', '%Y%m%d')
# end_date = datetime.datetime.today()
datas = None
stock_yield = None

dates9, stock_yield9 = surplus_line1(stock_datas, start_date, end_date, 1, 1)
dates1, stock_yield1 = surplus_line3_low(stock_datas, start_date, end_date, 1, 1, 1)
dates10, stock_yield10 = surplus_line3_high(stock_datas, start_date, end_date, 1, 2, 1)
dates8, stock_yield8 = surplus_line1_low(stock_datas, start_date, end_date, 1, 1)
dates5, stock_yield5 = surplus_line3(stock_datas, start_date, end_date, 1, 1)
dates6, stock_yield6 = days_overrise(stock_datas, start_date, end_date, 1, 1)
# dates7, stock_yield7 = days_overrise_other(stock_datas, start_date, end_date, 3, 2, 0.0)

plt.plot(dates1, stock_yield1, color='red')
plt.plot(dates5, stock_yield5, color='purple')
plt.plot(dates6, stock_yield6, color='black')
# plt.plot(dates7, stock_yield7, color='pink')
plt.plot(dates8, stock_yield8, color='turquoise')
plt.plot(dates9, stock_yield9, color='yellow')
plt.plot(dates10, stock_yield10, color='fuchsia')
plt.show()
