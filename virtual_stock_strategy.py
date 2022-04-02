import numpy as np
import pandas as pd
import math


stock_buy_rate = 0.001
yinhuashui = 0.000

def double_average_line(stock_datas, start_date, end_date, days, second_days):
    stock_datas['date'] = pd.to_datetime(stock_datas.date, format="%Y/%m/%d")
    years_data = stock_datas[(stock_datas['date'] >= start_date) & (stock_datas['date'] <= end_date)]
    years_data.reset_index(drop=True, inplace=True)
    buy_in = 100
    dates = []
    stock_yield = []
    buy_price = 0
    sell_price = 0
    origin_money = 100000000
    current_money = 100000000
    current_market_value = 0
    other_money = 0
    for index in range(years_data.shape[0]):
        if index in range(max([days, second_days])):
            stock_yield.append(0)
            dates.append(years_data.loc[index, 'date'].date())
            continue
        today_buy = 0
        average_price = years_data.loc[(index-days):(index-1),'close'].sum() / days
        second_average_price = years_data.loc[(index-second_days):(index-1),'close'].sum() / second_days
        if average_price > second_average_price and buy_in == 100:
            buy_in = 1
            buy_price = years_data.loc[index, 'open']
            stock_number = int(current_money / (buy_price * 100))
            current_market_value = stock_number * 100 * buy_price
            current_market_value = current_market_value * (1 - stock_buy_rate)
            other_money = current_money - current_market_value
            today_buy = 1
        average_price = years_data.loc[(index - days):(index - 1), 'close'].sum() / days
        second_average_price = years_data.loc[(index - second_days):(index - 1), 'close'].sum() / second_days
        if average_price < second_average_price and \
                buy_in == 1 and today_buy == 0:
            buy_in = 0
            # if years_data.loc[index, 'open'] < years_data.loc[index-days, 'low']:
            #     sell_price = years_data.loc[index, 'open']
            sell_price = years_data.loc[index, 'close']
        if buy_in == 1:
            today_yield = (years_data.loc[index, 'close'] - buy_price) / buy_price
            current_market_value = current_market_value * (1 + today_yield)
            all_today_yield = (current_market_value + other_money - origin_money) / origin_money
            stock_yield.append(all_today_yield)
            current_money = current_market_value + other_money
            buy_price = years_data.loc[index, 'close']
        if buy_in == 100:
            stock_yield.append(stock_yield[-1])
        if buy_in == 0:
            today_yield = (sell_price - buy_price) / buy_price
            current_market_value = current_market_value * (1 + today_yield)
            current_market_value = current_market_value * (1 - yinhuashui - stock_buy_rate)
            current_money = current_market_value + other_money
            all_today_yield = (current_market_value + other_money - origin_money) / origin_money
            stock_yield.append(all_today_yield)
            buy_in = 100
        dates.append(years_data.loc[index, 'date'].date())
    return dates, stock_yield


def double_average_line1(stock_datas, start_date, end_date, days, second_days, loss_days):
    stock_datas['date'] = pd.to_datetime(stock_datas.date, format="%Y/%m/%d")
    years_data = stock_datas[(stock_datas['date'] >= start_date) & (stock_datas['date'] <= end_date)]
    years_data.reset_index(drop=True, inplace=True)
    buy_in = 100
    dates = []
    stock_yield = []
    buy_price = 0
    sell_price = 0
    origin_money = 100000000
    current_money = 100000000
    current_market_value = 0
    other_money = 0
    for index in range(years_data.shape[0]):
        if index in range(max([days, second_days])):
            stock_yield.append(0)
            dates.append(years_data.loc[index, 'date'].date())
            continue
        today_buy = 0
        average_price = years_data.loc[(index-days):(index-1),'close'].sum() / days
        second_average_price = years_data.loc[(index-second_days):(index-1),'close'].sum() / second_days
        if average_price > second_average_price and buy_in == 100:
            buy_in = 1
            buy_price = years_data.loc[index, 'open']
            stock_number = int(current_money / (buy_price * 100))
            current_market_value = stock_number * 100 * buy_price
            current_market_value = current_market_value * (1 - stock_buy_rate)
            other_money = current_money - current_market_value
            today_buy = 1
        average_temp = years_data.loc[(index - days + 1):(index), 'close'].sum() / days
        second_average_temp = years_data.loc[(index - second_days + 1):(index), 'close'].sum() / second_days
        if (years_data.loc[index, 'amount'] / years_data.loc[index, 'volume'] <
            (years_data.loc[(index-loss_days):(index-1), 'amount'] /
             years_data.loc[(index-loss_days):(index-1), 'volume']).max()) and \
                buy_in == 1 and today_buy == 0:
            buy_in = 0
            # if years_data.loc[index, 'open'] < years_data.loc[index-days, 'low']:
            #     sell_price = years_data.loc[index, 'open']
            sell_price = years_data.loc[index, 'close']
        if buy_in == 1:
            today_yield = (years_data.loc[index, 'close'] - buy_price) / buy_price
            current_market_value = current_market_value * (1 + today_yield)
            all_today_yield = (current_market_value + other_money - origin_money) / origin_money
            stock_yield.append(all_today_yield)
            current_money = current_market_value + other_money
            buy_price = years_data.loc[index, 'close']
        if buy_in == 100:
            stock_yield.append(stock_yield[-1])
        if buy_in == 0:
            today_yield = (sell_price - buy_price) / buy_price
            current_market_value = current_market_value * (1 + today_yield)
            current_market_value = current_market_value * (1 - yinhuashui - stock_buy_rate)
            current_money = current_market_value + other_money
            all_today_yield = (current_market_value + other_money - origin_money) / origin_money
            stock_yield.append(all_today_yield)
            buy_in = 100
        dates.append(years_data.loc[index, 'date'].date())
    return dates, stock_yield


def double_average_line_next_day(stock_datas, start_date, end_date, days, second_days, loss_days):
    stock_datas['date'] = pd.to_datetime(stock_datas.date, format="%Y/%m/%d")
    years_data = stock_datas[(stock_datas['date'] >= start_date) & (stock_datas['date'] <= end_date)]
    years_data.reset_index(drop=True, inplace=True)
    buy_in = 100
    dates = []
    stock_yield = []
    buy_price = 0
    sell_price = 0
    origin_money = 100000000
    current_money = 100000000
    current_market_value = 0
    other_money = 0
    for index in range(years_data.shape[0]):
        if index in range(max([days, second_days])):
            stock_yield.append(0)
            dates.append(years_data.loc[index, 'date'].date())
            continue
        today_buy = 0
        average_price = years_data.loc[(index-days):(index-1),'close'].sum() / days
        second_average_price = years_data.loc[(index-second_days):(index-1),'close'].sum() / second_days
        if average_price > second_average_price and buy_in == 100:
            buy_in = 1
            buy_price = years_data.loc[index, 'open']
            stock_number = int(current_money / (buy_price * 100))
            current_market_value = stock_number * 100 * buy_price
            current_market_value = current_market_value * (1 - stock_buy_rate)
            other_money = current_money - current_market_value
            today_buy = 1
        average_temp = years_data.loc[(index - days + 1):(index), 'close'].sum() / days
        second_average_temp = years_data.loc[(index - second_days + 1):(index), 'close'].sum() / second_days
        if (years_data.loc[index-1, 'amount'] / years_data.loc[index-1, 'volume'] <
            (years_data.loc[(index-loss_days-1):(index-2), 'amount'] /
             years_data.loc[(index-loss_days-1):(index-2), 'volume']).max()) and \
                buy_in == 1 and today_buy == 0:
            buy_in = 0
            # if years_data.loc[index, 'open'] < years_data.loc[index-days, 'low']:
            #     sell_price = years_data.loc[index, 'open']
            sell_price = years_data.loc[index, 'open']
        if buy_in == 1:
            today_yield = (years_data.loc[index, 'close'] - buy_price) / buy_price
            current_market_value = current_market_value * (1 + today_yield)
            all_today_yield = (current_market_value + other_money - origin_money) / origin_money
            stock_yield.append(all_today_yield)
            current_money = current_market_value + other_money
            buy_price = years_data.loc[index, 'close']
        if buy_in == 100:
            stock_yield.append(stock_yield[-1])
        if buy_in == 0:
            today_yield = (sell_price - buy_price) / buy_price
            current_market_value = current_market_value * (1 + today_yield)
            current_market_value = current_market_value * (1 - yinhuashui - stock_buy_rate)
            current_money = current_market_value + other_money
            all_today_yield = (current_market_value + other_money - origin_money) / origin_money
            stock_yield.append(all_today_yield)
            buy_in = 100
        dates.append(years_data.loc[index, 'date'].date())
    return dates, stock_yield


def double_average_line2(stock_datas, start_date, end_date, days, second_days, loss_days):
    stock_datas['date'] = pd.to_datetime(stock_datas.date, format="%Y/%m/%d")
    years_data = stock_datas[(stock_datas['date'] >= start_date) & (stock_datas['date'] <= end_date)]
    years_data.reset_index(drop=True, inplace=True)
    buy_in = 100
    dates = []
    stock_yield = []
    buy_price = 0
    sell_price = 0
    origin_money = 100000000
    current_money = 100000000
    current_market_value = 0
    other_money = 0
    for index in range(years_data.shape[0]):
        if index in range(max([days, second_days])):
            stock_yield.append(0)
            dates.append(years_data.loc[index, 'date'].date())
            continue
        today_buy = 0
        average_price = years_data.loc[(index-days):(index-1),'close'].sum() / days
        second_average_price = years_data.loc[(index-second_days):(index-1),'close'].sum() / second_days
        if average_price > second_average_price and buy_in == 100:
            buy_in = 1
            buy_price = years_data.loc[index, 'open']
            stock_number = int(current_money / (buy_price * 100))
            current_market_value = stock_number * 100 * buy_price
            current_market_value = current_market_value * (1 - stock_buy_rate)
            other_money = current_money - current_market_value
            today_buy = 1
        average_temp = years_data.loc[(index - days + 1):(index), 'close'].sum() / days
        second_average_temp = years_data.loc[(index - second_days + 1):(index), 'close'].sum() / second_days
        if (years_data.loc[index, 'amount'] / years_data.loc[index, 'volume'] <
            (years_data.loc[(index-loss_days):(index-1), 'amount'] /
             years_data.loc[(index-loss_days):(index-1), 'volume']).max()) and \
                average_temp < second_average_temp and \
                buy_in == 1 and today_buy == 0:
            buy_in = 0
            # if years_data.loc[index, 'open'] < years_data.loc[index-days, 'low']:
            #     sell_price = years_data.loc[index, 'open']
            sell_price = years_data.loc[index, 'close']
        if buy_in == 1:
            today_yield = (years_data.loc[index, 'close'] - buy_price) / buy_price
            current_market_value = current_market_value * (1 + today_yield)
            all_today_yield = (current_market_value + other_money - origin_money) / origin_money
            stock_yield.append(all_today_yield)
            current_money = current_market_value + other_money
            buy_price = years_data.loc[index, 'close']
        if buy_in == 100:
            stock_yield.append(stock_yield[-1])
        if buy_in == 0:
            today_yield = (sell_price - buy_price) / buy_price
            current_market_value = current_market_value * (1 + today_yield)
            current_money = current_market_value + other_money
            all_today_yield = (current_market_value + other_money - origin_money) / origin_money
            stock_yield.append(all_today_yield)
            buy_in = 100
        dates.append(years_data.loc[index, 'date'].date())
    return dates, stock_yield

