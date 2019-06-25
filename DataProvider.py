import jqdatasdk as jqd
import ConstantLib as cl

class dataProvider:
    # Attributes
    securityIDCode = cl.securityIDCodeSP500INX # default as S&P 500
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
            self.log.append([message])
    
    # Set security ID & Code
    # If ID or code is not provided, S&P 500 is set as default
    def set_security_id_code(self, securityID, securityCode):
        if securityID is not None and securityCode is not None:
            self.securityIDCode = securityID + '.' + securityCode
    