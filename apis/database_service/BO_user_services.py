from ..models import BOUserModel

from . import Log_model_services
from .. import const

class BO_User_Service:
    def __init__(self,roleid=None,username=None,password=None,name=None,auth_key=None,auth_iv=None,email=None,mobile=None):
        self.roleid=roleid
        self.username=username
        self.password=password
        self.name=name
        self.email=email
        self.auth_key=auth_key
        self.auth_iv=auth_iv
        self.mobile=mobile
    def save(self,client_ip_address,created_by):
        bouser = BOUserModel()
        bouser.role=self.roleid
        bouser.username=self.username
        bouser.password=self.password
        bouser.name=self.name
        bouser.email=self.email
        bouser.auth_key=self.auth_key
        bouser.auth_iv=self.auth_iv
        bouser.mobile=self.mobile
        bouser.save()
        return bouser.id
    @staticmethod
    def fetch_by_name(name,client_ip_address,created_by):
        bouser=BOUserModel.objects.filter(name=name)
        
        return bouser
    @staticmethod
    def fetch_by_name(email,client_ip_address,created_by):
        bouser=BOUserModel.objects.filter(email=email)
        
        return bouser
    @staticmethod
    def fetch_by_username_password(username,password,client_ip_address,created_by):
        bouser = BOUserModel.objects.filter(username=username,password=password)
        return bouser
    @staticmethod
    def fetch_user_type(id):
        bouser = BOUserModel.objects.get(id=id)
        if bouser == None:
            return None
        return bouser.role
    @staticmethod
    def fetch_by_id(id):
        try:
         bouser = BOUserModel.objects.get(id=id)
         return bouser
        except Exception as e:
            return None

    
        