def double_average_volume(stock_datas, start_date, end_date, days, second_days, loss_days):
    stock_datas['date'] = pd.to_datetime(stock_datas.date, format="%Y/%m/%d")
    years_data = stock_datas[(stock_datas['date'] >= start_date) & (stock_datas['date'] <= end_date)]
    years_data.reset_index(drop=True, inplace=True)
    buy_in = 100
    dates = []
    stock_yield = []
    buy_price = 0
    sell_price = 0
    origin_money = 100000000
    current_money = 100000000
    current_market_value = 0
    other_money = 0
    for index in range(years_data.shape[0]):
        if index in range(max([days, second_days])):
            stock_yield.append(0)
            dates.append(years_data.loc[index, 'date'].date())
            continue
        today_buy = 0
        average_volume = years_data.loc[(index-days):(index-1),'volume'].sum() / days
        second_average_volume = years_data.loc[(index-second_days):(index-1),'volume'].sum() / second_days
        if average_volume < second_average_volume and buy_in == 100:
            buy_in = 1
            buy_price = years_data.loc[index, 'open']
            stock_number = int(current_money / (buy_price * 100))
            current_market_value = stock_number * 100 * buy_price
            current_market_value = current_market_value * (1 - stock_buy_rate)
            other_money = current_money - current_market_value
            today_buy = 1
        average_temp = years_data.loc[(index - days + 1):(index), 'close'].sum() / days
        second_average_temp = years_data.loc[(index - second_days + 1):(index), 'close'].sum() / second_days
        if years_data.loc[index, 'volume'] < \
            (years_data.loc[(index-loss_days):(index-1), 'volume']).max() and \
                buy_in == 1 and today_buy == 0:
            buy_in = 0
            # if years_data.loc[index, 'open'] < years_data.loc[index-days, 'low']:
            #     sell_price = years_data.loc[index, 'open']
            sell_price = years_data.loc[index, 'close']
        if buy_in == 1:
            today_yield = (years_data.loc[index, 'close'] - buy_price) / buy_price
            current_market_value = current_market_value * (1 + today_yield)
            all_today_yield = (current_market_value + other_money - origin_money) / origin_money
            stock_yield.append(all_today_yield)
            current_money = current_market_value + other_money
            buy_price = years_data.loc[index, 'close']
        if buy_in == 100:
            stock_yield.append(stock_yield[-1])
        if buy_in == 0:
            today_yield = (sell_price - buy_price) / buy_price
            current_market_value = current_market_value * (1 + today_yield)
            current_market_value = current_market_value * (1 - yinhuashui - stock_buy_rate)
            current_money = current_market_value + other_money
            all_today_yield = (current_market_value + other_money - origin_money) / origin_money
            stock_yield.append(all_today_yield)
            buy_in = 100
        dates.append(years_data.loc[index, 'date'].date())
        if math.isnan(current_market_value):
            print('hello')
    return dates, stock_yield

def double_average_line_over(stock_datas, start_date, end_date, days, second_days, loss_days):
    stock_datas['date'] = pd.to_datetime(stock_datas.date, format="%Y/%m/%d")
    years_data = stock_datas[(stock_datas['date'] >= start_date) & (stock_datas['date'] <= end_date)]
    years_data.reset_index(drop=True, inplace=True)
    buy_in = 100
    dates = []
    stock_yield = []
    buy_price = 0
    sell_price = 0
    origin_money = 100000000
    current_money = 100000000
    current_market_value = 0
    other_money = 0
    for index in range(years_data.shape[0]):
        if index in range(max([days, second_days])):
            stock_yield.append(0)
            dates.append(years_data.loc[index, 'date'].date())
            continue
        today_buy = 0
        # before_average_price = years_data.loc[(index-days-1):(index-2),'close'].sum() / days
        # before_second_average_price = years_data.loc[(index-second_days-1):(index-2),'close'].sum() / second_days
        average_price = years_data.loc[(index-days):(index-1),'close'].sum() / days
        second_average_price = years_data.loc[(index-second_days):(index-1),'close'].sum() / second_days
        if average_price > second_average_price and \
                (years_data.loc[index-1, 'amount'] / years_data.loc[index-1, 'volume'] <
                 years_data.loc[index-2, 'amount'] / years_data.loc[index-2, 'volume']) and buy_in == 100:
            buy_in = 1
            buy_price = years_data.loc[index, 'open']
            stock_number = int(current_money / (buy_price * 100))
            current_market_value = stock_number * 100 * buy_price
            current_market_value = current_market_value * (1 - stock_buy_rate)
            other_money = current_money - current_market_value
            today_buy = 1
        average_price = years_data.loc[(index - days):(index - 1), 'close'].sum() / days
        second_average_price = years_data.loc[(index - second_days):(index - 1), 'close'].sum() / second_days
        if (years_data.loc[index, 'amount'] / years_data.loc[index, 'volume'] <
            (years_data.loc[(index-loss_days):(index-1), 'amount'] /
             years_data.loc[(index-loss_days):(index-1), 'volume']).max()) and \
                buy_in == 1 and today_buy == 0:
            buy_in = 0
            # if years_data.loc[index, 'open'] < years_data.loc[index-days, 'low']:
            #     sell_price = years_data.loc[index, 'open']
            sell_price = years_data.loc[index, 'close']
        if buy_in == 1:
            today_yield = (years_data.loc[index, 'close'] - buy_price) / buy_price
            current_market_value = current_market_value * (1 + today_yield)
            all_today_yield = (current_market_value + other_money - origin_money) / origin_money
            stock_yield.append(all_today_yield)
            current_money = current_market_value + other_money
            buy_price = years_data.loc[index, 'close']
        if buy_in == 100:
            stock_yield.append(stock_yield[-1])
        if buy_in == 0:
            today_yield = (sell_price - buy_price) / buy_price
            current_market_value = current_market_value * (1 + today_yield)
            current_market_value = current_market_value * (1 - yinhuashui - stock_buy_rate)
            current_money = current_market_value + other_money
            all_today_yield = (current_market_value + other_money - origin_money) / origin_money
            stock_yield.append(all_today_yield)
            buy_in = 100
        dates.append(years_data.loc[index, 'date'].date())
    return dates, stock_yield

def ac_overrise_over(stock_datas, start_date, end_date, days, loss_days):
    stock_datas['date'] = pd.to_datetime(stock_datas.date, format="%Y/%m/%d")
    years_data = stock_datas[(stock_datas['date'] >= start_date) & (stock_datas['date'] <= end_date)]
    years_data.reset_index(drop=True, inplace=True)
    buy_in = 100
    dates = []
    stock_yield = []
    buy_price = 0
    sell_price = 0
    origin_money = 100000000
    current_money = 100000000
    current_market_value = 0
    other_money = 0
    for index in range(years_data.shape[0]):
        if index in range(max([days, loss_days])):
            stock_yield.append(0)
            dates.append(years_data.loc[index, 'date'].date())
            continue
        today_buy = 0
        # before_average_price = years_data.loc[(index-days-1):(index-2),'close'].sum() / days
        # before_second_average_price = years_data.loc[(index-second_days-1):(index-2),'close'].sum() / second_days
        # average_ac = (years_data.loc[(index-days):(index-1),'amount'] / years_data.loc[(index-days):(index-1),'volume']).sum() / days
        # second_average_ac = (years_data.loc[(index-second_days):(index-1),'amount'] / years_data.loc[(index-second_days):(index-1),'volume']).sum() / second_days
        if years_data.loc[index, 'amount'] > \
                (years_data.loc[(index-days):(index-1), 'amount'] ).min() and \
                years_data.loc[index,'close'] > years_data.loc[index,'open'] and buy_in == 100:
            buy_in = 1
            buy_price = years_data.loc[index, 'close']
            stock_number = int(current_money / (buy_price * 100))
            current_market_value = stock_number * 100 * buy_price
            current_market_value = current_market_value * (1 - stock_buy_rate)
            other_money = current_money - current_market_value
            today_buy = 1
        # average_price = years_data.loc[(index - days):(index - 1), 'close'].sum() / days
        # second_average_price = years_data.loc[(index - second_days):(index - 1), 'close'].sum() / second_days
        if (years_data.loc[index, 'amount'] / years_data.loc[index, 'volume'] <
            (years_data.loc[(index-loss_days):(index-1), 'amount'] /
             years_data.loc[(index-loss_days):(index-1), 'volume']).max()) and \
                buy_in == 1 and today_buy == 0:
            buy_in = 0
            # if years_data.loc[index, 'open'] < years_data.loc[index-days, 'low']:
            #     sell_price = years_data.loc[index, 'open']
            sell_price = years_data.loc[index, 'close']
        if buy_in == 1:
            today_yield = (years_data.loc[index, 'close'] - buy_price) / buy_price
            current_market_value = current_market_value * (1 + today_yield)
            all_today_yield = (current_market_value + other_money - origin_money) / origin_money
            stock_yield.append(all_today_yield)
            current_money = current_market_value + other_money
            buy_price = years_data.loc[index, 'close']
        if buy_in == 100:
            stock_yield.append(stock_yield[-1])
        if buy_in == 0:
            today_yield = (sell_price - buy_price) / buy_price
            current_market_value = current_market_value * (1 + today_yield)
            current_money = current_market_value + other_money
            all_today_yield = (current_market_value + other_money - origin_money) / origin_money
            stock_yield.append(all_today_yield)
            buy_in = 100
        dates.append(years_data.loc[index, 'date'].date())
    return dates, stock_yield

def pct_overrise(stock_datas, start_date, end_date):
    stock_datas['date'] = pd.to_datetime(stock_datas.date, format="%Y/%m/%d")
    years_data = stock_datas[(stock_datas['date'] >= start_date) & (stock_datas['date'] <= end_date)]
    years_data.reset_index(drop=True, inplace=True)
    buy_in = 100
    dates = []
    stock_yield = []
    buy_price = 0
    sell_price = 0
    origin_money = 100000000
    current_money = 100000000
    current_market_value = 0
    other_money = 0
    for index in range(years_data.shape[0]):
        if index in range(1):
            stock_yield.append(0)
            dates.append(years_data.loc[index, 'date'].date())
            continue
        today_buy = 0
        # before_average_price = years_data.loc[(index-days-1):(index-2),'close'].sum() / days
        # before_second_average_price = years_data.loc[(index-second_days-1):(index-2),'close'].sum() / second_days
        # average_ac = (years_data.loc[(index-days):(index-1),'amount'] / years_data.loc[(index-days):(index-1),'volume']).sum() / days
        # second_average_ac = (years_data.loc[(index-second_days):(index-1),'amount'] / years_data.loc[(index-second_days):(index-1),'volume']).sum() / second_days
        if years_data.loc[index, 'pctChg'] and buy_in == 100:
            buy_in = 1
            buy_price = years_data.loc[index, 'close']
            stock_number = int(current_money / (buy_price * 100))
            current_market_value = stock_number * 100 * buy_price
            current_market_value = current_market_value * (1 - stock_buy_rate)
            other_money = current_money - current_market_value
            today_buy = 1
        # average_price = years_data.loc[(index - days):(index - 1), 'close'].sum() / days
        # second_average_price = years_data.loc[(index - second_days):(index - 1), 'close'].sum() / second_days
        if years_data.loc[index, 'pctChg'] < 0 and buy_in == 1 and today_buy == 0:
            buy_in = 0
            # if years_data.loc[index, 'open'] < years_data.loc[index-days, 'low']:
            #     sell_price = years_data.loc[index, 'open']
            sell_price = years_data.loc[index, 'close']
        if buy_in == 1:
            today_yield = (years_data.loc[index, 'close'] - buy_price) / buy_price
            current_market_value = current_market_value * (1 + today_yield)
            all_today_yield = (current_market_value + other_money - origin_money) / origin_money
            stock_yield.append(all_today_yield)
            current_money = current_market_value + other_money
            buy_price = years_data.loc[index, 'close']
        if buy_in == 100:
            stock_yield.append(stock_yield[-1])
        if buy_in == 0:
            today_yield = (sell_price - buy_price) / buy_price
            current_market_value = current_market_value * (1 + today_yield)
            current_money = current_market_value + other_money
            all_today_yield = (current_market_value + other_money - origin_money) / origin_money
            stock_yield.append(all_today_yield)
            buy_in = 100
        dates.append(years_data.loc[index, 'date'].date())
    return dates, stock_yield

