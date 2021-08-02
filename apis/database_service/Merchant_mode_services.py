from ..database_models.MerchantModeModel import MercahantModeModel


class Merchant_Mode_Service:
    def __init__(self,merchant_id,bank_partner_id,mode_id):
        self.merchant_id=merchant_id
        self.bank_partner_id=bank_partner_id
        self.mode_id=mode_id
    def save(self):
        merchant_mode=MercahantModeModel()
        merchant_mode.merchant_id=self.merchant_id
        merchant_mode.bank_partner_id=self.bank_partner_id
        merchant_mode.mode_id=self.mode_id
        merchant_mode.save()
    @staticmethod
    def fetch_by_id(id):
        try:
            record=MercahantModeModel.objects.get(id=id)
            if record==None:
                return None
            return record
        except Exception as e:
            return None
    @staticmethod
    def fetch_by_merchant_id(merchant_id):
        record=MercahantModeModel.objects.filter(merchant_id=merchant_id)
        return record
    @staticmethod
    def fetch_by_merchant_id_and_mode(merchant_id,mode_id):
        record=MercahantModeModel.objects.filter(merchant_id=merchant_id,mode_id=mode_id)
        return record