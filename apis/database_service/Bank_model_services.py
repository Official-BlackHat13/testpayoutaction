from ..models import BankPartnerModel as BankModel
from . import Log_model_services
from .. import const
class Bank_model_services:
    def __init__(self,bank_name=None,bank_code=None,nodal_account_number=None,nodal_ifsc=None,nodal_account_name=None):
        self.bank_name=bank_name
        self.bank_code=bank_code
        self.nodal_account_number=nodal_account_number
        self.nodal_ifsc=nodal_ifsc
        self.nodal_account_name=nodal_account_name
    def save(self,client_ip_address,created_by):
        log_service=Log_model_services.Log_Model_Service(log_type="create",table_name="apis_bankpartnermodel",remarks="saving records in api_bankpartnermodel table",client_ip_address=client_ip_address,server_ip_address=const.server_ip,created_by=created_by)
        
        bankModel=BankModel()
        bankModel.bank_name=self.bank_name
        bankModel.bank_code=self.bank_code
        bankModel.nodal_account_number=self.nodal_account_number
        bankModel.nodal_ifsc=self.nodal_ifsc
        bankModel.nodal_account_name=self.nodal_account_name
        
        bankModel.save()
        log_service.table_id=bankModel.id
        log_service.save()
        return True
    @staticmethod
    def fetch_by_bankcode(bank_code,client_ip_address,created_by)->BankModel:
        log_service=Log_model_services.Log_Model_Service(log_type="fetch",table_name="apis_bankpartnermodel",remarks="fetching records from apis_bankpartnermodel by bank code",client_ip_address=client_ip_address,server_ip_address=const.server_ip,created_by=created_by)
        
        bankModel=BankModel.objects.filter(bank_code=bank_code)
        log_service.save()
        if len(bankModel)==0:
            return None
        return bankModel[0]
    @staticmethod
    def fetch_by_id(id,client_ip_address,created_by)->BankModel:
        log_service=Log_model_services.Log_Model_Service(log_type="fetch",table_name="apis_bankpartnermodel",remarks="fetching records from apis_bankpartnermodel by primary key in the record",client_ip_address=client_ip_address,server_ip_address=const.server_ip,created_by=created_by)
        
        bankModel=BankModel.objects.get(id=id)
        log_service.table_id=bankModel.id
        log_service.save()
        return bankModel