def two_head_overrise(stock_datas, start_date, end_date):
    stock_datas['date'] = pd.to_datetime(stock_datas.date, format="%Y/%m/%d")
    years_data = stock_datas[(stock_datas['date'] >= start_date) & (stock_datas['date'] <= end_date)]
    years_data.reset_index(drop=True, inplace=True)
    buy_in = 100
    dates = []
    stock_yield = []
    buy_price = 0
    sell_price = 0
    origin_money = 100000000
    current_money = 100000000
    current_market_value = 0
    other_money = 0
    for index in range(years_data.shape[0]):
        if index in range(1):
            stock_yield.append(0)
            dates.append(years_data.loc[index, 'date'].date())
            continue
        today_buy = 0
        # before_average_price = years_data.loc[(index-days-1):(index-2),'close'].sum() / days
        # before_second_average_price = years_data.loc[(index-second_days-1):(index-2),'close'].sum() / second_days
        # average_ac = (years_data.loc[(index-days):(index-1),'amount'] / years_data.loc[(index-days):(index-1),'volume']).sum() / days
        # second_average_ac = (years_data.loc[(index-second_days):(index-1),'amount'] / years_data.loc[(index-second_days):(index-1),'volume']).sum() / second_days
        if years_data.loc[index, 'low'] > years_data.loc[index-1, 'low'] and buy_in == 100:
            buy_in = 1
            buy_price = years_data.loc[index, 'close']
            stock_number = int(current_money / (buy_price * 100))
            current_market_value = stock_number * 100 * buy_price
            current_market_value = current_market_value * (1 - stock_buy_rate)
            other_money = current_money - current_market_value
            today_buy = 1
        # average_price = years_data.loc[(index - days):(index - 1), 'close'].sum() / days
        # second_average_price = years_data.loc[(index - second_days):(index - 1), 'close'].sum() / second_days
        if years_data.loc[index, 'high'] < years_data.loc[index-1, 'high'] and buy_in == 1 and today_buy == 0:
            buy_in = 0
            # if years_data.loc[index, 'open'] < years_data.loc[index-days, 'low']:
            #     sell_price = years_data.loc[index, 'open']
            sell_price = years_data.loc[index, 'close']
        if buy_in == 1:
            today_yield = (years_data.loc[index, 'close'] - buy_price) / buy_price
            current_market_value = current_market_value * (1 + today_yield)
            all_today_yield = (current_market_value + other_money - origin_money) / origin_money
            stock_yield.append(all_today_yield)
            current_money = current_market_value + other_money
            buy_price = years_data.loc[index, 'close']
        if buy_in == 100:
            stock_yield.append(stock_yield[-1])
        if buy_in == 0:
            today_yield = (sell_price - buy_price) / buy_price
            current_market_value = current_market_value * (1 + today_yield)
            current_money = current_market_value + other_money
            all_today_yield = (current_market_value + other_money - origin_money) / origin_money
            stock_yield.append(all_today_yield)
            buy_in = 100
        dates.append(years_data.loc[index, 'date'].date())
    return dates, stock_yield

def hatch_line(stock_datas, start_date, end_date):
    stock_datas['date'] = pd.to_datetime(stock_datas.date, format="%Y/%m/%d")
    years_data = stock_datas[(stock_datas['date'] >= start_date) & (stock_datas['date'] <= end_date)]
    years_data.reset_index(drop=True, inplace=True)
    buy_in = 100
    dates = []
    stock_yield = []
    buy_price = 0
    sell_price = 0
    origin_money = 100000000
    current_money = 100000000
    current_market_value = 0
    other_money = 0
    for index in range(years_data.shape[0]):
        if index in range(1):
            stock_yield.append(0)
            dates.append(years_data.loc[index, 'date'].date())
            continue
        today_buy = 0
        # before_average_price = years_data.loc[(index-days-1):(index-2),'close'].sum() / days
        # before_second_average_price = years_data.loc[(index-second_days-1):(index-2),'close'].sum() / second_days
        # average_ac = (years_data.loc[(index-days):(index-1),'amount'] / years_data.loc[(index-days):(index-1),'volume']).sum() / days
        # second_average_ac = (years_data.loc[(index-second_days):(index-1),'amount'] / years_data.loc[(index-second_days):(index-1),'volume']).sum() / second_days
        if years_data.loc[index, 'close'] > years_data.loc[index, 'open'] and \
                years_data.loc[index, 'high'] - years_data.loc[index, 'close'] <= \
                years_data.loc[index, 'open'] - years_data.loc[index, 'low'] and buy_in == 100:
            buy_in = 1
            buy_price = years_data.loc[index, 'close']
            stock_number = int(current_money / (buy_price * 100))
            current_market_value = stock_number * 100 * buy_price
            current_market_value = current_market_value * (1 - stock_buy_rate)
            other_money = current_money - current_market_value
            today_buy = 1
        # average_price = years_data.loc[(index - days):(index - 1), 'close'].sum() / days
        # second_average_price = years_data.loc[(index - second_days):(index - 1), 'close'].sum() / second_days
        if years_data.loc[index, 'low'] <= years_data.loc[index-1, 'low'] and buy_in == 1 and today_buy == 0:
            buy_in = 0
            # if years_data.loc[index, 'open'] < years_data.loc[index-days, 'low']:
            #     sell_price = years_data.loc[index, 'open']
            sell_price = years_data.loc[index, 'close']
        if buy_in == 1:
            today_yield = (years_data.loc[index, 'close'] - buy_price) / buy_price
            current_market_value = current_market_value * (1 + today_yield)
            all_today_yield = (current_market_value + other_money - origin_money) / origin_money
            stock_yield.append(all_today_yield)
            current_money = current_market_value + other_money
            buy_price = years_data.loc[index, 'close']
        if buy_in == 100:
            stock_yield.append(stock_yield[-1])
        if buy_in == 0:
            today_yield = (sell_price - buy_price) / buy_price
            current_market_value = current_market_value * (1 + today_yield)
            current_money = current_market_value + other_money
            all_today_yield = (current_market_value + other_money - origin_money) / origin_money
            stock_yield.append(all_today_yield)
            buy_in = 100
        dates.append(years_data.loc[index, 'date'].date())
    return dates, stock_yield

def average_line(stock_datas, start_date, end_date, days):
    stock_datas['date'] = pd.to_datetime(stock_datas.date, format="%Y/%m/%d")
    years_data = stock_datas[(stock_datas['date'] >= start_date) & (stock_datas['date'] <= end_date)]
    years_data.reset_index(drop=True, inplace=True)
    buy_in = 100
    dates = []
    stock_yield = []
    buy_price = 0
    sell_price = 0
    origin_money = 100000
    current_money = 100000
    current_market_value = 0
    other_money = 0
    for index in range(years_data.shape[0]):
        if index in range(days):
            stock_yield.append(0)
            dates.append(years_data.loc[index, 'date'].date())
            continue
        today_buy = 0
        average_price = years_data.loc[(index-days):(index-1),'close'].sum() / days
        if years_data.loc[index, 'high'] > average_price and buy_in == 100:
            buy_in = 1
            if years_data.loc[index, 'low'] < average_price:
                buy_price = average_price
            else:
                buy_price = years_data.loc[index, 'close']
            stock_number = int(current_money / (buy_price * 100))
            current_market_value = stock_number * 100 * buy_price
            current_market_value = current_market_value * (1 - stock_buy_rate)
            other_money = current_money - current_market_value
            today_buy = 1
        average_price = years_data.loc[(index - days):(index - 1), 'close'].sum() / days
        if years_data.loc[index, 'low'] < average_price and \
                buy_in == 1 and today_buy == 0:
            buy_in = 0
            # if years_data.loc[index, 'open'] < years_data.loc[index-days, 'low']:
            #     sell_price = years_data.loc[index, 'open']
            if years_data.loc[index, 'high'] >= average_price:
                sell_price = average_price
            else:
                sell_price = years_data.loc[index, 'close']
        if buy_in == 1:
            today_yield = (years_data.loc[index, 'close'] - buy_price) / buy_price
            current_market_value = current_market_value * (1 + today_yield)
            all_today_yield = (current_market_value + other_money - origin_money) / origin_money
            stock_yield.append(all_today_yield)
            current_money = current_market_value + other_money
            buy_price = years_data.loc[index, 'close']
        if buy_in == 100:
            stock_yield.append(stock_yield[-1])
        if buy_in == 0:
            today_yield = (sell_price - buy_price) / buy_price
            current_market_value = current_market_value * (1 + today_yield)
            current_money = current_market_value + other_money
            all_today_yield = (current_market_value + other_money - origin_money) / origin_money
            stock_yield.append(all_today_yield)
            buy_in = 100
        dates.append(years_data.loc[index, 'date'].date())
    return dates, stock_yield

def surplus_line1(stock_datas, start_date, end_date, days, loss_days):
    stock_datas['date'] = pd.to_datetime(stock_datas.date, format="%Y/%m/%d")
    years_data = stock_datas[(stock_datas['date'] >= start_date) & (stock_datas['date'] <= end_date)]
    years_data.reset_index(drop=True, inplace=True)
    buy_in = 100
    dates = []
    stock_yield = []
    buy_price = 0
    sell_price = 0
    origin_money = 100000000
    current_money = 100000000
    current_market_value = 0
    other_money = 0
    for index in range(years_data.shape[0]):
        if index in range(max(days,loss_days)):
            stock_yield.append(0)
            dates.append(years_data.loc[index, 'date'].date())
            continue
        today_buy = 0
        # result = days_overeise_average(stock_datas, index, 3, 21)
        if years_data.loc[index, 'high'] > years_data.loc[index - days, 'high'] and \
                years_data.loc[index, 'open'] < years_data.loc[index-1, 'close']*1.1 \
                and buy_in == 100:
            buy_in = 1
            if years_data.loc[index, 'open'] >= years_data.loc[index - days, 'high']:
                buy_price = years_data.loc[index, 'open']
            else:
                buy_price = years_data.loc[index - days, 'high']
            stock_number = int(current_money / (buy_price * 1))
            current_market_value = stock_number * 1 * buy_price
            current_market_value = current_market_value * (1 - stock_buy_rate)
            other_money = current_money - current_market_value
            today_buy = 1
        if (years_data.loc[index, 'low'] < years_data.loc[index - loss_days, 'low']) and \
                buy_in == 1 and today_buy == 0:
            buy_in = 0
            # if years_data.loc[index, 'open'] <= years_data.loc[index-loss_days, 'low']:
            #     sell_price = years_data.loc[index, 'open']
            if years_data.loc[index, 'high'] >= years_data.loc[index - loss_days, 'low']:
                sell_price = years_data.loc[index - loss_days, 'low']
            else:
                sell_price = years_data.loc[index, 'close']
        if buy_in == 1:
            today_yield = (years_data.loc[index, 'close'] - buy_price) / buy_price
            current_market_value = current_market_value * (1 + today_yield)
            all_today_yield = (current_market_value + other_money - origin_money) / origin_money
            stock_yield.append(all_today_yield)
            current_money = current_market_value + other_money
            buy_price = years_data.loc[index, 'close']
        if buy_in == 100:
            stock_yield.append(stock_yield[-1])
        if buy_in == 0:
            today_yield = (sell_price - buy_price) / buy_price
            current_market_value = current_market_value * (1 + today_yield)
            current_market_value = current_market_value * (1 - yinhuashui - stock_buy_rate)
            current_money = current_market_value + other_money
            all_today_yield = (current_market_value + other_money - origin_money) / origin_money
            stock_yield.append(all_today_yield)
            buy_in = 100
        dates.append(years_data.loc[index, 'date'].date())
    return dates, stock_yield


