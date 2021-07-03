from ..database_models.OtpModel import OtpModel
from datetime import datetime,timedelta,timezone

class Otp_Model_Services:
    def __init__(self,user_id=None,user_type=None,verification_token=None,mobile=None,email=None,otp=None,expire_datetime=None,otp_status=None):
        self.user_id = user_id
        self.user_type=user_type
        self.verification_token=verification_token
        self.mobile=mobile
        self.email=email
        self.otp=otp
        self.expire_datetime=expire_datetime
        self.otp_status=otp_status
    def save(self)->int:
        otp_model = OtpModel()
        otp_model.user=self.user_id
        otp_model.user_type=self.user_type
        otp_model.verification_token=self.verification_token
        otp_model.mobile=self.mobile
        otp_model.email=self.email
        otp_model.otp=self.otp
        time_add= timedelta(minutes=5)
        otp_model.expire_datetime=datetime.now()+time_add
        otp_model.otp_status=self.otp_status
        otp_model.save()
        return otp_model.id
    @staticmethod
    def fetch_by_verification_token_with_otp(verification_token,otp):
        otp_model = OtpModel.objects.filter(verification_token=verification_token,otp_status="pending",otp=otp)
        dt=datetime.now()
        dt = dt.replace(tzinfo=timezone.utc)
        if(len(otp_model)>0 and otp_model[0].expire_datetime<dt):
            Otp_Model_Services.update_status(otp_model[0].id,"Expired")
            return "OTP Expired"
        return otp_model
    @staticmethod
    def fetch_by_verification_only(verification_token)->list:
        print("excuting")
        otp_model = OtpModel.objects.filter(verification_token=verification_token,otp_status="pending")
        
        return otp_model
    @staticmethod
    def update_status(id,status):
        otp_model = OtpModel.objects.filter(id=id,otp_status="pending")
        print(otp_model)
        if len(otp_model)>0:
         otp_model=otp_model[0]
         otp_model.otp_status=status
         otp_model.updated_at=datetime.now()
         otp_model.save()
        return True
    
