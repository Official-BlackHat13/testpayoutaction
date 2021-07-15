# from django.shortcuts import render
# Create your views here.


from django.db.models import query


from pyexcel_xls import get_data as xls_get
from pyexcel_xlsx import get_data as xlsx_get
from django.utils.datastructures import MultiValueDictKeyError
# from apis.database_models.Test import TestModel

from rest_framework.exceptions import server_error
# from apis.bank_services.IFDC_service import payment
from django.http import *
from rest_framework import generics
from django.shortcuts import *
from rest_framework.views import APIView
from rest_framework.response import *
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema

from apis.database_service import Beneficiary_model_services
from ..API_docs import payout_docs,auth_docs,login_docs,payoutTransactionEnquiry_docs,addBalance_docs,addBeneficiary_docs,log_docs
from datetime import datetime
from ..serializersFolder.serializers import LogsSerializer
#from .serializers import *
# from .models import *
import ast
from ..other_service import payout_service
from ..database_models import LedgerModel,ModeModel
from apis.database_service.Ledger_model_services import *
from django.http.response import JsonResponse
from apis.other_service.enquiry_service import *
from apis.database_service.Beneficiary_model_services import *
from ..database_service import Client_model_service,Bank_model_services
from rest_framework.parsers import JSONParser
from ..database_service import Client_model_service,Bank_model_services,IpWhitelisting_model_service
from django.contrib.auth.models import User
# from .database_service import Client_model_service,Ledger_model_services
from rest_framework.permissions import IsAuthenticated
from .. import const
from ..Utils import randomstring
from ..database_service import BO_user_services

from ..models import MerchantModel,RoleModel







# from .models import MerchantModel,RoleModel
from sabpaisa import auth

from datetime import datetime

from ..bank_services import ICICI_service

from ..other_service import login_service,signup_service


from sabpaisa import auth
from ..database_service.charge_model_service import charge_model_service
class addCharge(APIView):
    def post(self,request):
        query = request.headers.get("auth_token")
        merchantId = auth.AESCipher(const.AuthKey,const.AuthIV).decrypt(query)
        mode = request.data.get("mode")
        min_amount = request.data.get("min_amount")
        max_amount = request.data.get("max_amount")
        charge_percentage_or_fix = request.data.get("charge_percentage_or_fix")
        charge = request.data.get("charge")
        service = charge_model_service(merchant_id=merchantId,mode=mode,min_amount=min_amount,max_amount=max_amount,charge_percentage_or_fix=charge_percentage_or_fix,charge=charge)
        resp = service.save(client_ip_address=request.META['REMOTE_ADDR'])
        return Response({"message":"data saved","data":str(resp)},status=status.HTTP_200_OK)


class fetchCharges(APIView):
    def post(self,request):
        query = request.headers.get("auth_token")
        if(query==""):
            return Response({"message":"merchant id required"})
        id = request.data.get("chargeId")
        merchantId = auth.AESCipher(const.AuthKey,const.AuthIV).decrypt(query)
        service = charge_model_service()
        resp = service.fetch_by_id(id = id,client_ip_address=request.META['REMOTE_ADDR'],created_by="merchant id :: "+merchantId,merchant_id=merchantId)
        if(resp=="-1"):
            return Response({"message":"no data found","response_code":"1"},status=status.HTTP_404_NOT_FOUND)
        response = {
            "id":resp.get("id"),
            "mode id":resp.get("mode"),
            "min_amount":resp.get("min_amount"),
            "max_amount":resp.get("max_amount"),
            "charge_percentage_or_fix":resp.get("charge_percentage_or_fix"),
            "charge":resp.get("charge")
        }
        clientModel = Client_model_service.Client_Model_Service.fetch_by_id(
            id=merchantId, created_by="merchantid :: "+merchantId, client_ip_address=request.META['REMOTE_ADDR'])
        authKey = clientModel.auth_key
        authIV = clientModel.auth_iv
        encResp = auth.AESCipher(authKey,authIV).encrypt(str(response))
        return Response({"message":"data found","data":str(encResp),"response_code":"1"},status=status.HTTP_200_OK)

