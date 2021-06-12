from ..models import LedgerModel


class Ledger_Model_Service:
    def __init__(self,client_id=None,client_code=None,amount=None,trans_type=None,status=None,bank_ref_no=None,customer_ref_no=None,bank_id=None,trans_time=None):
        self.client_id=client_id
        self.client_code=client_code
        self.amount=amount
        self.trans_type=trans_type
        self.status=status
        self.bank_ref_no=bank_ref_no
        self.customer_ref_no=customer_ref_no
        self.bank_id=bank_id
        self.trans_time=trans_time
    def save(self):
        ledgermodel = LedgerModel()
        ledgermodel.client=self.client_id
        ledgermodel.client_code=self.client_code
        ledgermodel.amount=self.amount
        ledgermodel.trans_type=self.trans_type
        ledgermodel.status=self.status
        ledgermodel.bank_ref_no=self.bank_ref_no
        ledgermodel.customer_ref_no=self.customer_ref_no
        ledgermodel.bank=self.bank_id
        ledgermodel.trans_time=self.trans_time
        ledgermodel.save()
        return True
    def fetch_by_clientid(self,client_id):
        ledgerModels=LedgerModel.objects.filter(client=client_id)
        return ledgerModels
    def fetch_by_clientcode(self,client_code):
        ledgerModels=LedgerModel.objects.filter(client_code=client_code)
        return ledgerModels
    def fetch_by_id(self,id):
        ledgerModels=LedgerModel.objects.get(id=id)
        return True