def surplus_line1_low(stock_datas, start_date, end_date, days, loss_days):
    stock_datas['date'] = pd.to_datetime(stock_datas.date, format="%Y/%m/%d")
    years_data = stock_datas[(stock_datas['date'] >= start_date) & (stock_datas['date'] <= end_date)]
    years_data.reset_index(drop=True, inplace=True)
    buy_in = 100
    dates = []
    stock_yield = []
    buy_price = 0
    sell_price = 0
    origin_money = 100000000
    current_money = 100000000
    current_market_value = 0
    other_money = 0
    for index in range(years_data.shape[0]):
        if index in range(max(days,loss_days)):
            stock_yield.append(0)
            dates.append(years_data.loc[index, 'date'].date())
            continue
        today_buy = 0
        # result = days_overeise_average(stock_datas, index, 3, 21)
        if years_data.loc[index, 'high'] > years_data.loc[index - days, 'high'] and \
                years_data.loc[index, 'low'] <= years_data.loc[index - days, 'high'] and \
                years_data.loc[index, 'open'] < years_data.loc[index-1, 'close']*1.1 \
                and buy_in == 100:
            buy_in = 1
            # if years_data.loc[index, 'open'] >= years_data.loc[index - days, 'high']:
            #     buy_price = years_data.loc[index, 'open']
            # else:
            buy_price = years_data.loc[index - days, 'high']
            stock_number = int(current_money / (buy_price * 1))
            current_market_value = stock_number * 1 * buy_price
            current_market_value = current_market_value * (1 - stock_buy_rate)
            other_money = current_money - current_market_value
            today_buy = 1
        if (years_data.loc[index, 'low'] < years_data.loc[index - loss_days, 'low']) and \
                buy_in == 1 and today_buy == 0:
            buy_in = 0
            # if years_data.loc[index, 'open'] <= years_data.loc[index-loss_days, 'low']:
            #     sell_price = years_data.loc[index, 'open']
            if years_data.loc[index, 'high'] >= years_data.loc[index - loss_days, 'low']:
                sell_price = years_data.loc[index - loss_days, 'low']
            else:
                sell_price = years_data.loc[index, 'close']
        if buy_in == 1:
            today_yield = (years_data.loc[index, 'close'] - buy_price) / buy_price
            current_market_value = current_market_value * (1 + today_yield)
            all_today_yield = (current_market_value + other_money - origin_money) / origin_money
            stock_yield.append(all_today_yield)
            current_money = current_market_value + other_money
            buy_price = years_data.loc[index, 'close']
        if buy_in == 100:
            stock_yield.append(stock_yield[-1])
        if buy_in == 0:
            today_yield = (sell_price - buy_price) / buy_price
            current_market_value = current_market_value * (1 + today_yield)
            current_market_value = current_market_value * (1 - yinhuashui - stock_buy_rate)
            current_money = current_market_value + other_money
            all_today_yield = (current_market_value + other_money - origin_money) / origin_money
            stock_yield.append(all_today_yield)
            buy_in = 100
        dates.append(years_data.loc[index, 'date'].date())
    return dates, stock_yield


def surplus_line_sun(stock_datas, start_date, end_date, days):
    stock_datas['date'] = pd.to_datetime(stock_datas.date, format="%Y/%m/%d")
    years_data = stock_datas[(stock_datas['date'] >= start_date) & (stock_datas['date'] <= end_date)]
    years_data.reset_index(drop=True, inplace=True)
    buy_in = 100
    dates = []
    stock_yield = []
    buy_price = 0
    sell_price = 0
    origin_money = 100000000
    current_money = 100000000
    current_market_value = 0
    other_money = 0
    for index in range(years_data.shape[0]):
        if index < days:
            stock_yield.append(0)
            dates.append(years_data.loc[index, 'date'].date())
            continue
        today_buy = 0
        # result = days_overeise_average(stock_datas, index, 3, 21)
        if years_data.loc[index, 'high'] > years_data.loc[index - days, 'high'] and \
                years_data.loc[index-1, 'close'] >= years_data.loc[index-1, 'open'] and \
                years_data.loc[index, 'open'] < years_data.loc[index-1, 'close']*1.1 \
                and buy_in == 100:
            buy_in = 1
            if years_data.loc[index, 'open'] >= years_data.loc[index - days, 'high']:
                buy_price = years_data.loc[index, 'open']
            else:
                buy_price = years_data.loc[index - days, 'high']
            stock_number = int(current_money / (buy_price * 100))
            current_market_value = stock_number * 100 * buy_price
            current_market_value = current_market_value * (1 - yinhuashui)
            other_money = current_money - current_market_value
            today_buy = 1
        if (years_data.loc[index, 'close'] < years_data.loc[index, 'open']) and \
                buy_in == 1 and today_buy == 0:
            buy_in = 0
            # if years_data.loc[index, 'open'] <= years_data.loc[index-loss_days, 'low']:
            #     sell_price = years_data.loc[index, 'open']
            # if years_data.loc[index, 'high'] >= years_data.loc[index - loss_days, 'low']:
            #     sell_price = years_data.loc[index - loss_days, 'low']
            # else:
            sell_price = years_data.loc[index, 'close']
        if buy_in == 1:
            today_yield = (years_data.loc[index, 'close'] - buy_price) / buy_price
            current_market_value = current_market_value * (1 + today_yield)
            all_today_yield = (current_market_value + other_money - origin_money) / origin_money
            stock_yield.append(all_today_yield)
            current_money = current_market_value + other_money
            buy_price = years_data.loc[index, 'close']
        if buy_in == 100:
            stock_yield.append(stock_yield[-1])
        if buy_in == 0:
            today_yield = (sell_price - buy_price) / buy_price
            current_market_value = current_market_value * (1 + today_yield)
            current_market_value = current_market_value * (1 - stock_buy_rate)
            current_money = current_market_value + other_money
            all_today_yield = (current_market_value + other_money - origin_money) / origin_money
            stock_yield.append(all_today_yield)
            buy_in = 100
        dates.append(years_data.loc[index, 'date'].date())
    return dates, stock_yield


def surplus_line2(stock_datas, start_date, end_date, days, loss_days, v_days):
    stock_datas['date'] = pd.to_datetime(stock_datas.date, format="%Y/%m/%d")
    years_data = stock_datas[(stock_datas['date'] >= start_date) & (stock_datas['date'] <= end_date)]
    years_data.reset_index(drop=True, inplace=True)
    buy_in = 100
    dates = []
    stock_yield = []
    buy_price = 0
    sell_price = 0
    origin_money = 100000000
    current_money = 100000000
    current_market_value = 0
    other_money = 0
    for index in range(years_data.shape[0]):
        if index in range(max(days,loss_days)):
            stock_yield.append(0)
            dates.append(years_data.loc[index, 'date'].date())
            continue
        today_buy = 0
        # result = days_overeise_average(stock_datas, index, 3, 21)
        if years_data.loc[index, 'high'] > years_data.loc[index - days, 'high'] and \
                years_data.loc[index, 'low'] <= years_data.loc[index-days, 'high'] and \
                years_data.loc[index, 'open'] < years_data.loc[index-1, 'close']*1.1 \
                and buy_in == 100:
            buy_in = 1
            # if years_data.loc[index, 'open'] >= years_data.loc[index - days, 'high']:
            #     buy_price = years_data.loc[index, 'open']
            # else:
            buy_price = years_data.loc[index - days, 'high']
            stock_number = int(current_money / (buy_price * 100))
            current_market_value = stock_number * 100 * buy_price
            current_market_value = current_market_value * (1 - stock_buy_rate)
            other_money = current_money - current_market_value
            today_buy = 1
        if (years_data.loc[index, 'low'] < years_data.loc[index - loss_days, 'low'] or
            (years_data.loc[index,'volume']) < (years_data.loc[(index-v_days):(index-1), 'volume']).max()) and \
                years_data.loc[index, 'close'] < years_data.loc[index, 'close'] * 1.05 and \
                buy_in == 1 and today_buy == 0:
            buy_in = 0
            # if years_data.loc[index, 'open'] <= years_data.loc[index-loss_days, 'low']:
            #     sell_price = years_data.loc[index, 'open']
            if years_data.loc[index, 'high'] >= years_data.loc[index - loss_days, 'low'] and \
                    years_data.loc[index, 'low'] < years_data.loc[index - loss_days, 'low']:
                sell_price = years_data.loc[index - loss_days, 'low']
            else:
                sell_price = years_data.loc[index, 'close']
        if buy_in == 1:
            today_yield = (years_data.loc[index, 'close'] - buy_price) / buy_price
            current_market_value = current_market_value * (1 + today_yield)
            all_today_yield = (current_market_value + other_money - origin_money) / origin_money
            stock_yield.append(all_today_yield)
            current_money = current_market_value + other_money
            buy_price = years_data.loc[index, 'close']
        if buy_in == 100:
            stock_yield.append(stock_yield[-1])
        if buy_in == 0:
            today_yield = (sell_price - buy_price) / buy_price
            current_market_value = current_market_value * (1 + today_yield)
            current_market_value = current_market_value * (1 - yinhuashui - stock_buy_rate)
            current_money = current_market_value + other_money
            all_today_yield = (current_market_value + other_money - origin_money) / origin_money
            stock_yield.append(all_today_yield)
            buy_in = 100
        dates.append(years_data.loc[index, 'date'].date())
    return dates, stock_yield


def surplus_line3(stock_datas, start_date, end_date, days, loss_days):
    stock_datas['date'] = pd.to_datetime(stock_datas.date, format="%Y/%m/%d")
    years_data = stock_datas[(stock_datas['date'] >= start_date) & (stock_datas['date'] <= end_date)]
    years_data.reset_index(drop=True, inplace=True)
    buy_in = 100
    dates = []
    stock_yield = []
    buy_price = 0
    sell_price = 0
    origin_money = 100000000
    current_money = 100000000
    current_market_value = 0
    other_money = 0
    for index in range(years_data.shape[0]):
        if index in range(max(days,loss_days)):
            stock_yield.append(0)
            dates.append(years_data.loc[index, 'date'].date())
            continue
        today_buy = 0
        # result = days_overeise_average(stock_datas, index, 3, 21)
        if years_data.loc[index, 'high'] > years_data.loc[index - days, 'high'] and \
                years_data.loc[index, 'open'] < years_data.loc[index-1, 'close']*1.1 \
                and buy_in == 100:
            buy_in = 1
            if years_data.loc[index, 'open'] >= years_data.loc[index - days, 'high']:
                buy_price = years_data.loc[index, 'open']
            else:
                buy_price = years_data.loc[index - days, 'high']
            stock_number = int(current_money / (buy_price * 1))
            current_market_value = stock_number * 1 * buy_price
            current_market_value = current_market_value * (1 - stock_buy_rate)
            other_money = current_money - current_market_value
            today_buy = 1
        if (years_data.loc[index, 'low'] < years_data.loc[index - loss_days, 'close']) and \
                buy_in == 1 and today_buy == 0:
            buy_in = 0
            # if years_data.loc[index, 'open'] <= years_data.loc[index-loss_days, 'low']:
            #     sell_price = years_data.loc[index, 'open']
            if years_data.loc[index, 'high'] >= years_data.loc[index - loss_days, 'close']:
                sell_price = years_data.loc[index - loss_days, 'close']
            else:
                sell_price = years_data.loc[index, 'close']
        if buy_in == 1:
            today_yield = (years_data.loc[index, 'close'] - buy_price) / buy_price
            current_market_value = current_market_value * (1 + today_yield)
            all_today_yield = (current_market_value + other_money - origin_money) / origin_money
            stock_yield.append(all_today_yield)
            current_money = current_market_value + other_money
            buy_price = years_data.loc[index, 'close']
        if buy_in == 100:
            stock_yield.append(stock_yield[-1])
        if buy_in == 0:
            today_yield = (sell_price - buy_price) / buy_price
            current_market_value = current_market_value * (1 + today_yield)
            current_market_value = current_market_value * (1 - yinhuashui - stock_buy_rate)
            current_money = current_market_value + other_money
            all_today_yield = (current_market_value + other_money - origin_money) / origin_money
            stock_yield.append(all_today_yield)
            buy_in = 100
        dates.append(years_data.loc[index, 'date'].date())
    return dates, stock_yield


