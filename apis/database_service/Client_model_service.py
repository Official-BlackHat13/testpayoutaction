from ..models import MerchantModel as ClientModel
from . import Log_model_services
from .. import const
class Client_Model_Service:
    def __init__(self,client_id=None,client_code=None,role_id=None,auth_key=None,user=None,auth_iv=None,bank_id=None,client_username=None,client_password=None):
        self.client_id=client_id
        self.client_code=client_code
        self.auth_key=auth_key
        self.user = user
        self.auth_iv=auth_iv
        self.bank_id=bank_id
        self.client_username=client_username
        self.role_id=role_id
        self.client_password=client_password
        
    def save(self,client_ip_address,created_by)->int:
        log_service=Log_model_services.Log_Model_Service(log_type="create",table_name="apis_clientmodel",remarks="saving records in apis_clientmodel table",client_ip_address=client_ip_address,server_ip_address=const.server_ip,created_by=created_by)
        
        clientmodel=ClientModel()
        clientmodel.client=self.client_id
        clientmodel.client_code=self.client_code
        clientmodel.auth_key=self.auth_key
        clientmodel.role=self.role_id
        clientmodel.auth_iv=self.auth_iv
        clientmodel.bank=self.bank_id
        clientmodel.client_username=self.client_username
        clientmodel.client_password=self.client_password
        clientmodel.user = self.user
        clientmodel.save()
        log_service.table_id=clientmodel.id
        log_service.save()
        return clientmodel.id
    @staticmethod
    def fetch_by_id(id,client_ip_address,created_by)->ClientModel:
        log_service=Log_model_services.Log_Model_Service(log_type="fetch",table_name="apis_clientmodel",remarks="fetching records in apis_clientmodel table by primary key id",client_ip_address=client_ip_address,server_ip_address=const.server_ip,created_by=created_by)
        
        clientModel=ClientModel.objects.get(id=id,status=True)
        model=clientModel
        log_service.table_id=model.id
        log_service.save()
        return model
    @staticmethod
    def fetch_by_clientid(client_id,client_ip_address,created_by)->ClientModel:
        log_service=Log_model_services.Log_Model_Service(log_type="fetch",table_name="apis_clientmodel",remarks="fetching records in apis_clientmodel table by client id",client_ip_address=client_ip_address,server_ip_address=const.server_ip,created_by=created_by)
        
        clientModels=ClientModel.objects.filter(client=client_id,status=True)
        model=clientModels[0]
        log_service.table_id=model.id
        log_service.save()
        return model
    @staticmethod
    def fetch_by_clientcode(client_code,client_ip_address,created_by)->ClientModel:
        log_service=Log_model_services.Log_Model_Service(log_type="fetch",table_name="apis_clientmodel",remarks="fetching records in apis_clientmodel table by client code",client_ip_address=client_ip_address,server_ip_address=const.server_ip,created_by=created_by)
        log_service.save()
        clientModel=ClientModel.objects.filter(client_code=client_code,status=True)
        model=clientModel[0]
        return model
    @staticmethod
    def fetch_all_by_clientcode(client_code,client_ip_address,created_by)->ClientModel:
        log_service=Log_model_services.Log_Model_Service(log_type="fetch",table_name="apis_clientmodel",remarks="fetching all records in apis_clientmodel table by client code",client_ip_address=client_ip_address,server_ip_address=const.server_ip,created_by=created_by)
        log_service.save()
        clientModel=ClientModel.objects.filter(client_code=client_code,status=True)
        return clientModel
    