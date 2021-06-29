from apis.database_models.IpWhiteListedModel import IpWhiteListedModel
from . import models
from rest_framework.response import *
from django.shortcuts import HttpResponse
from datetime import datetime
from . import const
def IpWhiteListed(get_response):
    def middleware(request):
        ip=request.META['REMOTE_ADDR']

        ipWhiteListedModel=models.IpWhiteListedModel.objects.filter(ip_address=ip,status=True)
        if len(ipWhiteListedModel)==0 and const.ipwhitelisting:
            iprecords=models.IpHittingRecordModel()
            iprecords.ip_address=ip
            iprecords.ip_type="Blocked"
            iprecords.hitting_time=datetime.now()
            iprecords.save()
            return HttpResponse(str({"message":"IP Not Authorized"}))
        # iprecords=models.IpHittingRecordModel()
        # iprecords.ip_address=ip
        # iprecords.ip_type="Allowed"
        # iprecords.hitting_time=datetime.now()
        # iprecords.save()
        
        response=get_response(request)
        return response
    return middleware