def surplus_line3_low(stock_datas, start_date, end_date, days, loss_days, rate):
    stock_datas['date'] = pd.to_datetime(stock_datas.date, format="%Y/%m/%d")
    years_data = stock_datas[(stock_datas['date'] >= start_date) & (stock_datas['date'] <= end_date)]
    years_data.reset_index(drop=True, inplace=True)
    buy_in = 100
    dates = []
    stock_yield = []
    buy_price = 0
    sell_price = 0
    origin_money = 100000000
    current_money = 100000000
    current_market_value = 0
    other_money = 0
    for index in range(years_data.shape[0]):
        if index in range(max(days,loss_days)):
            stock_yield.append(0)
            dates.append(years_data.loc[index, 'date'].date())
            continue
        today_buy = 0
        # result = days_overeise_average(stock_datas, index, 3, 21)
        if years_data.loc[index, 'high'] > years_data.loc[index - days, 'high'] and \
                years_data.loc[index, 'low'] <= years_data.loc[index - days, 'high'] and \
                ((years_data.loc[index, 'high'] - years_data.loc[index, 'low']) / years_data.loc[index, 'low'] < rate) \
                and buy_in == 100:
            buy_in = 1
            # if years_data.loc[index, 'open'] >= years_data.loc[index - days, 'high']:
            #     buy_price = years_data.loc[index, 'open']
            # else:
            buy_price = years_data.loc[index - days, 'high']
            stock_number = int(current_money / (buy_price * 1))
            current_market_value = stock_number * 1 * buy_price
            current_market_value = current_market_value * (1 - stock_buy_rate)
            other_money = current_money - current_market_value
            today_buy = 1
        if (years_data.loc[index, 'low'] < years_data.loc[index - loss_days, 'close']) and \
                buy_in == 1 and today_buy == 0:
            buy_in = 0
            # if years_data.loc[index, 'open'] <= years_data.loc[index-loss_days, 'low']:
            #     sell_price = years_data.loc[index, 'open']
            if years_data.loc[index, 'high'] >= years_data.loc[index - loss_days, 'close']:
                sell_price = years_data.loc[index - loss_days, 'close']
            else:
                sell_price = years_data.loc[index, 'close']
        if buy_in == 1:
            today_yield = (years_data.loc[index, 'close'] - buy_price) / buy_price
            current_market_value = current_market_value * (1 + today_yield)
            all_today_yield = (current_market_value + other_money - origin_money) / origin_money
            stock_yield.append(all_today_yield)
            current_money = current_market_value + other_money
            buy_price = years_data.loc[index, 'close']
        if buy_in == 100:
            stock_yield.append(stock_yield[-1])
        if buy_in == 0:
            today_yield = (sell_price - buy_price) / buy_price
            current_market_value = current_market_value * (1 + today_yield)
            current_market_value = current_market_value * (1 - yinhuashui - stock_buy_rate)
            current_money = current_market_value + other_money
            all_today_yield = (current_market_value + other_money - origin_money) / origin_money
            stock_yield.append(all_today_yield)
            buy_in = 100
        dates.append(years_data.loc[index, 'date'].date())
    return dates, stock_yield


def surplus_line3_high(stock_datas, start_date, end_date, days, loss_days, rate):
    stock_datas['date'] = pd.to_datetime(stock_datas.date, format="%Y/%m/%d")
    years_data = stock_datas[(stock_datas['date'] >= start_date) & (stock_datas['date'] <= end_date)]
    years_data.reset_index(drop=True, inplace=True)
    buy_in = 100
    dates = []
    stock_yield = []
    buy_price = 0
    sell_price = 0
    origin_money = 100000000
    current_money = 100000000
    current_market_value = 0
    other_money = 0
    for index in range(years_data.shape[0]):
        if index in range(max(days,loss_days)):
            stock_yield.append(0)
            dates.append(years_data.loc[index, 'date'].date())
            continue
        today_buy = 0
        # result = days_overeise_average(stock_datas, index, 3, 21)
        if years_data.loc[index, 'high'] > years_data.loc[index - days, 'high'] and \
                years_data.loc[index, 'low'] <= years_data.loc[index - days, 'high'] and \
                ((years_data.loc[index, 'high'] - years_data.loc[index, 'low']) / years_data.loc[index, 'low'] < rate) \
                and buy_in == 100:
            buy_in = 1
            # if years_data.loc[index, 'open'] >= years_data.loc[index - days, 'high']:
            #     buy_price = years_data.loc[index, 'open']
            # else:
            buy_price = years_data.loc[index - days, 'high']
            stock_number = int(current_money / (buy_price * 1))
            current_market_value = stock_number * 1 * buy_price
            current_market_value = current_market_value * (1 - stock_buy_rate)
            other_money = current_money - current_market_value
            today_buy = 1
        if (years_data.loc[index, 'low'] < years_data.loc[index - loss_days, 'high']) and \
                buy_in == 1 and today_buy == 0:
            buy_in = 0
            # if years_data.loc[index, 'open'] <= years_data.loc[index-loss_days, 'low']:
            #     sell_price = years_data.loc[index, 'open']
            if years_data.loc[index, 'high'] >= years_data.loc[index - loss_days, 'high']:
                sell_price = years_data.loc[index - loss_days, 'high']
            else:
                sell_price = years_data.loc[index, 'close']
        if buy_in == 1:
            today_yield = (years_data.loc[index, 'close'] - buy_price) / buy_price
            current_market_value = current_market_value * (1 + today_yield)
            all_today_yield = (current_market_value + other_money - origin_money) / origin_money
            stock_yield.append(all_today_yield)
            current_money = current_market_value + other_money
            buy_price = years_data.loc[index, 'close']
        if buy_in == 100:
            stock_yield.append(stock_yield[-1])
        if buy_in == 0:
            today_yield = (sell_price - buy_price) / buy_price
            current_market_value = current_market_value * (1 + today_yield)
            current_market_value = current_market_value * (1 - yinhuashui - stock_buy_rate)
            current_money = current_market_value + other_money
            all_today_yield = (current_market_value + other_money - origin_money) / origin_money
            stock_yield.append(all_today_yield)
            buy_in = 100
        dates.append(years_data.loc[index, 'date'].date())
    return dates, stock_yield


def typing_surplus_line(stock_datas, start_date, end_date, days):
    stock_datas['date'] = pd.to_datetime(stock_datas.date, format="%Y/%m/%d")
    years_data = stock_datas[(stock_datas['date']>=start_date) & (stock_datas['date']<=end_date)]
    years_data.reset_index(drop=True, inplace=True)
    buy_in = 100
    dates = []
    stock_yield = []
    buy_price = 0
    sell_price = 0
    origin_money = 100000
    current_money = 100000
    current_market_value = 0
    other_money = 0
    for index in range(years_data.shape[0]):
        if index in range(days+1):
            stock_yield.append(0)
            dates.append(years_data.loc[index,'date'].date())
            continue
        today_buy = 0
        if years_data.loc[index, 'high'] > years_data.loc[index-days, 'high'] and \
                years_data.loc[index, 'low'] < years_data.loc[index-days,'high'] \
                and years_data.loc[index-days, 'high'] < years_data.loc[index-days-1, 'high'] and \
                years_data.loc[index-days, 'low'] < years_data.loc[index-days-1, 'low'] \
                and buy_in==100:
            buy_in = 1
            buy_price = years_data.loc[index-days, 'high'] + 0.01
            stock_number = int(current_money / (buy_price * 100))
            current_market_value = stock_number * 100 * buy_price
            current_market_value = current_market_value * (1 - stock_buy_rate)
            other_money = current_money - current_market_value
            today_buy = 1
        if years_data.loc[index, 'low'] < years_data.loc[index-days, 'low'] and buy_in == 1 and today_buy==0:
            buy_in = 0
            if years_data.loc[index, 'high'] >= years_data.loc[index-days, 'low']:
                sell_price = years_data.loc[index-days, 'low'] - 0.01
            else:
                sell_price = years_data.loc[index, 'close']
        if buy_in == 1:
            today_yield = (years_data.loc[index, 'close'] - buy_price) / buy_price
            current_market_value = current_market_value * (1 + today_yield)
            all_today_yield = (current_market_value + other_money - origin_money) / origin_money
            stock_yield.append(all_today_yield)
            current_money = current_market_value + other_money
            buy_price = years_data.loc[index, 'close']
        if buy_in == 100:
            stock_yield.append(stock_yield[-1])
        if buy_in == 0:
            today_yield = (sell_price - buy_price) / buy_price
            current_market_value = current_market_value * (1 + today_yield)
            current_money = current_market_value + other_money
            all_today_yield = (current_market_value + other_money - origin_money) / origin_money
            stock_yield.append(all_today_yield)
            buy_in = 100
        dates.append(years_data.loc[index,'date'].date())
    return dates, stock_yield


def typing(stock_datas, start_date, end_date, days):
    stock_datas['date'] = pd.to_datetime(stock_datas.date, format="%Y/%m/%d")
    years_data = stock_datas[(stock_datas['date']>=start_date) & (stock_datas['date']<=end_date)]
    years_data.reset_index(drop=True, inplace=True)
    buy_in = 100
    dates = []
    stock_yield = []
    buy_price = 0
    sell_price = 0
    origin_money = 100000
    current_money = 100000
    current_market_value = 0
    other_money = 0
    for index in range(years_data.shape[0]):
        if index in range(days+1):
            stock_yield.append(0)
            dates.append(years_data.loc[index,'date'].date())
            continue
        today_buy = 0
        if years_data.loc[index, 'high'] > years_data.loc[index-days, 'high'] and \
                years_data.loc[index, 'low'] > years_data.loc[index-days,'low'] \
                and years_data.loc[index-days, 'high'] < years_data.loc[index-days-1, 'high'] and \
                years_data.loc[index-days, 'low'] < years_data.loc[index-days-1, 'low'] \
                and buy_in==100:
            buy_in = 1
            buy_price = years_data.loc[index, 'close']
            stock_number = int(current_money / (buy_price * 100))
            current_market_value = stock_number * 100 * buy_price
            current_market_value = current_market_value * (1 - stock_buy_rate)
            other_money = current_money - current_market_value
            today_buy = 1
        if years_data.loc[index, 'low'] < years_data.loc[index-days, 'low'] and buy_in == 1 and today_buy==0:
            buy_in = 0
            if years_data.loc[index, 'high'] >= years_data.loc[index-days, 'low']:
                sell_price = years_data.loc[index-days, 'low']
            else:
                sell_price = years_data.loc[index, 'close']
        if buy_in == 1:
            today_yield = (years_data.loc[index, 'close'] - buy_price) / buy_price
            current_market_value = current_market_value * (1 + today_yield)
            all_today_yield = (current_market_value + other_money - origin_money) / origin_money
            stock_yield.append(all_today_yield)
            current_money = current_market_value + other_money
            buy_price = years_data.loc[index, 'close']
        if buy_in == 100:
            stock_yield.append(stock_yield[-1])
        if buy_in == 0:
            today_yield = (sell_price - buy_price) / buy_price
            current_market_value = current_market_value * (1 + today_yield)
            current_market_value = current_market_value * (1 - yinhuashui - stock_buy_rate)
            current_money = current_market_value + other_money
            all_today_yield = (current_market_value + other_money - origin_money) / origin_money
            stock_yield.append(all_today_yield)
            buy_in = 100
        dates.append(years_data.loc[index,'date'].date())
    return dates, stock_yield


