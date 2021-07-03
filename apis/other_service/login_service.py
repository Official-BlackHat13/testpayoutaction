from django.http import response
from ..database_service.Client_model_service import Client_Model_Service
from ..database_service.Otp_model_services import Otp_Model_Services
from ..Utils import randomstring
import requests
import threading
import time
from .. import const
class Login_service:
    def __init__(self,username=None,password=None,client_ip_address=None):
        self.username=username
        self.password=password
        self.client_ip_address=client_ip_address
    def login_request(self):
        client_model = Client_Model_Service.fetch_by_username_password(self.username,self.password,client_ip_address=self.client_ip_address,created_by="api call")
        print(client_model)
        if len(client_model)==0:
            print('if')
            return False
        else:
            print("else")
            user = client_model[0]
            rec=Client_Model_Service.get_user_type(user.id)
            # print(rec[0][0])
            otp = int(randomstring.randomNumber(6))
            otp_service = Otp_Model_Services(user_id=user.id,user_type=rec[0][0],email=user.email,otp=otp,otp_status="pending",verification_token=randomstring.randomString(30))
            id=otp_service.save()
            class ExpireOTP(threading.Thread):
                def run(self):
                    print("service_running")
                    time.sleep(5*60)
                    print("service_init")
                    Otp_Model_Services.update_status(id,"Expired")
                    print("service_done")
            
            response = requests.post(const.email_api,headers={"user-agent":"Application","Accept":"*/*","Content-Type":"application/json; charset=utf-8"},json={"toEmail": user.email,
  "toCc": "",
  "subject": "OTP for Sabpaisa Payout",
  "msg": "Please find the otp for your payout login request "+str(otp)})
            ExpireOTP().start()
            return otp_service.verification_token
    @staticmethod
    def login_verification(verification_token,otp):
        record = Otp_Model_Services.fetch_by_verification_token_with_otp(verification_token,otp)
        print(record)
        if record=="OTP Expired":
            return record
        elif len(record)==0:
            return False
        else:
            Otp_Model_Services.update_status(record[0].id,"Verified")
            return record[0].user
    @staticmethod
    def resend_otp(verification_token):
        record = Otp_Model_Services.fetch_by_verification_only(verification_token)
        user = Client_Model_Service.fetch_by_id(record[0].user,"cs","cs0")
        
        # print(record[0].user)
        token=Login_service(username=user.client_username,password=user.client_password,client_ip_address="ds").login_request()
        return token
        
        
