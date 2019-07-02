# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import math

import jqdata

def initialize(context):
    set_params()
    set_backtest()
    run_daily(trade, 'every_bar')
    
def set_params():
    g.days = 0
    g.refresh_rate = 10
    g.stocknum = 10
    
def set_backtest():
    set_benchmark('000001.XSHG')
    set_option('use_real_price', True)
    log.set_level('order', 'error')
    
def trade(context):
    if g.days % 10 == 0:
        sample = get_index_stocks('000001.XSHG', date = None)
        q = query(valuation.code, valuation.pb_ratio).filter(valuation.code.in_(sample))
        df = get_fundamentals(q, date = None)
        df.columns = ['code', 'pb_ratio']
        
        df.index = df.code.values
        del df['code']
        df = df.fillna(0)
        
        mean = df.mean()['pb_ratio']
        std = df.std()['pb_ratio']
        
        df = df[df.pb_ratio<mean+3*std] 
        df = df[df.pb_ratio > mean-3*std]
        
        factor = df.sort_values(by = 'pb_ratio')
        
        stockset = list(factor.index[:10])
        sell_list = list(context.portfolio.positions.keys())
        for stock in sell_list:
            if stock not in stockset[:g.stocknum]:
                stock_sell = stock
                order_target_value(stock_sell, 0)
            
        if len(context.portfolio.positions) < g.stocknum:
            num = g.stocknum - len(context.portfolio.positions)
            cash = context.portfolio.cash/num
        else:
            cash = 0
            num = 0
        for stock in stockset[:g.stocknum]:
            if stock in sell_list:
                pass
            else:
                stock_buy = stock
                order_target_value(stock_buy, cash)
                num = num - 1
                if num == 0:
                    break
        g.days += 1
    else:
        g.days = g.days + 1    
            