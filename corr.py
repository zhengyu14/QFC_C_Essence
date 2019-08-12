from jqdata import *
from jqfactor import Factor, calc_factors
from jqlib.alpha101 import *
import datetime
import pandas as pd
import numpy as np

def getAlpha(alpha,date):
    
    alpha_series = globals()[alpha](date,'000300.XSHG')
    
    return alpha_series

def assignFactorValue(alpha,date):
    Alpha = pd.Series(index = getAlpha(alpha,date).sort_values(ascending = False).index)
    Alpha[0:30] = 1
    Alpha[30:60] = 2
    Alpha[60:90] = 3
    Alpha[90:120] = 4
    Alpha[120:150] = 5
    Alpha[150:180] = 6
    Alpha[180:210] = 7
    Alpha[210:240] = 8
    Alpha[240:270] = 9
    Alpha[270:300] = 10
    
    return Alpha
def getSingleDateCorr(alphaName_list,date):
    df = pd.DataFrame(columns = alphaName_list, index = get_index_stocks('000300.XSHG', date=None))
    
    for alpha in alphaName_list:
        df[alpha] = assignFactorValue(alpha,date)
    
    df_corr = df.corr()
    
    return df_corr

def CorrAvg(corr_list):
    if len(corr_list) > 0:
        avg_list = corr_list[0]
    
    for i in range(1,len(corr_list)):
        avg_list += corr_list[i]
        
    return avg_list/len(corr_list)

def getPeriodCorr(startDate,endDate,alphaName_list):
    tradeDays = get_trade_days(start_date=startDate, end_date=endDate)
    
    i = 0
    corr_list = []
    
    while True: 
        
        if i >= len(tradeDays):
            break
        
        tempCorr_df = getSingleDateCorr(alphaName_list,str(tradeDays[i]))
        corr_list.append(tempCorr_df)     
        
        i += 7        
         
    return CorrAvg(corr_list)

getPeriodCorr('2014-06-01','2019-06-30',['alpha_033','alpha_038'])