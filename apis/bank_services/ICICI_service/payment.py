import requests
from bank_api import Icici
from ...bank_models.ICICI_Model import payment_request_model

class Payment:
    def __init__(self,body={}):
        self.header=payment_request_model.Header_Request()
        self.body=body
        self.details=Icici.icic_details()
        self.api_live=Icici.prod()
        self.api_uat=Icici.uat()
        self.key=Icici.key()
        self.header.Username=self.details["iciciImpsUserName"]
        self.header.Password=self.details["Password"]
        
    

    def payment_request_live(self):
        
        requests.post(self.api_live,json=self.body,headers=self.header.to_Json())

