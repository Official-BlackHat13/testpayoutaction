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
    def fetch_all_logs_in_parts(length,start,end)->list:
        if start=="all" or end=="all":
         logmodel= LogModel.objects.all()
        else:
            logmodel=LogModel.objects.filter(created_at__range=[start,end])
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


