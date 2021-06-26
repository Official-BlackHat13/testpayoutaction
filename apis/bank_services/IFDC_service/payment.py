import requests
from bank_api import Idfc
class Payment:
    def __init__(self,message_header={},message_body={},environment="UAT"):
        self.message_header=message_header
        self.message_body=message_body
        self.environment=environment
    def hit(self):
        api=""
        if self.environment=="UAT":
            api=Idfc.uat_idfcPaymentAPI()
        else:
            api=Idfc.prod_idfcPaymentAPI()
        res = requests.post(api,json={"paymentTransactionReq":{"msgHdr":self.message_header,"msgBdy":self.message_body}})
        print(res.json())
        return res.json()