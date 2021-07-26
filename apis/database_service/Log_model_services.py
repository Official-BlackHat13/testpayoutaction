from logging import log
from ..models import LogModel
from datetime import datetime
import math
class Log_Model_Service:
    def __init__(self,log_type=None,client_ip_address=None,table_id=None,table_name=None,server_ip_address=None,remarks=None,full_request=None,created_by=None):
        
        self.log_type=log_type
        self.client_ip_address=client_ip_address
        self.server_ip_address=server_ip_address
        self.table_id = table_id
        self.table_name=table_name
        self.remarks = remarks
        self.full_request = full_request
        # self.full_response = full_response
        self.created_by=created_by
    def save(self)->int:
        logmodel = LogModel()
        logmodel.table_name=self.table_name
        logmodel.table_primary_id=self.table_id
        logmodel.log_type=self.log_type
        logmodel.client_ip_address=self.client_ip_address
        logmodel.server_ip_address=self.server_ip_address
        logmodel.remarks=self.remarks
        logmodel.full_request=self.full_request
        # logmodel.full_response=self.full_response
        logmodel.created_by=self.created_by
        logmodel.save()
        return logmodel.id
    @staticmethod
    def fetch_by_id(id)->LogModel:
        logmodel = LogModel.objects.get(id=id)
        return logmodel
    @staticmethod
    def update_response(id,response)->LogModel:
        logmodel = LogModel.objects.get(id=id)
        logmodel.full_response = response
        logmodel.updated_at=datetime.now()
        logmodel.save()
        return logmodel
    @staticmethod
    def fetch_all_logs_in_parts(page,length,start,end)->list:
        if start=="all" or end=="all":
         logmodel= LogModel.objects.all()
        else:
            # logmodel=LogModel.objects.filter(created_at__range=[start,end])
            logmodel=LogModel.objects.raw("select * from apis_logmodel where created_at between "+str(start)+" and "+str(end)+" limit "+str((page-1)*length)+" , "+str(page*length))
            print(logmodel.columns)
            def rec(rec):

                json = {"customer_ref_no":rec.customer_ref_no,"trans_completed_time":rec.trans_completed_time,"trans_init_time":rec.trans_init_time,"charge":rec.charge,"payment_mode":rec.payment_mode_id,"bene_account_name":rec.bene_account_name,"bene_account_number":rec.bene_account_number,"bene_ifsc":rec.bene_ifsc,"payout_trans_id":rec.payout_trans_id,"created_at":rec.created_at,"updated_at":rec.updated_at,"deleted_at":rec.deleted_at,"trans_amount_type":rec.trans_amount_type,"merchant_id":rec.merchant_id,"client_username":rec.client_username,"id":rec.id,"amount":rec.amount,"type_status":rec.type_status,"trans_type":rec.trans_type,}
                return json
        if length=="all":
            return logmodel
        if len(logmodel)==0:
            return logmodel
        length=int(length)
        splitlen = math.ceil(len(logmodel)/length)
        split_list = []
        for i in range(splitlen):
            split_list.append(logmodel[length*i:length*(i+1)])
        split_list.reverse()
        # print(split_list,splitlen)
        return [split_list,splitlen]


