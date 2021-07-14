# from ..database_models.OtpModel import OtpModel
from ..database_models.SlabModel import SlabModel
from datetime import datetime,timedelta,timezone

class Slab_Model_Service:
    def __init__(self,merchant_id=None,min_amount=None,max_amount=None):
        self.merchant_id=merchant_id
        self.min_amount=min_amount
        self.max_amount=max_amount
    def save(self):
        slabmodel = SlabModel()
        slabmodel.merchant_id=self.merchant_id
        slabmodel.min_amount=self.min_amount
        slabmodel.max_amount=self.max_amount
        slabmodel.save()
    def fetch_by_id(id=None):
        slabmodel=SlabModel.objects.get(id=id)
        return slabmodel
    def check_slab(amount):
        slabmodel=SlabModel.objects.filter(max_amount__gt=amount,min_amount__lt=amount)
        if len(slabmodel)==0:
            return False
        return True


