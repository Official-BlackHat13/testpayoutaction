from ..database_models.WebhookModel import WebhookModel
from ..database_service.Log_model_services import Log_Model_Service
from ..const import server_ip
class Webhook_Model_Service:
    def __init__(self,merchant_id,webhook):
        self.merchant_id=merchant_id
        self.webhook=webhook
    def save(self,client_ip_address)->int:
        log = Log_Model_Service(log_type="create",client_ip_address=client_ip_address,table_name="api_webhook_model",server_ip_address=server_ip,remarks="creating webhook record for merchant id :: "+self.merchant_id)
        
        webhook = WebhookModel()
        webhook.merchant_id=self.merchant_id
        webhook.webhook=self.webhook
        webhook.save()
        log.table_id=webhook.id
        log.save()
        return webhook.id
    @staticmethod
    def fetch_by_merchant_id(merchant_id,client_ip_address)->WebhookModel:
        log = Log_Model_Service(log_type="fetch",client_ip_address=client_ip_address,table_name="api_webhook_model",server_ip_address=server_ip,remarks="fetching webhook record for merchant id :: "+merchant_id)
        webhook = WebhookModel.objects.filter(merchant_id=merchant_id,status=True)
        if len(webhook)==0:
            return None
        return webhook[0]
        
        
