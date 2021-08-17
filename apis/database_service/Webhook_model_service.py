from datetime import datetime
from ..database_models.WebhookModel import WebhookModel
from ..database_service.Log_model_services import Log_Model_Service
from ..const import server_ip
class Webhook_Model_Service:
    def __init__(self,merchant_id=None,webhook=None,is_instant=None,is_interval=None,max_request=None,time_interval=None):
        self.merchant_id=merchant_id
        self.webhook=webhook
        self.is_instant=is_instant
        self.is_interval=is_interval
        self.max_request=max_request
        self.time_interval=time_interval
    def save(self,client_ip_address,admin_id)->int:
        log = Log_Model_Service(log_type="create",client_ip_address=client_ip_address,table_name="api_webhook_model",server_ip_address=server_ip,remarks="creating webhook record for merchant id :: "+str(self.merchant_id))
        
        webhook = WebhookModel()
        webhook.merchant_id=self.merchant_id
        webhook.webhook=self.webhook
        webhook.status = True
        webhook.is_instant=self.is_instant
        webhook.is_interval=self.is_interval
        webhook.max_request=self.max_request
        webhook.time_interval=self.time_interval
        webhook.created_by = "admin id :: "+str(admin_id)
        resp = WebhookModel.objects.filter(merchant_id=self.merchant_id,webhook=self.webhook)
        if(len(resp)!=0):
            return 0
        webhook.save()
        log.table_id=webhook.id
        log.save()
        return 1
    @staticmethod
    def fetch_by_merchant_id(merchant_id,client_ip_address)->WebhookModel:
        log = Log_Model_Service(log_type="fetch",client_ip_address=client_ip_address,table_name="api_webhook_model",server_ip_address=server_ip,remarks="fetching webhook record for merchant id :: "+str(merchant_id))
        webhook = WebhookModel.objects.filter(merchant_id=merchant_id,status=True).values()
        if len(webhook)==0:
            return None
        resp = {
            "merchant_id":webhook[0].get("merchant_id"),
            "webhook":webhook[0].get("webhook"),
            "is_instant":webhook[0].get("is_instant"),
            "is_interval":webhook[0].get("is_interval"),
            "max_request":webhook[0].get("max_request"),
            "time_interval":webhook[0].get("time_interval")
        }
        return resp
    @staticmethod
    def deleteWebhookByMerchantId(admin_id,merchant_id, webhook):
        webhook = WebhookModel.objects.filter(merchant_id=merchant_id,status=True,webhook=webhook)
        if len(webhook)==0:
            return 0
        webhook[0].status=False
        webhook[0].deleted_by="admin id :: "+str(admin_id)
        webhook[0].deleted_at= datetime.now()
        webhook[0].save()