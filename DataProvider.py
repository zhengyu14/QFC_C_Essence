import jqdatasdk as jqd
import ConstantLib as cl
import pandas as pd

class dataProvider:
    # Attributes
    securityIDCode = cl.securityIDCode000001XSHE # default as 000001.XSHE
    securityData = pd.DataFrame()
    log = []

    # Initialize instance and log-in JQData
    def __init__(self):
        # Authenticated when 'auth success' is shown
        jqd.auth(cl.jqDataID, cl.jqDataPassword)

    # Log-out JQData when max. connection (3) is reached
    def logout(self):
        jqd.logout()

    # Log a new message
    def add_log(self, message):
        if message != '':
            self.log.append(message)
    
    def get_log(self):
        return self.log
    
    # Set security ID & Code
    # If ID or code is not provided, S&P 500 is set as default
    def set_security_id_code(self, securityID, securityCode):
        if securityID is not None and securityCode is not None:
            self.securityIDCode = securityID + '.' + securityCode
    
    # Get security daily data
    #   field: 'None' means default ['open', 'close', 'high', 'low', 'volume', 'money']
    #   skip_paused: 'True' means skipping none-trading date (停牌, 未上市或者退市后)
    #   fq: 复权选项: 'pre': 前复权; None: 不复权, 返回实际价格; 'post': 后复权
    def get_security_daily_data(self, startDate, endDate):
        try:
            self.securityData = jqd.get_price(self.securityIDCode, start_date=startDate, end_date=endDate, frequency='daily', fields=None, skip_paused=True, fq='pre')
        except:
            self.add_log(cl.msgInvalidSecurityIDCode)
        return self.securityData
        

    