def overrise(stock_datas, start_date, end_date):
    stock_datas['date'] = pd.to_datetime(stock_datas.date, format="%Y/%m/%d")
    years_data = stock_datas[(stock_datas['date']>=start_date) & (stock_datas['date']<=end_date)]
    years_data.reset_index(drop=True, inplace=True)
    buy_in = 100
    dates = []
    stock_yield = []
    buy_price = 0
    sell_price = 0
    origin_money = 100000
    current_money = 100000
    current_market_value = 0
    other_money = 0
    for index in range(years_data.shape[0]):
        if index in [0]:
            stock_yield.append(0)
            dates.append(years_data.loc[index,'date'].date())
            continue
        today_buy = 0
        if years_data.loc[index, 'open'] > years_data.loc[index-1, 'high'] and buy_in==100:
            buy_in = 1
            buy_price = years_data.loc[index, 'open']
            stock_number = int(current_money / (buy_price * 100))
            current_market_value = stock_number * 100 * buy_price
            current_market_value = current_market_value * (1 - stock_buy_rate)
            other_money = current_money - current_market_value
            today_buy = 1
        if years_data.loc[index, 'low'] < years_data.loc[index-1, 'low'] and buy_in == 1 and today_buy==0:
            buy_in = 0
            if years_data.loc[index, 'high'] >= years_data.loc[index-1, 'low']:
                sell_price = years_data.loc[index-1, 'low']
            else:
                sell_price = years_data.loc[index, 'close']
        if buy_in == 1:
            today_yield = (years_data.loc[index, 'close'] - buy_price) / buy_price
            current_market_value = current_market_value * (1 + today_yield)
            all_today_yield = (current_market_value + other_money - origin_money) / origin_money
            stock_yield.append(all_today_yield)
            current_money = current_market_value + other_money
            buy_price = years_data.loc[index, 'close']
        if buy_in == 100:
            stock_yield.append(stock_yield[-1])
        if buy_in == 0:
            today_yield = (sell_price - buy_price) / buy_price
            current_market_value = current_market_value * (1 + today_yield)
            current_money = current_market_value + other_money
            all_today_yield = (current_market_value + other_money - origin_money) / origin_money
            stock_yield.append(all_today_yield)
            buy_in = 100
        dates.append(years_data.loc[index,'date'].date())
    return dates, stock_yield


def days_overrise(stock_datas, start_date, end_date, days, loss_days):
    stock_datas['date'] = pd.to_datetime(stock_datas.date, format="%Y/%m/%d")
    years_data = stock_datas[(stock_datas['date']>=start_date) & (stock_datas['date']<=end_date)]
    years_data.reset_index(drop=True, inplace=True)
    buy_in = 100
    dates = []
    stock_yield = []
    buy_price = 0
    sell_price = 0
    origin_money = 100000000
    current_money = 100000000
    current_market_value = 0
    other_money = 0
    for index in range(years_data.shape[0]):
        if index in range(days):
            stock_yield.append(0)
            dates.append(years_data.loc[index,'date'].date())
            continue
        today_buy = 0
        five_max = years_data.loc[(index-days):(index-1), 'high'].max()
        if years_data.loc[index, 'high'] > five_max and \
                years_data.loc[index, 'low'] <= five_max and \
                years_data.loc[index, 'open'] < years_data.loc[index-1, 'close']*1.1 and buy_in==100:
            buy_in = 1
            # if years_data.loc[index, 'open'] > five_max:
            #     buy_price = years_data.loc[index, 'open']
            # elif years_data.loc[index, 'low'] < five_max:
            buy_price = five_max
            # else:
            #     buy_price = years_data.loc[index, 'close']
            stock_number = int(current_money / (buy_price * 1))
            current_market_value = stock_number * 1 * buy_price
            current_market_value = current_market_value * (1 - stock_buy_rate)
            other_money = current_money - current_market_value
            today_buy = 1
        if years_data.loc[index, 'low'] < years_data.loc[(index-loss_days):(index-1), 'low'].min() and buy_in == 1 and today_buy==0:
            buy_in = 0
            # if years_data.loc[index, 'high'] > years_data.loc[(index-loss_days):(index-1), 'low'].max():
            #     sell_price = years_data.loc[(index-loss_days):(index-1), 'low'].max()
            # else:
            sell_price = years_data.loc[index, 'close']
        if buy_in == 1:
            today_yield = (years_data.loc[index, 'close'] - buy_price) / buy_price
            current_market_value = current_market_value * (1 + today_yield)
            all_today_yield = (current_market_value + other_money - origin_money) / origin_money
            stock_yield.append(all_today_yield)
            current_money = current_market_value + other_money
            buy_price = years_data.loc[index, 'close']
        if buy_in == 100:
            stock_yield.append(stock_yield[-1])
        if buy_in == 0:
            today_yield = (sell_price - buy_price) / buy_price
            current_market_value = current_market_value * (1 + today_yield)
            current_market_value = current_market_value * (1 - yinhuashui - stock_buy_rate)
            current_money = current_market_value + other_money
            all_today_yield = (current_market_value + other_money - origin_money) / origin_money
            stock_yield.append(all_today_yield)
            buy_in = 100
            print(years_data.loc[index, 'date'])
        dates.append(years_data.loc[index,'date'].date())
    return dates, stock_yield


def days_overrise_other(stock_datas, start_date, end_date, days, loss_days, add_price):
    stock_datas['date'] = pd.to_datetime(stock_datas.date, format="%Y/%m/%d")
    years_data = stock_datas[(stock_datas['date']>=start_date) & (stock_datas['date']<=end_date)]
    years_data.reset_index(drop=True, inplace=True)
    buy_in = 100
    dates = []
    stock_yield = []
    buy_price = 0
    sell_price = 0
    origin_money = 100000000
    current_money = 100000000
    current_market_value = 0
    other_money = 0
    for index in range(years_data.shape[0]):
        if index in range(max(days,loss_days+1)):
            stock_yield.append(0)
            dates.append(years_data.loc[index,'date'].date())
            continue
        today_buy = 0
        five_max = years_data.loc[(index-days):(index-1), 'high'].max()
        if years_data.loc[index, 'high'] > five_max and \
                years_data.loc[index, 'open'] < years_data.loc[index-1, 'close']*1.1 and buy_in==100:
            buy_in = 1
            if years_data.loc[index, 'open'] > five_max:
                buy_price = years_data.loc[index, 'open']
            elif years_data.loc[index, 'low'] < five_max:
                buy_price = five_max
            # else:
            #     buy_price = years_data.loc[index, 'close']
            stock_number = int(current_money / (buy_price * 1))
            current_market_value = stock_number * 1 * buy_price
            current_market_value = current_market_value * (1 - stock_buy_rate)
            other_money = current_money - current_market_value
            today_buy = 1
        if (years_data.loc[index-1, 'low'] <= years_data.loc[(index-loss_days), 'low'] or \
            years_data.loc[index-1, 'high'] < years_data.loc[index-loss_days, 'high']) and buy_in == 1 and today_buy==0:
            buy_in = 0
            if years_data.loc[index, 'high'] >= years_data.loc[(index-loss_days):(index-1), 'low'].max() + add_price:
                if years_data.loc[index, 'low'] < years_data.loc[(index-loss_days):(index-1), 'low'].max() + add_price:
                    sell_price = years_data.loc[(index-loss_days):(index-1), 'low'].max() + add_price
                else:
                    sell_price = years_data.loc[index, 'close']
            else:
                sell_price = years_data.loc[index, 'close']
        if buy_in == 1:
            today_yield = (years_data.loc[index, 'close'] - buy_price) / buy_price
            current_market_value = current_market_value * (1 + today_yield)
            all_today_yield = (current_market_value + other_money - origin_money) / origin_money
            stock_yield.append(all_today_yield)
            current_money = current_market_value + other_money
            buy_price = years_data.loc[index, 'close']
        if buy_in == 100:
            stock_yield.append(stock_yield[-1])
        if buy_in == 0:
            today_yield = (sell_price - buy_price) / buy_price
            current_market_value = current_market_value * (1 + today_yield)
            current_market_value = current_market_value * (1 - yinhuashui - stock_buy_rate)
            current_money = current_market_value + other_money
            all_today_yield = (current_market_value + other_money - origin_money) / origin_money
            stock_yield.append(all_today_yield)
            buy_in = 100
            # print(years_data.loc[index, 'date'])
        dates.append(years_data.loc[index,'date'].date())
    return dates, stock_yield


def days_overrise_other_today(stock_datas, start_date, end_date, days, loss_days):
    stock_datas['date'] = pd.to_datetime(stock_datas.date, format="%Y/%m/%d")
    years_data = stock_datas[(stock_datas['date']>=start_date) & (stock_datas['date']<=end_date)]
    years_data.reset_index(drop=True, inplace=True)
    buy_in = 100
    dates = []
    stock_yield = []
    buy_price = 0
    sell_price = 0
    origin_money = 100000000
    current_money = 100000000
    current_market_value = 0
    other_money = 0
    for index in range(years_data.shape[0]):
        if index in range(max(days,loss_days+1)):
            stock_yield.append(0)
            dates.append(years_data.loc[index,'date'].date())
            continue
        today_buy = 0
        five_max = years_data.loc[(index-days):(index-1), 'high'].max()
        if years_data.loc[index, 'high'] > five_max and \
                years_data.loc[index, 'open'] < years_data.loc[index-1, 'close']*1.1 and buy_in==100:
            buy_in = 1
            if years_data.loc[index, 'open'] > five_max:
                buy_price = years_data.loc[index, 'open']
            elif years_data.loc[index, 'low'] < five_max:
                buy_price = five_max
            # else:
            #     buy_price = years_data.loc[index, 'close']
            stock_number = int(current_money / (buy_price * 100))
            current_market_value = stock_number * 100 * buy_price
            current_market_value = current_market_value * (1 - stock_buy_rate)
            other_money = current_money - current_market_value
            today_buy = 1
        if (years_data.loc[index, 'low'] < years_data.loc[(index-loss_days), 'close'] or \
            years_data.loc[index, 'high'] <= years_data.loc[index-loss_days, 'high']) and buy_in == 1 and today_buy==0:
            buy_in = 0
            # if years_data.loc[index, 'high'] >= years_data.loc[(index-loss_days):(index-1), 'low'].max() + add_price:
            #     if years_data.loc[index, 'low'] < years_data.loc[(index-loss_days):(index-1), 'low'].max() + add_price:
            #         sell_price = years_data.loc[(index-loss_days):(index-1), 'low'].max() + add_price
            #     else:
            #         sell_price = years_data.loc[index, 'close']
            # else:
            if years_data.loc[index, 'high'] >= years_data.loc[index-loss_days, 'close']:
                sell_price = years_data.loc[index-loss_days, 'close']
            else:
                sell_price = years_data.loc[index, 'close']
        if buy_in == 1:
            today_yield = (years_data.loc[index, 'close'] - buy_price) / buy_price
            current_market_value = current_market_value * (1 + today_yield)
            all_today_yield = (current_market_value + other_money - origin_money) / origin_money
            stock_yield.append(all_today_yield)
            current_money = current_market_value + other_money
            buy_price = years_data.loc[index, 'close']
        if buy_in == 100:
            stock_yield.append(stock_yield[-1])
        if buy_in == 0:
            today_yield = (sell_price - buy_price) / buy_price
            current_market_value = current_market_value * (1 + today_yield)
            current_market_value = current_market_value * (1 - yinhuashui - stock_buy_rate)
            current_money = current_market_value + other_money
            all_today_yield = (current_market_value + other_money - origin_money) / origin_money
            stock_yield.append(all_today_yield)
            buy_in = 100
            # print(years_data.loc[index, 'date'])
        dates.append(years_data.loc[index,'date'].date())
    return dates, stock_yield


# from buy_and_sell import get_stock_datas
# def plot_5_minutes(date, stock_code):
#     stock_datas = get_stock_datas(stock_code, '5')
#     stock_datas['date'] = pd.to_datetime(stock_datas.date, format="%Y/%m/%d")
#     years_data = stock_datas[(stock_datas['date'] >= date) & (stock_datas['date'] <= date)]



