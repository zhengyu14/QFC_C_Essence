import DataProvider as dp
import datetime as dttm

provider = dp.dataProvider()
provider.set_security_id_code('000905', 'XSHG')
#security_data = provider.get_security_data_min(dttm.datetime(2007,1,1,9,0,0),dttm.datetime(2007,2,5,15,0,0))
stock_code_list=provider.get_index_stocks()