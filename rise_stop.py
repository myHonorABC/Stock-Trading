import pandas as pd
from matplotlib import pyplot as plt
from ballstock_download import download_data
import baostock as bs
import datetime
from stock_strategy import days_overrise1, surplus_line1, double_average_line1
from buy_and_sell import StockDeal,get_stock_datas


stock_code = 'sz.000592'
# bs.login()
# download_data([stock_code])
# bs.logout()
start_date = datetime.datetime.strptime('19900101', '%Y%m%d')
delta_date = datetime.timedelta(days=10)
end_date = datetime.datetime.today() - delta_date
stock_datas = get_stock_datas(stock_code, 'd')

cur_rate = 0
all_rise_rate = []
for i in range(10):
    cur_rate += 0.01
    all_rise_rate.append(cur_rate)

# all_rise_rate = [0.1]

rise_radio = []
all_pcfNcfTTM = []
all_psTTM = []
all_pbMRQ = []
all_turn = []
all_ac = []
for rate_item in all_rise_rate:
    all_rise = 0
    next_rise = 0
    pcfNcfTTM_temp = []
    psTTM_temp = []
    pbMRQ_temp = []
    turn_temp = []
    ac_temp = []
    for index in range(stock_datas.shape[0]-1):
        days = 3
        if index in range(days):
            continue
        before_rise_rate = (stock_datas.loc[index, 'close'] - stock_datas.loc[index-1, 'close']) / \
                    stock_datas.loc[index-1, 'close']
        rise_rate = (stock_datas.loc[index+1, 'close'] - stock_datas.loc[index, 'close']) / stock_datas.loc[index, 'close']
        cur_pctChg = stock_datas.loc[index, 'pctChg']
        cur_psTTM = stock_datas.loc[index, 'psTTM']
        cur_pbMRQ = stock_datas.loc[index, 'pbMRQ']
        cur_turn = stock_datas.loc[index, 'turn']
        cur_ac = stock_datas.loc[index, 'amount'] / stock_datas.loc[index, 'volume']
        max_price = stock_datas.loc[(index-days):(index-1), 'high'].max()
        if (before_rise_rate >= rate_item and before_rise_rate <= rate_item+1) and (stock_datas.loc[index, 'close'] <= max_price) and (stock_datas.loc[index, 'high'] >= max_price):
            all_rise += 1
            if (rise_rate > 0):
                next_rise += 1
                pcfNcfTTM_temp.append(stock_datas.loc[index, 'pcfNcfTTM'])
                psTTM_temp.append(stock_datas.loc[index, 'psTTM'])
                pbMRQ_temp.append(stock_datas.loc[index, 'pbMRQ'])
                turn_temp.append(stock_datas.loc[index, 'turn'])
                ac_temp.append(cur_ac)
    print(next_rise / all_rise)
    if all_rise != 0:
        rise_temp = next_rise / all_rise
        rise_radio.append(rise_temp)
    else:
        rise_radio.append(1)
    all_pcfNcfTTM.append(pcfNcfTTM_temp)
    all_psTTM.append(psTTM_temp)
    all_pbMRQ.append(pbMRQ_temp)
    all_turn.append(turn_temp)
    all_ac.append(ac_temp)
# plt.plot(all_rise_rate, rise_radio, color='red')
# plt.show()
# for pcfNcfTTM_item in all_pcfNcfTTM:
#     plt.plot(range(len(pcfNcfTTM_item)), pcfNcfTTM_item, color='red')
# for psTTM_item in all_psTTM:
#     plt.plot(range(len(psTTM_item)), psTTM_item, color='red')
# for pbMRQ_item in all_pbMRQ:
#     plt.plot(range(len(pbMRQ_item)), pbMRQ_item, color='red')
# for turn_item in all_turn:
#     plt.plot(range(len(turn_item)), turn_item, color='red')
#     plt.show()
# for ac_item in all_ac:
#     plt.plot(range(len(ac_item)), ac_item, color='red')
#     plt.show()
# plt.show()