def days_overrise_back(stock_datas, start_date, end_date, days, loss_days):
    stock_datas['date'] = pd.to_datetime(stock_datas.date, format="%Y/%m/%d")
    years_data = stock_datas[(stock_datas['date']>=start_date) & (stock_datas['date']<=end_date)]
    years_data.reset_index(drop=True, inplace=True)
    buy_in = 100
    dates = []
    stock_yield = []
    buy_price = 0
    add_buy_price = 0
    sell_price = 0
    origin_money = 100000000
    current_money = 100000000
    add_money = 100000000
    current_market_value = 0
    other_money = 0
    for index in range(years_data.shape[0]):
        if index in range(max(days,loss_days)):
            stock_yield.append(0)
            dates.append(years_data.loc[index,'date'].date())
            continue
        today_buy = 0
        five_max = years_data.loc[(index-days):(index-1), 'high'].max()
        if years_data.loc[index, 'high'] > five_max and buy_in==100:
            buy_in = 1
            if years_data.loc[index, 'open'] > five_max:
                buy_price = years_data.loc[index, 'open']
            elif years_data.loc[index, 'low'] <= five_max:
                buy_price = five_max
            # else:
            #     buy_price = years_data.loc[index, 'close']
            stock_number = int(current_money / (buy_price * 100))
            current_market_value = stock_number * 100 * buy_price
            current_market_value = current_market_value * (1 - stock_buy_rate)
            other_money = current_money - current_market_value
            if years_data.loc[index, 'close'] < buy_price:
                add_buy_price = years_data.loc[index, 'close']
                add_stock_number = int(add_money / (add_buy_price * 100))
                add_current_market_value = add_stock_number * 100 * add_buy_price
                add_current_market_value = add_current_market_value * (1 - stock_buy_rate)
                add_other_money = add_money - add_current_market_value
                current_market_value += add_current_market_value
                other_money += add_other_money
                origin_money += add_money
                print('11111111')
            today_buy = 1
        if years_data.loc[index, 'amount'] / years_data.loc[index, 'volume'] < \
            (years_data.loc[(index-loss_days):(index-1), 'amount'] /
             years_data.loc[(index-loss_days):(index-1), 'volume']).max()\
                and buy_in == 1 and today_buy==0:
            buy_in = 0
            sell_price = years_data.loc[index, 'close']
        if buy_in == 1:
            today_yield = (years_data.loc[index, 'close'] - buy_price) / buy_price
            current_market_value = current_market_value * (1 + today_yield)

            all_today_yield = (current_market_value + other_money - origin_money) / origin_money
            stock_yield.append(all_today_yield)
            current_money = current_market_value + other_money
            buy_price = years_data.loc[index, 'close']
        if buy_in == 100:
            stock_yield.append(stock_yield[-1])
        if buy_in == 0:
            today_yield = (sell_price - buy_price) / buy_price
            current_market_value = current_market_value * (1 + today_yield)
            current_money = current_market_value + other_money
            all_today_yield = (current_market_value + other_money - origin_money) / (origin_money)
            stock_yield.append(all_today_yield)
            buy_in = 100
        dates.append(years_data.loc[index,'date'].date())
    return dates, stock_yield


def days_overrise_next(stock_datas, start_date, end_date, days, loss_days):
    stock_datas['date'] = pd.to_datetime(stock_datas.date, format="%Y/%m/%d")
    years_data = stock_datas[(stock_datas['date']>=start_date) & (stock_datas['date']<=end_date)]
    years_data.reset_index(drop=True, inplace=True)
    buy_in = 100
    dates = []
    stock_yield = []
    buy_price = 0
    sell_price = 0
    origin_money = 100000000
    current_money = 100000000
    current_market_value = 0
    other_money = 0
    for index in range(years_data.shape[0]):
        if index in range(days):
            stock_yield.append(0)
            dates.append(years_data.loc[index,'date'].date())
            continue
        today_buy = 0
        five_max = years_data.loc[(index-days):(index-1), 'high'].max()
        if years_data.loc[index, 'high'] > five_max and buy_in==100:
            buy_in = 1
            if years_data.loc[index, 'open'] > five_max:
                buy_price = years_data.loc[index, 'open']
            elif years_data.loc[index, 'low'] <= five_max:
                buy_price = five_max + 0.01
            # else:
            #     buy_price = years_data.loc[index, 'close']
            stock_number = int(current_money / (buy_price * 100))
            current_market_value = stock_number * 100 * buy_price
            current_market_value = current_market_value * (1 - stock_buy_rate)
            other_money = current_money - current_market_value
            today_buy = 1
        if years_data.loc[index-1, 'low'] <= years_data.loc[(index-loss_days):(index-2), 'low'].min() and buy_in == 1 and today_buy==0:
            buy_in = 0
            if years_data.loc[index, 'high'] >= years_data.loc[(index-loss_days):(index-1), 'low'].max():
                sell_price = years_data.loc[(index-loss_days):(index-1), 'low'].max()
            else:
                sell_price = years_data.loc[index, 'close']
        if buy_in == 1:
            today_yield = (years_data.loc[index, 'close'] - buy_price) / buy_price
            current_market_value = current_market_value * (1 + today_yield)
            all_today_yield = (current_market_value + other_money - origin_money) / origin_money
            stock_yield.append(all_today_yield)
            current_money = current_market_value + other_money
            buy_price = years_data.loc[index, 'close']
        if buy_in == 100:
            stock_yield.append(stock_yield[-1])
        if buy_in == 0:
            today_yield = (sell_price - buy_price) / buy_price
            current_market_value = current_market_value * (1 + today_yield)
            current_money = current_market_value + other_money
            all_today_yield = (current_market_value + other_money - origin_money) / origin_money
            stock_yield.append(all_today_yield)
            buy_in = 100
        dates.append(years_data.loc[index,'date'].date())
    return dates, stock_yield


def days_overrise1(stock_datas, start_date, end_date, days, loss_days, rise_rate):
    stock_datas['date'] = pd.to_datetime(stock_datas.date, format="%Y/%m/%d")
    years_data = stock_datas[(stock_datas['date']>=start_date) & (stock_datas['date']<=end_date)]
    years_data.reset_index(drop=True, inplace=True)
    buy_in = 100
    dates = []
    stock_yield = []
    buy_price = 0
    sell_price = 0
    origin_money = 100000000
    current_money = 100000000
    current_market_value = 0
    other_money = 0
    for index in range(years_data.shape[0]):
        if index in range(days):
            stock_yield.append(0)
            dates.append(years_data.loc[index,'date'].date())
            continue
        today_buy = 0
        five_max = years_data.loc[(index-days):(index-1), 'high'].max()
        rise_rate_temp = (five_max - years_data.loc[(index-1), 'close']) / years_data.loc[(index-1), 'close']
        open_rise_rate = (years_data.loc[index, 'open'] - years_data.loc[(index-1), 'close']) / years_data.loc[(index-1), 'close']
        close_rise_rate = (years_data.loc[index, 'close'] - years_data.loc[(index-1), 'close']) / years_data.loc[(index-1), 'close']
        if years_data.loc[index, 'high'] > five_max \
                and years_data.loc[index, 'low'] <= five_max and \
                years_data.loc[index, 'open'] < years_data.loc[index-1, 'close']*1.1\
                and buy_in==100:
            buy_in = 1
            # if years_data.loc[index, 'open'] > five_max:
            #     buy_price = years_data.loc[index, 'open']
            # else:
            buy_price = five_max
            # else:
            #     buy_price = years_data.loc[index, 'close']
            stock_number = int(current_money / (buy_price * 100))
            current_market_value = stock_number * 100 * buy_price
            current_market_value = current_market_value * (1 - stock_buy_rate)
            other_money = current_money - current_market_value
            today_buy = 1
        if (years_data.loc[index, 'amount'] / years_data.loc[index, 'volume'] < (years_data.loc[(index-loss_days):(index-1), 'amount']/years_data.loc[(index-loss_days):(index-1),'volume']).max())  and \
                buy_in == 1 and today_buy==0:
            buy_in = 0
            # if years_data.loc[index, 'high'] >= years_data.loc[(index-loss_days):(index-1), 'low'].max():
            #     sell_price = years_data.loc[(index-loss_days):(index-1), 'low'].max()
            # else:
            sell_price = years_data.loc[index, 'close']
        if buy_in == 1:
            today_yield = (years_data.loc[index, 'close'] - buy_price) / buy_price
            current_market_value = current_market_value * (1 + today_yield)
            all_today_yield = (current_market_value + other_money - origin_money) / origin_money
            stock_yield.append(all_today_yield)
            current_money = current_market_value + other_money
            buy_price = years_data.loc[index, 'close']
        if buy_in == 100:
            stock_yield.append(stock_yield[-1])
        if buy_in == 0:
            today_yield = (sell_price - buy_price) / buy_price
            current_market_value = current_market_value * (1 + today_yield)
            current_market_value = current_market_value * (1 - yinhuashui - stock_buy_rate)
            current_money = current_market_value + other_money
            all_today_yield = (current_market_value + other_money - origin_money) / origin_money
            stock_yield.append(all_today_yield)
            buy_in = 100
        dates.append(years_data.loc[index,'date'].date())
    return dates, stock_yield


def days_overrise2(stock_datas, start_date, end_date, days, loss_days, rise_rate):
    stock_datas['date'] = pd.to_datetime(stock_datas.date, format="%Y/%m/%d")
    years_data = stock_datas[(stock_datas['date']>=start_date) & (stock_datas['date']<=end_date)]
    years_data.reset_index(drop=True, inplace=True)
    buy_in = 100
    dates = []
    stock_yield = []
    buy_price = 0
    sell_price = 0
    origin_money = 100000000
    current_money = 100000000
    current_market_value = 0
    other_money = 0
    for index in range(years_data.shape[0]):
        if index in range(days):
            stock_yield.append(0)
            dates.append(years_data.loc[index,'date'].date())
            continue
        today_buy = 0
        five_max = years_data.loc[(index-days):(index-1), 'high'].max()
        rise_rate_temp = (five_max - years_data.loc[(index-1), 'close']) / years_data.loc[(index-1), 'close']
        open_rise_rate = (years_data.loc[index, 'open'] - years_data.loc[(index-1), 'close']) / years_data.loc[(index-1), 'close']
        close_rise_rate = (years_data.loc[index, 'close'] - years_data.loc[(index-1), 'close']) / years_data.loc[(index-1), 'close']
        if years_data.loc[index, 'high'] > years_data.loc[index-days, 'high'] and \
                years_data.loc[index, 'open'] < years_data.loc[index-1, 'close']*1.1\
                and buy_in==100:
            buy_in = 1
            if years_data.loc[index, 'open'] >= years_data.loc[index-days, 'high']:
                buy_price = years_data.loc[index, 'open']
            elif years_data.loc[index, 'low'] <= five_max:
                buy_price = five_max
            else:
                buy_price = years_data.loc[index, 'close']
            stock_number = int(current_money / (buy_price * 100))
            current_market_value = stock_number * 100 * buy_price
            current_market_value = current_market_value * (1 - stock_buy_rate)
            other_money = current_money - current_market_value
            today_buy = 1
        if (years_data.loc[index, 'amount'] / years_data.loc[index, 'volume'] < (years_data.loc[(index-loss_days):(index-1), 'amount']/years_data.loc[(index-loss_days):(index-1),'volume']).max()) and \
                buy_in == 1 and today_buy==0:
            buy_in = 0
            # if years_data.loc[index, 'high'] >= years_data.loc[(index-loss_days), 'low']:
            #     sell_price = years_data.loc[(index-loss_days), 'low']
            # else:
            sell_price = years_data.loc[index, 'close']
        if buy_in == 1:
            today_yield = (years_data.loc[index, 'close'] - buy_price) / buy_price
            current_market_value = current_market_value * (1 + today_yield)
            all_today_yield = (current_market_value + other_money - origin_money) / origin_money
            stock_yield.append(all_today_yield)
            current_money = current_market_value + other_money
            buy_price = years_data.loc[index, 'close']
        if buy_in == 100:
            stock_yield.append(stock_yield[-1])
        if buy_in == 0:
            today_yield = (sell_price - buy_price) / buy_price
            current_market_value = current_market_value * (1 + today_yield)
            current_market_value = current_market_value * (1 - yinhuashui - stock_buy_rate)
            current_money = current_market_value + other_money
            all_today_yield = (current_market_value + other_money - origin_money) / origin_money
            stock_yield.append(all_today_yield)
            buy_in = 100
        dates.append(years_data.loc[index,'date'].date())
    return dates, stock_yield


