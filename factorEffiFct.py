# -*- coding: utf-8 -*-
import ConstantLib as cl
import pandas as pd

# this function is used to reallocation the portfolio to the target component
# id_target refer to a dataframe containing id that we expect to be included in the portfolio
# id_original refer to a dataframe containing id included in the present portfolio
def reallocate(id_target, id_original): 
    for i in range(0,len(id_original)): # short stocks that we no longer needed
        if id_original[i] not in id_target.values:
            ##### 卖出 id_original[i]
    
    ### 资金分配？
    '''
    if len(context.portfolio.positions) < g.stocknum:
            num = g.stocknum - len(context.portfolio.positions)
            cash = context.portfolio.cash/num
        else:
            cash = 0
            num = 0
    '''
    
            
    for i in range(0,len(id_target)): # long stocks that we want to include in the portfolio
        if id_target[i] not in id_orininal.values:
            ##### 买入 id_target[i]
            

# this function is designed to be use in back test, and it's only an one-period adjustment
def onePeriodAdj(factor_df): # df contains two columns, first is stock id, second is factor values
    factor_df.columns = ['stock_id', 'factor_value']
    factor_df = factor_df.sort_values(by=df.columns[1], ascending=False)
    numberInSubportfolio = int(len(factor_df)/10) # number of stocks in each subportfolio
    
    
    ### 如果不能整除，舍弃最后几条数据？
    
    # get target subportfolios' stock id
    portfolioTarget_df = pd.DataFrame(columns = cl.subPortfolioName)
    count_temp = 0
    for i in portfolioTarget_df.columns:
        portfolioTarget_df[i] = factor_df['stock_id'].iloc[count_temp*numberInSubportfolio:(count_temp+1)*numberInSubportfolio].values
        count_temp += 1
    del count_temp
    
    for i in portfolioTarget_df.columns:
        reallocate(portfolioTarget_df[i], portfolio_original[i])
        
        
# this function is used to test the efficiency of the factors
def factorEfficiencyTest(startDate,endDate, dpObject,factor_name):
    for i in range(startDate,endDate):
        factor_df = dpObject.get_Factor(i,factor_name)
        onePeriodAdj(factor_df)
    ### 获得10个subportfolio的return
    return subP_returns
    
    
    
    
