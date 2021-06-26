from ..models import LedgerModel
from django.db import connection

class Ledger_Model_Service:
    def __init__(self,client_id=None,client_code=None,type_status=None,amount=None,van=None,trans_type=None,status=None,bank_ref_no=None,customer_ref_no=None,bank_id=None,trans_time=None,bene_account_name=None,bene_account_number=None,bene_ifsc=None,request_header=None):
        self.client_id=client_id
        self.client_code=client_code
        self.amount=amount
        self.trans_type=trans_type
        self.status=status
        self.bank_ref_no=bank_ref_no
        self.customer_ref_no=customer_ref_no
        self.bank_id=bank_id
        self.trans_time=trans_time
        self.type_status=type_status
        self.bene_account_name=bene_account_name
        self.bene_account_number=bene_account_number
        self.bene_ifsc=bene_ifsc
        self.request_header=request_header

        self.van=van
    def save(self):
        ledgermodel = LedgerModel()
        ledgermodel.client=self.client_id
        ledgermodel.client_code=self.client_code
        ledgermodel.amount=self.amount
        ledgermodel.trans_type=self.trans_type
        ledgermodel.type_status=self.type_status
        ledgermodel.trans_status=self.status
        ledgermodel.bank_ref_no=self.bank_ref_no
        ledgermodel.customer_ref_no=self.customer_ref_no
        ledgermodel.bank=self.bank_id
        ledgermodel.trans_time=self.trans_time
        ledgermodel.van=self.van
        ledgermodel.bene_account_name=self.bene_account_name
        ledgermodel.bene_account_number=self.bene_account_number
        ledgermodel.bene_ifsc=self.bene_ifsc
        ledgermodel.request_header=self.request_header
        
        ledgermodel.save()
        return ledgermodel.id
    def fetch_by_clientid(self,client_id):
        ledgerModels=LedgerModel.objects.filter(client=client_id)
        return ledgerModels
    def fetch_by_clientcode(self,client_code):
        ledgerModels=LedgerModel.objects.filter(client_code=client_code)
        return ledgerModels
    def fetch_by_id(self,id):
        ledgerModels=LedgerModel.objects.get(id=id)
        return ledgerModels
    def fetch_by_van(self,van):
        ledgerModels=LedgerModel.objects.filter(van=van)
        return ledgerModels
    def update_status(self,id,status):
        ledgerModel=LedgerModel.objects.get(id=id)
        ledgerModel.trans_status=status
        return ledgerModel
    def getBalance(self,clientCode):
        cursors = connection.cursor()
        cursors.execute("getBalance("+clientCode+",@balance)")
        cursors.execute("select @balance")
        value = cursors.fetchall()
        cursors.close()
        return value
