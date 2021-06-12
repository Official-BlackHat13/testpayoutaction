from ..models import BankModel
class Bank_model_services:
    def __init__(self,bank_name=None,bank_code=None,nodal_account_number=None,nodal_ifsc=None,nodal_account_name=None):
        self.bank_name=bank_name
        self.bank_code=bank_code
        self.nodal_account_number=nodal_account_number
        self.nodal_ifsc=nodal_ifsc
        self.nodal_account_name=nodal_account_name
    def save(self):
        bankModel=BankModel()
        bankModel.bank_name=self.bank_name
        bankModel.bank_code=self.bank_code
        bankModel.nodal_account_number=self.nodal_account_number
        bankModel.nodal_ifsc=self.nodal_ifsc
        bankModel.nodal_account_name=self.nodal_account_name
        bankModel.save()
        return True
    def fetch_by_bankcode(self):
        bankModel=BankModel.objects.filter(bank_code=self.bank_code)
        return bankModel[0]
    def fetch_by_id(self,id):
        bankModel=BankModel.objects.get(id=id)
        return True