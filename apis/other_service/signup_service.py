from ..database_service import Client_model_service,Bank_model_services,IpWhitelisting_model_service
from .. import const
import requests
from django.contrib.auth.models import User
from ..Utils import randomstring
class Signup_Service:
    def __init__(self,user=None,client_ip_address=None):
        self.user= user
        self.client_ip_address=client_ip_address
    def SignUp(self):
        
        if(len(Client_model_service.Client_Model_Service.fetch_all_by_clientcode(self.user["client_code"],client_ip_address=self.client_ip_address,created_by="new user"))>0):
                raise Exception("Client Code Already Present")
        
        elif(len(Client_model_service.Client_Model_Service.fetch_by_email(self.user["email"],client_ip_address=self.client_ip_address,created_by="new user"))>0):
            raise Exception("Email already exist")
        
        # print(len(len_client_by_mail))
        user_client =User.objects.create_user(self.user["username"], self.user["email"],self.user["password"])
        bank=Bank_model_services.Bank_model_services.fetch_by_bankcode(self.user["bank_code"],client_ip_address=self.client_ip_address,created_by="client added")
        client = Client_model_service.Client_Model_Service(email=self.user["email"],role_id=self.user['role_id'],user=user_client.id,client_id=self.user['client_id'],client_code=self.user["client_code"],auth_key=randomstring.randomString(),auth_iv=randomstring.randomString(),bank_id=bank.id,client_username=self.user["username"],client_password=self.user["password"])
        merchant_id=client.save(client_ip_address=self.client_ip_address,created_by="client added")
        print("requesting api "+const.domain+"api/token/")
        res = requests.post(const.domain+"api/token/",json={"username":self.user["username"],"password":self.user["password"]})
        print("response from json")
        print(res.json())
        IpWhitelisting_model_service.IpWhiteListing_Model_Service.saveMultipleIp(merchant_id=merchant_id,ips=self.user["ip_addresses"],clientip=self.client_ip_address)
        return {"client":client,"merchant_id":merchant_id,"token":res}    