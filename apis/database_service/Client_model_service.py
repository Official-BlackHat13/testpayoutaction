from ..models import ClientModel
class Client_Model_Service:
    def __init__(self,client_id=None,client_code=None,auth_key=None,auth_iv=None,bank_id=None,client_username=None,client_password=None):
        self.client_id=client_id
        self.client_code=client_code
        self.auth_key=auth_key
        self.auth_iv=auth_iv
        self.bank_id=bank_id
        self.client_username=client_username
        self.client_password=client_password
    def save(self):
        clientmodel=ClientModel()
        clientmodel.client=self.client_id
        clientmodel.client_code=self.client_code
        clientmodel.auth_key=self.auth_key
        clientmodel.auth_iv=self.auth_iv
        clientmodel.bank=self.bank_id
        clientmodel.client_username=self.client_username
        clientmodel.client_password=self.client_password
        clientmodel.save()
        return True
    def fetch_by_clientid(self,client_id):
        clientModels=ClientModel.objects.filter(client=client_id)
        return clientModels[0]
    def fetch_by_clientcode(self,client_code):
        clientModel=ClientModel.objects.filter(client_code=client_code)
        return clientModel[0]