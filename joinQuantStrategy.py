# 导入函数库
from jqdata import *
from sklearn import linear_model
from sklearn.metrics import r2_score

# Constants
cnst_stock_num = 0
cnst_index = '000905.XSHG'
cnst_col_name_close = 'close'
cnst_r2_threshold = 0.7448547637992133

def initialize(context):
    set_benchmark(cnst_index)
    set_option('use_real_price', True)
    set_order_cost(OrderCost(close_tax=0.001, open_commission=0.0003, close_commission=0.0003, min_commission=5), type='stock')
    run_daily(market_open, time='10:30', reference_security=cnst_index)

def market_open(context):
    stock_list_all = get_index_stocks(cnst_index)

    # Process trend data
    if len(stock_list_all) == 0:
        return
    stock = stock_list_all[cnst_stock_num]
    # Get individual stock data from market open to 10:30
    trend_data = get_bars(stock, count=60, unit='1m', fields=[cnst_col_name_close])[cnst_col_name_close]
    if len(trend_data) == 0:
        return
    if get_r_square(trend_data) > cnst_r2_threshold and get_delta_price(trend_data) > 0:
        # Do long
        available_cash = context.subportfolios[0].available_cash
        if available_cash > 0:
            order_value(stock, available_cash)
    elif get_r_square(trend_data) > cnst_r2_threshold and get_delta_price(trend_data) < 0:
        # Do short
        order_target_value(stock, 0)

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