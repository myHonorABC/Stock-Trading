import pandas as pd
from matplotlib import pyplot as plt
from ballstock_download import download_data
import baostock as bs
import datetime
from buy_and_sell import get_stock_datas
from stock_strategy import days_overrise, days_overrise_other,days_overrise_other_today, days_overrise1, surplus_line1, surplus_line1_low, \
    surplus_line2, surplus_line3, surplus_line3_low, surplus_line3_high, double_average_line1, days_overrise2_ac, \
    days_overrise2, surplus_line_sun, close_overrise_high_low, overrise_high_close_low_high, surplus_line3_low_open

# sh.600165
stock_code = 'sz.301023'
bs.login()
download_data([stock_code])
bs.logout()
start_date = datetime.datetime.strptime('19900201', '%Y%m%d')
# end_date = datetime.datetime.strptime('20200301', '%Y%m%d')
end_date = datetime.datetime.today()
stock_datas = get_stock_datas(stock_code, 'd')
datas = None
stock_yield = None

dates9, stock_yield9 = surplus_line1(stock_datas, start_date, end_date, 3, 2)
dates1, stock_yield1 = surplus_line3_low(stock_datas, start_date, end_date, 1, 1, 1)
# dates2, stock_yield2 = surplus_line3_low_open(stock_datas, start_date, end_date, 1, 1, 1)
# dates2, stock_yield2 = days_overrise_other_today(stock_datas, start_date, end_date, 1, 1)
dates10, stock_yield10 = surplus_line3_high(stock_datas, start_date, end_date, 1, 2, 1)
# dates1, stock_yield1 = surplus_line_sun(stock_datas, start_date, end_date, 3)
# dates2, stock_yield2 = surplus_line1(stock_datas, start_date, end_date, 2, 1)
dates2, stock_yield2 = surplus_line1(stock_datas, start_date, end_date, 1, 1)
dates8, stock_yield8 = surplus_line1_low(stock_datas, start_date, end_date, 1, 1)
dates3, stock_yield3 = days_overrise1(stock_datas, start_date, end_date, 1, 3, 0.002)
dates4, stock_yield4 = surplus_line2(stock_datas, start_date, end_date, 1, 1, 6)
dates5, stock_yield5 = surplus_line3(stock_datas, start_date, end_date, 1, 1)
dates6, stock_yield6 = days_overrise(stock_datas, start_date, end_date, 1, 1)
dates7, stock_yield7 = days_overrise_other(stock_datas, start_date, end_date, 3, 2, 0.0)
dates11, stock_yield11 = overrise_high_close_low_high(stock_datas, start_date, end_date, 1)
# dates11, stock_yield11 = close_overrise_high_low(stock_datas, start_date, end_date, 1, 1)

plt.plot(dates1, stock_yield1, color='red')
plt.plot(dates2, stock_yield2, color='orange')
plt.plot(dates3, stock_yield3, color='blue')
plt.plot(dates4, stock_yield4, color='green')
plt.plot(dates5, stock_yield5, color='purple')
# plt.plot(dates6, stock_yield6, color='black')
plt.plot(dates7, stock_yield7, color='pink')
plt.plot(dates8, stock_yield8, color='turquoise')
plt.plot(dates9, stock_yield9, color='yellow')
plt.plot(dates10, stock_yield10, color='fuchsia')
# plt.plot(dates11, stock_yield11, color='black')
plt.show()
