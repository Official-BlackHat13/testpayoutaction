from ..models import ChargeModel
from . import Log_model_services
from .. import const

class charge_model_service:
    def __init__(self,mode=None,min_amount=None,max_amount=None,charge_percentage_or_fix=None,charge=None,created_at=None,deleted_at=None,updated_at=None,merchant_id=None):
        self.min_amount=min_amount
        self.max_amount=max_amount
        self.charge_percentage_or_fix=charge_percentage_or_fix
        self.charge = charge
        self.created_at = created_at
        self.deleted_at=deleted_at
        self.updated_at = updated_at
        self.merchant_id = merchant_id
    def save(self,client_ip_address):
        log_service=Log_model_services.Log_Model_Service(log_type="create",table_name="apis_chargemodel",remarks="saving records in apis_chargemodel table",client_ip_address=client_ip_address,server_ip_address=const.server_ip,created_by="mechant id :: "+self.merchant_id)
        chargeModel = ChargeModel()
        chargeModel.min_amount = self.min_amount
        chargeModel.max_amount = self.max_amount
        chargeModel.charge_percentage_or_fix = self.charge_percentage_or_fix
        chargeModel.charge = self.charge
        chargeModel.created_at = self.created_at
        chargeModel.deleted_at = self.deleted_at
        chargeModel.updated_at = self.updated_at
        chargeModel.merchant_id= self.merchant_id
        chargeModel.save()
        log_service.table_id=chargeModel.id
        log_service.save()
        return chargeModel.id
    @staticmethod
    def fetch_by_id(id,client_ip_address,created_by,merchant_id):
        log_service=Log_model_services.Log_Model_Service(log_type="fetch",table_name="apis_chargemodel",remarks="fetching records from apis_chargemodel by primary key in the record",client_ip_address=client_ip_address,server_ip_address=const.server_ip,created_by=created_by)
        chargeModel=ChargeModel.objects.get(id=id,merchant_id=merchant_id)
        log_service.table_id=chargeModel.id
        log_service.save()
        return chargeModel
    # @staticmethod
    # def delete(id,client_ip_address,merchantId):
    #     log_service = Log_model_services.Log_Model_Service(log_type="delete", table_name="apis_chargemodel", remarks="deleting records in apis_chargemodel table",
    #                                                         client_ip_address=client_ip_address, server_ip_address=const.server_ip, created_by="merchant id :: "+merchantId)
    #     charge = ChargeModel.objects.filter(id=id,merchant=merchantId)
    #     if(len(charge) > 0):     
    #         chargermodel = ChargeModel()
    #         chargermodel = charge[0]  

        