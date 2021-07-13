from ..database_models.BeneficiaryModel import BeneficiaryModel

class Beneficiary_Model_Services:
    def __init__(self,full_name=None,account_number=None,ifsc_code=None,merchant_id=None):
        self.full_name=full_name
        self.account_number=account_number
        self.ifsc_code=ifsc_code
        self.merchant_id=merchant_id
    def save(self):
        beneficiarymodel = BeneficiaryModel()
        beneficiarymodel.full_name=self.full_name
        beneficiarymodel.account_number=self.account_number
        beneficiarymodel.ifsc_code=self.ifsc_code
        beneficiarymodel.merchant_id=self.merchant_id
        beneficiarymodel.save()
    @staticmethod
    def fetch_by_id(id):
        beneficiarymodel=BeneficiaryModel.objects.get(id=id)
        return beneficiarymodel
    @staticmethod
    def fetch_by_account_number_ifsc(merchant_id,account_number,ifsc):
        beneficiarymodel=BeneficiaryModel.objects.filter(merchant_id=merchant_id,account_number=account_number,ifsc_code=ifsc)
        if len(beneficiarymodel)==0:
            return None
        return beneficiarymodel
    def update(self,updated_by,updated_at,id,created_at):
        beneficiarymodel = BeneficiaryModel()
        beneficiarymodel.id = id
        beneficiarymodel.full_name=self.full_name
        beneficiarymodel.account_number=self.account_number
        beneficiarymodel.ifsc_code=self.ifsc_code
        beneficiarymodel.merchant_id=self.merchant_id
        beneficiarymodel.updated_at = updated_at
        beneficiarymodel.created_at=created_at
        beneficiarymodel.updated_by=updated_by
        beneficiarymodel.save()
    
    def fetchBeneficiaryByParams(self):
        if(self.ifsc_code!=None and self.account_number != None and self.merchant_id != None):
            resp = BeneficiaryModel.objects.filter(account_number=self.account_number,ifsc_code=self.ifsc_code,merchant_id=self.merchant_id).values()
            return list(resp)
        elif(self.ifsc_code!=None and self.account_number != None):
            resp = BeneficiaryModel.objects.filter(account_number=self.account_number,ifsc_code=self.ifsc_code).values()
            return list(resp)