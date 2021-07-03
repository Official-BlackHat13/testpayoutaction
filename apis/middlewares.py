import requests
from apis.database_models.IpWhiteListedModel import IpWhiteListedModel
from apis.database_service.Client_model_service import Client_Model_Service
from . import models
from rest_framework.response import *
from django.shortcuts import HttpResponse
from datetime import datetime

# from .database_service.Log_model_services import Log_Model_Service
from . import const
def IpWhiteListed(get_response):
    def middleware(request):
        print(request.headers)
        ip=request.META['REMOTE_ADDR']
        try:
            if(request.path!="/api/" and request.path!="/" and "/admin/" not in request.path and request.path!="/api/auth/" and request.path not in "/api/token/" and const.merchant_check):
                if "merchant_id" not in request.headers:
                    print("not condition")
                    error_res=HttpResponse(str({"message":"merchant id not provided"}))
                    error_res['Content-Type'] = 'application/json'
                    return error_res
                
                merchant_id = request.headers["merchant_id"]
                clientmodel=Client_Model_Service.fetch_by_id(int(merchant_id),request.META['REMOTE_ADDR'],merchant_id)
                # if not clientmodel:
                #     raise Exception("Merchant id not valid")
                if "/api/getLogs/" in  request.path:
                    pass
                if not clientmodel.is_ip_checking:
                    response=get_response(request)
                    return response
                ipWhiteListedModel=models.IpWhiteListedModel.objects.filter(ip_address=ip,status=True,merchant=merchant_id)
            else:
             ipWhiteListedModel=models.IpWhiteListedModel.objects.filter(ip_address=ip,status=True)
            
                
        except Exception as e:
            error_res=HttpResponse(str({"message":e.args}))
            error_res['Content-Type'] = 'application/json'
            return error_res
        print("request -->>",request.path)
        if len(ipWhiteListedModel)==0 and const.ipwhitelisting:
            iprecords=models.IpHittingRecordModel()
            iprecords.ip_address=ip
            iprecords.ip_type="Blocked"
            iprecords.hitting_time=datetime.now()
            iprecords.save()
            ip_res=HttpResponse(str({"message":"IP Not Authorized"}))
            ip_res['Content-Type'] = 'application/json'
            return ip_res
        # iprecords=models.IpHittingRecordModel()
        # iprecords.ip_address=ip
        # iprecords.ip_type="Allowed"
        # iprecords.hitting_time=datetime.now()
        # iprecords.save()
        
        response=get_response(request)
        return response
    return middleware
# def Logs(get_response):
#     def middleware(req):
#         client_ip=req.META['REMOTE_ADDR']
#         server_ip = const.server_ip
#         request = request.__dic__
#         Log_Model_Service()
#         response = get_response(req)
#         return response
#     return middleware