import pandas as pd
import numpy as np
import math
from jqlib.alpha101 import *
from sklearn.svm import SVR, LinearSVC, SVC
from sklearn.model_selection import GridSearchCV  
from sklearn.model_selection import learning_curve
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import Ridge
from sklearn.linear_model import BayesianRidge

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
    set_order_cost(OrderCost(close_tax=0, open_commission=0, close_commission=0, min_commission=0), type='stock')
    
    
def trade(context):
    if g.days % 7 == 0:
        stock_list_all = get_index_stocks('000300.XSHG', date = None)
        q = query(valuation.code, valuation.market_cap).filter(valuation.code.in_(stock_list_all))
        df = get_fundamentals(q, date = None)
        #df.columns = ['code', 'log_mcap', 'alpha_037', 'alpha_035', 'alpha_017', 'alpha_018', 'alpha_012']
        df.columns = ['code', 'log_mcap']
        
        Factor1 = alpha_037(context.current_dt.date(), stock_list_all)
        Factor2 = alpha_035(context.current_dt.date(), stock_list_all)
        Factor3 = alpha_017(context.current_dt.date(), stock_list_all)
        Factor4 = alpha_038(context.current_dt.date(), stock_list_all)
        Factor5 = alpha_012(context.current_dt.date(), stock_list_all)
        
        df['log_mcap'] = np.log(df['log_mcap'])
        
        df = df.set_index('code')
        #df.index = df.code.values
        #del df['code']
        
        df['Factor1'] = Factor1
        df['Factor2'] = Factor2
        df['Factor3'] = Factor3
        df['Factor4'] = Factor4
        df['Factor5'] = Factor5
        
        
        df = df.fillna(0)
        #df[df>10000] = 10000
        #df[df<-10000] = -10000

            
        X = df[['Factor1','Factor2','Factor3','Factor4','Factor5']]
        Y = df[['log_mcap']]
        X = X.fillna(0)
        Y = Y.fillna(0)
        
        #Bayes
        #brg = BayesianRidge(compute_score=True)
        #brg.fit(X, Y)
        
        #svr
        #svr = SVR(kernel='rbf', gamma=0.1) 
        #model = svr.fit(X, Y)
        
        # RandomForest
        #rnd = RandomForestRegressor(n_estimators=500, n_jobs=-1, random_state=123)
        #rnd.fit(X,Y)
        
        # RidgeRegression
        rdg = Ridge()
        rdg.fit(X,Y)
        
        
        factor = Y - pd.DataFrame(rdg.predict(X), index = Y.index, columns = ['log_mcap'])
        factor = factor.sort_values(by = 'log_mcap')
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
            