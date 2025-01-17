import jqdatasdk as jqd
import ConstantLib as cl
import pandas as pd

class dataProvider:
    # Attributes
    securityIDCode = cl.securityIDCode000001XSHE # default as 000001.XSHE
    securityData = pd.DataFrame()
    allSecurityIndex  =  pd.DataFrame()
    log = []

    # Initialize instance
    def __init__(self):
        # Initialize attributes
        self.securityIDCode = cl.securityIDCode000001XSHE # default as 000001.XSHE
        self.securityData = pd.DataFrame()
        #self.alpha = pd.DataFrame(columns = [cl.tinysoftAlphaCols])
        self.log = []

    '''
    Public functions
    '''
    # Get log
    def get_log(self):
        return self.log

    # Set security ID & Code
    # If ID or code is not provided, S&P 500 is set as default
    def set_security_id_code(self, securityID, securityCode):
        if securityID is not None and securityCode is not None:
            self.securityIDCode = securityID + '.' + securityCode

    def get_index_stocks(self):
        self._login_jqdata()
        data = jqd.get_index_stocks(self.securityIDCode)
        self._logout_jqdata()
        return data

    def get_allSecurityIndex(self):
        self.allSecurityIndex = jqd.get_all_securities(['stock']).index # get all stock id

    # Get security data
    #   field: 'None' means default ['open', 'close', 'high', 'low', 'volume', 'money']
    #   skip_paused: 'True' means skipping none-trading date (停牌, 未上市或者退市后)
    #   fq: 复权选项: 'pre': 前复权; None: 不复权, 返回实际价格; 'post': 后复权
    def get_security_data_daily(self, startDate, endDate):
        self._login_jqdata()
        try:
            self.securityData = jqd.get_price(self.securityIDCode, start_date=startDate, end_date=endDate, frequency=cl.jqDataFreqDaily, fields=None, skip_paused=True, fq='post')
        except:
            self._add_log(cl.msgInvalidSecurityIDCode)
        self._logout_jqdata()
        return self.securityData

    def get_security_data_min(self, startDatetime, endDatetime):
        self._login_jqdata()
        try:
            self.securityData = jqd.get_price(self.securityIDCode, start_date=startDatetime, end_date=endDatetime, frequency=cl.jqDataFreqMin, fields=None, skip_paused=True, fq='post')
        except:
            self._add_log(cl.msgInvalidSecurityIDCode)
        self._logout_jqdata()
        return self.securityData

    # Get factor value of all stocks
    def get_Factor(self, date, factor_name):
        try:
            self.securityData = jqd.get_fundamentals(jqd.query
                                      (jqd.valuation.code,factor_name
                                       ).filter(
                                               #jqd.valuation.code == self.securityIDCode
                                               jqd.valuation.code.in_(self.allSecurityIndex)
                                               ), date) #2019-01-01'
        except:
            self._add_log(cl.msgInvalidSecurityIDCode)
        return self.securityData

    '''
    Private functions
    '''
    # Log-in JQData
    def _login_jqdata(self):
        # Authenticated when 'auth success' is shown
        jqd.auth(cl.jqDataID, cl.jqDataPassword)

    # Log-out JQData
    def _logout_jqdata(self):
        jqd.logout()

    # Log a new message
    def _add_log(self, message):
        if message != '':
            self.log.append(message)
