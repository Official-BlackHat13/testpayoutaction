from ..database_models.IpWhiteListedModel import IpWhiteListedModel
from ..database_service.Log_model_services import Log_Model_Service
from .. import const
class IpWhiteListing_Model_Service:
    def __init__(self,merchant_id=None,ip_add=None,clientip=None):
        self.merchant_id = merchant_id
        self.ip_add=ip_add
        self.clientip=clientip
    def save(self)->int:
        # log = Log_Model_Service(log_type="create",client_ip_address=self.clientip,server_ip_address=const.server_ip,table_name="apis_ipwhitelistedmodel",remarks="adding records into apis_ipwhitelistedmodel")
        
        ipmodel = IpWhiteListedModel()
        ipmodel.merchant_id=self.merchant_id
        ipmodel.ip_address=self.ip_add
        ipmodel.created_by = "merchant id :: "+self.merchant_id
        ipmodel.save()
        # log.table_id=ipmodel.id
        # log.save()
        return ipmodel.id
    @staticmethod
    def saveMultipleIp(merchant_id,ips,clientip)->bool:
        log = Log_Model_Service(log_type="create multiple records",client_ip_address=clientip,server_ip_address=const.server_ip,table_name="apis_ipwhitelistedmodel",remarks="adding records into apis_ipwhitelistedmodel")
        log.save()
        for ip in ips:
            print("ip --> "+ip)
            IpWhiteListing_Model_Service(merchant_id=merchant_id,ip_add=ip,clientip=clientip).save()
        return True
    
    def deleteIp(self):
        ipModel = IpWhiteListedModel
        try:
            ipModel = IpWhiteListedModel.objects.get(merchant_id=self.merchant_id,ip_address=self.ip_add)
        except IpWhiteListedModel.DoesNotExist:
            return 0
        ipModel.status = False
        ipModel.save()
        return 1