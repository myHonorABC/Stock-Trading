import pandas as pd
from matplotlib import pyplot as plt
from ballstock_download import download_data
import baostock as bs
import datetime
from stock_strategy import days_overrise1, surplus_line1, double_average_line1


class StockDeal(object):
    def __init__(self, stock_code, strategy_nu, is_buy):
        self.stock_code = stock_code
        self.strategy_nu = strategy_nu
        self.is_buy = is_buy

    def buy_and_sell(self):
        '''
        股票买入与卖出策略选择
        :return:
        '''
        if self.strategy_nu == 1:
            self.double_average_ac(self.stock_code, 5, 15, 2)
        if self.strategy_nu == 2:
            self.price_overide_ac(self.stock_code, 3, 2)
        if self.strategy_nu == 3:
            self.before_override_down(self.stock_code, 3, 2)

    def sell_amount_volume(self, years_data, loss_days):
        '''
        明天成交额除以成交量的值小于前loss_days天成交额除以成交量的最大值时卖出
        :param years_data: 股票历史数据
        :param loss_days: 股票卖出参考天数
        :return:
        '''
        return (years_data.loc[(years_data.shape[0]-loss_days):(years_data.shape[0]-1), 'amount'] / years_data.loc[(years_data.shape[0]-loss_days):(years_data.shape[0]-1), 'volume']).max()

    def double_average_ac(self, stock_code, average, second_average, days):
        '''
        策略1：均价average高于均价second_average时买入；当天收盘前10分钟成交额除以成交量的值
        :param stock_code: 股票代码
        :param average: 第一个均价
        :param second_average: 第二个均价
        :param days: 卖出比较天数
        :return:
        '''
        stock_datas = pd.read_csv('./stk_data/d/{}.csv'.format(stock_code), encoding='gbk')
        stock_datas.sort_values(by='date')
        stock_datas = stock_datas[stock_datas['close'] != 0]
        stock_datas['date'] = pd.to_datetime(stock_datas.date, format="%Y/%m/%d")
        years_data = stock_datas
        years_data.reset_index(drop=True, inplace=True)
        if self.is_buy == 0:
            average_price = years_data.loc[(years_data.shape[0]-average):(years_data.shape[0]-1), 'close'].sum() / average
            second_average_price = years_data.loc[(years_data.shape[0]-second_average):(years_data.shape[0]-1), 'close'].sum() / second_average
            if average_price > second_average_price:
                print('明天以开盘价买入{}股票！'.format(self.stock_code))
            else:
                print('不满足条件，不买入股票！')
        else:
            sell_ac = self.sell_amount_volume(years_data, days)
            print('前{}天额量比的最大值为{},明天收盘前5分钟额量比小于该值时卖出'.format(days, sell_ac))

    def price_overide_ac(self, stock_code, days, loss_days):
        '''
        策略2：明天股票价格突破前days天的最高价时买入；明天成交额除以成交量的值小于前loss_days天成交额除以成交量的最大值时卖出
        :param stock_code: 股票代码
        :param days: 买入参考天数
        :param loss_days: 卖出参考天数
        :return:
        '''
        stock_datas = pd.read_csv('./stk_data/d/{}.csv'.format(stock_code), encoding='gbk')
        stock_datas.sort_values(by='date')
        stock_datas = stock_datas[stock_datas['close'] != 0]
        stock_datas['date'] = pd.to_datetime(stock_datas.date, format="%Y/%m/%d")
        years_data = stock_datas
        years_data.reset_index(drop=True, inplace=True)
        if self.is_buy == 0:
            days_max_price = years_data.loc[(years_data.shape[0]-days):(years_data.shape[0]-1), 'high'].max()
            print('明天股票{}的价格高于{}时买入, 开盘价格高时直接买入'.format(stock_code, days_max_price))
        else:
            sell_ac = self.sell_amount_volume(years_data, loss_days)
            print('前{}天额量比的最大值为{},明天收盘前5分钟额量比小于该值时卖出'.format(loss_days, sell_ac))

    def before_override_down(self, stock_code, days, loss_days):
        '''
        策略3：明天股价突破突破前days天的最高价时买入；明天股价到达前loss_days天的最低价时卖出
        :param stock_code: 股票代码
        :param days: 买入参考日
        :param loss_days: 卖出参考日
        :return:
        '''
        stock_datas = pd.read_csv('./stk_data/d/{}.csv'.format(stock_code), encoding='gbk')
        stock_datas.sort_values(by='date')
        stock_datas = stock_datas[stock_datas['close'] != 0]
        stock_datas['date'] = pd.to_datetime(stock_datas.date, format="%Y/%m/%d")
        years_data = stock_datas
        years_data.reset_index(drop=True, inplace=True)
        if self.is_buy == 0:
            before_max_price = years_data.loc[years_data.shape[0]-days, 'high']
            print('明天股票{}的价格高于{}时买入， 开盘价格高时'.format(stock_code, before_max_price))
        else:
            before_min_price = years_data.loc[years_data.shape[0]-loss_days, 'low']
            print('明天股票{}的价格到达{}时卖出，如果全天价格小于{}收盘前5分钟卖出'.format(stock_code, before_min_price, before_min_price))


def get_stock_datas(stock_code, mode):
    stock_datas = pd.read_csv('./stk_data/{}/{}.csv'.format(mode,stock_code))
    stock_datas.sort_values(by='date')
    stock_datas = stock_datas[stock_datas['close'] != 0]
    stock_datas['date'] = pd.to_datetime(stock_datas.date, format="%Y/%m/%d")
    years_data = stock_datas
    years_data.reset_index(drop=True, inplace=True)
    return years_data


if __name__ == '__main__':
    stock_code = 'sz.000012'
    # bs.login()
    # download_data([stock_code])
    # bs.logout()
    strategy_nu = 3
    is_buy = 0
    stock_deal = StockDeal(stock_code, strategy_nu, is_buy)
    stock_deal.buy_and_sell()
    start_date = datetime.datetime.strptime('19900101', '%Y%m%d')
    # end_date = datetime.datetime.strptime('20181231', '%Y%m%d')
    end_date = datetime.datetime.today()
    stock_datas = get_stock_datas(stock_code, 'd')
    datas = None
    stock_yield = None
    if strategy_nu == 1:
        dates, stock_yield = double_average_line1(stock_datas, start_date, end_date, 5, 15, 2)
    elif strategy_nu == 2:
        dates, stock_yield = days_overrise1(stock_datas, start_date, end_date, 3, 2, 0.002)
    elif strategy_nu == 3:
        dates, stock_yield = surplus_line1(stock_datas, start_date, end_date, 3, 3)
    plt.plot(dates, stock_yield, color='red')
    plt.show()
