import datetime

class Payment_Request_Model:
    def __init__(self,subwalletGuid=None,beneficiaryName=None,orderId=None,beneficiaryAccount=None,beneficiaryIFSC=None,amount=None,purpose=None,transfer_mode=None):
        self.subwalletGuid=subwalletGuid
        self.orderId=orderId
        self.beneficiaryName=beneficiaryName
        self.beneficiaryAccount=beneficiaryAccount
        self.beneficiaryIFSC=beneficiaryIFSC
        self.amount=amount
        self.purpose=purpose
        self.transfer_Mode = transfer_mode
        # self.date=date
    def to_json(self):
        # if self.transferMode=="RGTS" or self.transferMode=="NEFT":
        #      return {
        #     "subwalletGuid":self.subwalletGuid,
        #     "orderId":self.orderId,
        #     "beneficiaryName":self.beneficiaryName,
        #     "beneficiaryAccount":self.beneficiaryAccount,
        #     "beneficiaryIFSC":self.beneficiaryIFSC,
        #     "amount":self.amount,
        #     "transferMode":self.transfer_Mode,
        #     "purpose":self.purpose,
        #     "comments": "disbursal",
        #     "date":str(datetime.date.today())
        # }

        return {
            "subwalletGuid":self.subwalletGuid,
            "orderId":self.orderId,
            "beneficiaryAccount":self.beneficiaryAccount,
            "beneficiaryIFSC":self.beneficiaryIFSC,
            "amount":self.amount,
            "transferMode":self.transfer_Mode,
            "purpose":self.purpose,
            "comments": "disbursal",
            "date":str(datetime.date.today())
        }