def days_overrise2_ac(stock_datas, start_date, end_date, days, loss_days):
    stock_datas['date'] = pd.to_datetime(stock_datas.date, format="%Y/%m/%d")
    years_data = stock_datas[(stock_datas['date']>=start_date) & (stock_datas['date']<=end_date)]
    years_data.reset_index(drop=True, inplace=True)
    buy_in = 100
    dates = []
    stock_yield = []
    buy_price = 0
    sell_price = 0
    origin_money = 100000000
    current_money = 100000000
    current_market_value = 0
    other_money = 0
    for index in range(years_data.shape[0]):
        if index in range(days):
            stock_yield.append(0)
            dates.append(years_data.loc[index,'date'].date())
            continue
        today_buy = 0
        # before_days_max = years_data.loc[(index-before_days-1):(index-2), 'high'].max()
        five_max = years_data.loc[(index-days):(index-1), 'high'].max()
        if years_data.loc[index, 'high'] > five_max and buy_in==100:
            buy_in = 1
            if years_data.loc[index, 'open'] > five_max:
                buy_price = years_data.loc[index, 'open']
            elif years_data.loc[index, 'low'] <= five_max:
                buy_price = five_max
            # else:
            #     buy_price = years_data.loc[index, 'close']
            stock_number = int(current_money / (buy_price * 100))
            current_market_value = stock_number * 100 * buy_price
            current_market_value = current_market_value * (1 - stock_buy_rate)
            other_money = current_money - current_market_value
            today_buy = 1
        if ((years_data.loc[index, 'amount'] / years_data.loc[index, 'volume'] <
            (years_data.loc[(index-loss_days):(index-1), 'amount']/years_data.loc[(index-loss_days):(index-1),'volume']).max()) or \
                years_data.loc[index-1,'close'] < years_data.loc[index-2,'close'])  and \
                buy_in == 1 and today_buy==0:
            buy_in = 0
            # if years_data.loc[index, 'high'] >= years_data.loc[(index-loss_days):(index-1), 'low'].max():
            #     sell_price = years_data.loc[(index-loss_days):(index-1), 'low'].max()
            # else:
            import random
            if years_data.loc[index-1, 'close'] < years_data.loc[index-2,'close']:
                sell_price = random.uniform(years_data.loc[index,'low'], years_data.loc[index,'high'])
            else:
                sell_price = years_data.loc[index, 'close']
        if buy_in == 1:
            today_yield = (years_data.loc[index, 'close'] - buy_price) / buy_price
            current_market_value = current_market_value * (1 + today_yield)
            all_today_yield = (current_market_value + other_money - origin_money) / origin_money
            stock_yield.append(all_today_yield)
            current_money = current_market_value + other_money
            buy_price = years_data.loc[index, 'close']
        if buy_in == 100:
            stock_yield.append(stock_yield[-1])
        if buy_in == 0:
            today_yield = (sell_price - buy_price) / buy_price
            current_market_value = current_market_value * (1 + today_yield)
            current_market_value = current_market_value * (1 - yinhuashui - stock_buy_rate)
            current_money = current_market_value + other_money
            all_today_yield = (current_market_value + other_money - origin_money) / origin_money
            stock_yield.append(all_today_yield)
            buy_in = 100
        dates.append(years_data.loc[index,'date'].date())
    return dates, stock_yield


def days_overrise3(stock_datas, start_date, end_date, days):
    stock_datas['date'] = pd.to_datetime(stock_datas.date, format="%Y/%m/%d")
    years_data = stock_datas[(stock_datas['date']>=start_date) & (stock_datas['date']<=end_date)]
    years_data.reset_index(drop=True, inplace=True)
    buy_in = 100
    dates = []
    stock_yield = []
    buy_price = 0
    sell_price = 0
    origin_money = 100000000
    current_money = 100000000
    current_market_value = 0
    other_money = 0
    for index in range(years_data.shape[0]):
        if index in range(days):
            stock_yield.append(0)
            dates.append(years_data.loc[index,'date'].date())
            continue
        today_buy = 0
        five_max = years_data.loc[(index-days):(index-1), 'high'].max()
        if years_data.loc[index, 'high'] > five_max and buy_in==100:
            buy_in = 1
            if years_data.loc[index, 'open'] > five_max:
                buy_price = years_data.loc[index, 'open']
            elif years_data.loc[index, 'low'] <= five_max:
                buy_price = five_max + 0.01
            # else:
            #     buy_price = years_data.loc[index, 'close']
            stock_number = int(current_money / (buy_price * 100))
            current_market_value = stock_number * 100 * buy_price
            current_market_value = current_market_value * (1 - stock_buy_rate)
            other_money = current_money - current_market_value
            today_buy = 1
        if (years_data.loc[index, 'close'] < years_data.loc[index, 'open'].max())  and \
                buy_in == 1 and today_buy==0:
            buy_in = 0
            # if years_data.loc[index, 'high'] >= years_data.loc[(index-loss_days):(index-1), 'low'].max():
            #     sell_price = years_data.loc[(index-loss_days):(index-1), 'low'].max()
            # else:
            sell_price = years_data.loc[index, 'close']
        if buy_in == 1:
            today_yield = (years_data.loc[index, 'close'] - buy_price) / buy_price
            current_market_value = current_market_value * (1 + today_yield)
            all_today_yield = (current_market_value + other_money - origin_money) / origin_money
            stock_yield.append(all_today_yield)
            current_money = current_market_value + other_money
            buy_price = years_data.loc[index, 'close']
        if buy_in == 100:
            stock_yield.append(stock_yield[-1])
        if buy_in == 0:
            today_yield = (sell_price - buy_price) / buy_price
            current_market_value = current_market_value * (1 + today_yield)
            current_money = current_market_value + other_money
            all_today_yield = (current_market_value + other_money - origin_money) / origin_money
            stock_yield.append(all_today_yield)
            buy_in = 100
        dates.append(years_data.loc[index,'date'].date())
    return dates, stock_yield


def surplus_sun(stock_datas, start_date, end_date, days):
    stock_datas['date'] = pd.to_datetime(stock_datas.date, format="%Y/%m/%d")
    years_data = stock_datas[(stock_datas['date'] >= start_date) & (stock_datas['date'] <= end_date)]
    years_data.reset_index(drop=True, inplace=True)
    buy_in = 100
    dates = []
    stock_yield = []
    buy_price = 0
    sell_price = 0
    origin_money = 100000
    current_money = 100000
    current_market_value = 0
    other_money = 0
    for index in range(years_data.shape[0]):
        if index in range(2*days):
            stock_yield.append(0)
            dates.append(years_data.loc[index, 'date'].date())
            continue
        today_buy = 0
        if years_data.loc[index, 'high'] > years_data.loc[index - days, 'high'] and \
                years_data.loc[index-days, 'close'] > years_data.loc[index-days, 'open'] and \
                years_data.loc[index-days, 'high'] < years_data.loc[index-2*days, 'high'] and \
                years_data.loc[index-days, 'low'] < years_data.loc[index-2*days, 'low'] and buy_in == 100:
            buy_in = 1
            if years_data.loc[index, 'low'] > years_data.loc[index - days, 'high']:
                buy_price = years_data.loc[index, 'low']
            else:
                buy_price = years_data.loc[index - days, 'high'] + 0.01
            stock_number = int(current_money / (buy_price * 100))
            current_market_value = stock_number * 100 * buy_price
            current_market_value = current_market_value * (1 - stock_buy_rate)
            other_money = current_money - current_market_value
            today_buy = 1
        if years_data.loc[index, 'low'] < years_data.loc[index - days, 'low'] and \
                buy_in == 1 and today_buy == 0:
            buy_in = 0
            # if years_data.loc[index, 'open'] < years_data.loc[index-days, 'low']:
            #     sell_price = years_data.loc[index, 'open']
            if years_data.loc[index, 'high'] >= years_data.loc[index - days, 'low']:
                sell_price = years_data.loc[index - days, 'low'] - 0.01
            else:
                sell_price = years_data.loc[index, 'close']
        if buy_in == 1:
            today_yield = (years_data.loc[index, 'close'] - buy_price) / buy_price
            current_market_value = current_market_value * (1 + today_yield)
            all_today_yield = (current_market_value + other_money - origin_money) / origin_money
            stock_yield.append(all_today_yield)
            current_money = current_market_value + other_money
            buy_price = years_data.loc[index, 'close']
        if buy_in == 100:
            stock_yield.append(stock_yield[-1])
        if buy_in == 0:
            today_yield = (sell_price - buy_price) / buy_price
            current_market_value = current_market_value * (1 + today_yield)
            current_money = current_market_value + other_money
            all_today_yield = (current_market_value + other_money - origin_money) / origin_money
            stock_yield.append(all_today_yield)
            buy_in = 100
        dates.append(years_data.loc[index, 'date'].date())
    return dates, stock_yield


def surplus_hot(stock_datas, start_date, end_date, days):
    stock_datas['date'] = pd.to_datetime(stock_datas.date, format="%Y/%m/%d")
    years_data = stock_datas[(stock_datas['date'] >= start_date) & (stock_datas['date'] <= end_date)]
    years_data.reset_index(drop=True, inplace=True)
    buy_in = 100
    dates = []
    stock_yield = []
    buy_price = 0
    sell_price = 0
    origin_money = 100000
    current_money = 100000
    current_market_value = 0
    other_money = 0
    for index in range(years_data.shape[0]):
        if index in range(2*days):
            stock_yield.append(0)
            dates.append(years_data.loc[index, 'date'].date())
            continue
        today_buy = 0
        if years_data.loc[index, 'high'] > years_data.loc[index - days, 'high'] and \
                years_data.loc[index-days, 'close'] > years_data.loc[index-days, 'open'] and \
                years_data.loc[index-days, 'high'] > years_data.loc[index-2*days, 'high'] and \
                years_data.loc[index-days, 'low'] > years_data.loc[index-2*days, 'low'] and buy_in == 100:
            buy_in = 1
            if years_data.loc[index, 'low'] > years_data.loc[index - days, 'high']:
                buy_price = years_data.loc[index, 'close']
            else:
                buy_price = years_data.loc[index - days, 'high'] + 0.01
            stock_number = int(current_money / (buy_price * 100))
            current_market_value = stock_number * 100 * buy_price
            current_market_value = current_market_value * (1 - stock_buy_rate)
            other_money = current_money - current_market_value
            today_buy = 1
        if buy_in == 1 and today_buy == 0:
            buy_in = 0
            # if years_data.loc[index, 'open'] < years_data.loc[index-days, 'low']:
            #     sell_price = years_data.loc[index, 'open']
            sell_price = years_data.loc[index, 'close']
        if buy_in == 1:
            today_yield = (years_data.loc[index, 'close'] - buy_price) / buy_price
            current_market_value = current_market_value * (1 + today_yield)
            all_today_yield = (current_market_value + other_money - origin_money) / origin_money
            stock_yield.append(all_today_yield)
            current_money = current_market_value + other_money
            buy_price = years_data.loc[index, 'close']
        if buy_in == 100:
            stock_yield.append(stock_yield[-1])
        if buy_in == 0:
            today_yield = (sell_price - buy_price) / buy_price
            current_market_value = current_market_value * (1 + today_yield)
            current_money = current_market_value + other_money
            all_today_yield = (current_market_value + other_money - origin_money) / origin_money
            stock_yield.append(all_today_yield)
            buy_in = 100
        dates.append(years_data.loc[index, 'date'].date())
    return dates, stock_yield


def days_overeise_average(stock_datas, index, days, average_days):
    for index_item in range(days):
        current_index = index - index_item - 1
        before_average = stock_datas.loc[(current_index-average_days+1):(current_index), 'close'].sum() / average_days
        if stock_datas.loc[current_index, 'close'] < before_average:
            return False
    return True
