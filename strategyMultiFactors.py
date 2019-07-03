# 导入函数库
from jqdata import *
from jqfactor import Factor, calc_factors
from jqlib.alpha101 import *
import datetime
import pandas as pd
import numpy as np

# Constants
cnst_index = '000300.XSHG'
cnst_factor_name_boll_down = 'boll_down'
cnst_col_name_close = 'close'


# 策略初始化
def initialize(context):
    set_benchmark(cnst_index)
    set_option('use_real_price', True)
    log.set_level('order', 'error')
    set_order_cost(OrderCost(close_tax=0, open_commission=0, close_commission=0, min_commission=0), type='stock')
    # Monthly portfolio reallocation
    run_monthly(market_open, 1, time='open', reference_security=cnst_index)

'''
######################策略的交易逻辑######################
每周计算因子值， 并买入前 20 支股票
'''

# Reallocate portflio monthly when market opens
def market_open(context):
    
    # 1. 定义计算因子的 universe，
    #    建议使用与 benchmark 相同的指数，方便判断选股带来的 alpha
    stock_list_all = get_index_stocks(cnst_index)

    # 2. 获取因子值
    #    get_factor_values 有三个参数，context、因子列表、股票池，
    #    返回值是一个 dict，key 是因子类的 name 属性，value 是 pandas.Series
    #    Series 的 index 是股票代码，value 是当前日期能看到的最新因子值
    '''
    factor_values = get_factor_values(context, [ALPHA013(),ALPHA015(), GROSS_PROFITABILITY()], universe)

    alpha013 = factor_values['alpha013']
    alpha015 = factor_values['alpha015']
    gross_profitability = factor_values['gross_profitability']
    '''

    # 3. 对因子做线性加权处理， 并将结果进行排序。您在这一步可以研究自己的因子权重模型来优化策略结果。
    #    对因子做 rank 是因为不同的因子间由于量纲等原因无法直接相加，这是一种去量纲的方法。
    final_factor = alpha_001(context.current_dt.date(), stock_list_all)

    # 4. 由因子确定每日持仓的股票列表：
    #    采用因子值由大到小排名前 20 只股票作为目标持仓
    try:
        stock_list = list(final_factor.sort_values(ascending=False)[:20].index)
    except:
        stock_list = list(final_factor.order(ascending=False)[:20].index)

    # 5. 根据股票列表进行调仓：
    #    这里采取所有股票等额买入的方式，您可以使用自己的风险模型自由发挥个股的权重搭配
    rebalance_position(context, stock_list)

'''
Utilities
    1. Short stocks not in stock_list
    2. Long stocks in stock_list with same values
'''
def rebalance_position(context, stock_list):
    current_holding = context.portfolio.positions.keys()
    stocks_to_sell = list(set(current_holding) - set(stock_list))
    # 卖出
    bulk_orders(stocks_to_sell, 0)
    total_value = context.portfolio.total_value

    # 买入
    bulk_orders(stock_list, total_value/len(stock_list))

# 批量买卖股票
def bulk_orders(stock_list,target_value):
    for i in stock_list:
        order_target_value(i, target_value)

"""
# 策略中获取因子数据的函数
每日返回上一日的因子数据
详见 帮助-单因子分析
"""
def get_factor_values(context,factor_list, universe):
    """
    输入： 因子、股票池
    返回： 前一日的因子值
    """
    # 取因子名称
    factor_name = list(factor.name for factor in factor_list)

    # 计算因子值
    values = calc_factors(universe,
                        factor_list,
                        context.previous_date,
                        context.previous_date)
    # 装入 dict
    factor_dict = {i:values[i].iloc[0] for i in factor_name}
    return factor_dict