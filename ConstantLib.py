# Constants

import jqdatasdk as jqd

'''
JQData platform
'''
jqDataID = '18068008158'
jqDataPassword = 'Yu19920125'
jqDataFreqDaily = 'daily'
jqDataFreqMin = 'minute'

securityIDCode000001XSHE = '000001.XSHE'

'''
Tinysoft platform
'''
tinysoftServer = 'tsl.tinysoft.com.cn'
tinysoftPort = 443
tinysoftID = 'axzq'
tinysoftPassword = 'ax888888'

tinysoftAlphaCols = ['Alpha003','Alpha004','Alpha005','Alpha006','Alpha008', 
                    'Alpha011','Alpha012','Alpha013','Alpha014','Alpha015', 
                    'Alpha018','Alpha019','Alpha021','Alpha022','Alpha023',
                    'Alpha024','Alpha025','Alpha026','Alpha028','Alpha030']

'''
Message text
'''
msgInvalidSecurityIDCode = 'Invalid security ID or code.'
msgLoginTinysoftFailed = 'Failed to log-in Tinysoft.'

'''
Factor name
'''
factorPbRatio = jqd.valuation.pb_ratio
factorCirculatingMarketCap = jqd.valuation.circulating_market_cap