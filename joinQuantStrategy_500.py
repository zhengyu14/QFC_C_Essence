# 导入函数库
from jqdata import *
from sklearn import linear_model
from sklearn.metrics import r2_score

# Constants
cnst_index = '000905.XSHG'
cnst_col_name_close = 'close'
cnst_r2_threshold = 0.7448547637992133

def initialize(context):
    set_benchmark(cnst_index)
    set_option('use_real_price', True)
    set_order_cost(OrderCost(close_tax=0.001, open_commission=0.0003, close_commission=0.0003, min_commission=5), type='stock')
    run_daily(market_open, time='10:30', reference_security=cnst_index)

def market_open(context):
    stock_list_long=[]
    stock_list_short=[]
    stock_list_all = get_index_stocks(cnst_index)

    # Process trend data
    for stock in stock_list_all:
        # Get individual stock data from market open to 10:30
        trend_data = get_bars(stock, count=60, unit='1m', fields=[cnst_col_name_close])[cnst_col_name_close]
        if len(trend_data) == 0:
            break
        if get_r_square(trend_data) > cnst_r2_threshold and get_delta_price(trend_data) > 0:
            # LONG
            stock_list_long.append(stock)
        elif get_r_square(trend_data) > cnst_r2_threshold and get_delta_price(trend_data) < 0:
            # SHORT
            stock_list_short.append(stock)

    # Do long & short
    order(context, stock_list_long, stock_list_short)


def get_r_square(data):
    # Generate a virtual x-axis
    virtual_axis = []
    i = 0
    while i < len(data):
        virtual_axis.append([i])
        i += 1
    lnr_regr = linear_model.LinearRegression()
    lnr_regr.fit(virtual_axis,data)
    r_square = r2_score(data, lnr_regr.predict(virtual_axis))
    return r_square

def get_delta_price(trend_data):
    return trend_data[-1] - trend_data[0]

def order(context, long_list, short_list):
    # Do short
    if len(short_list) != 0:
        current_holding = context.portfolio.positions.keys()
        stocks_to_short = list(set(current_holding) & set(short_list))
        bulk_orders_target_value(stocks_to_short, 0)
        #total_value = context.portfolio.total_value

    # Do long
    if len(long_list) != 0:
        available_cash = context.subportfolios[0].available_cash
        bulk_orders_value(long_list, available_cash/len(long_list))

def bulk_orders_target_value(stock_list, target_value):
    for i in stock_list:
        order_target_value(i, target_value)

def bulk_orders_value(stock_list, value):
    for i in stock_list:
        order_value(i, value)