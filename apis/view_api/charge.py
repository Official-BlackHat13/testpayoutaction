# from django.shortcuts import render
# Create your views here.


from django.db.models import query


from pyexcel_xls import get_data as xls_get
from pyexcel_xlsx import get_data as xlsx_get
from django.utils.datastructures import MultiValueDictKeyError
from rest_framework import permissions
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
        request_obj = "path:: "+request.path+" :: headers::" + \
            str(request.headers)+" :: meta_data:: " + \
            str(request.META)+"data::"+str(request.data)

        log = Log_model_services.Log_Model_Service(log_type="addCharge request at "+request.path+" slug",
                                                   client_ip_address=request.META['REMOTE_ADDR'], server_ip_address=const.server_ip, full_request=request_obj)
        logid = log.save()
        try:
            header = request.headers.get("auth_token")
            adminId = auth.AESCipher(const.AuthKey,const.AuthIV).decrypt(header)
            admin = BO_user_services.BO_User_Service.fetch_by_id(adminId)
            if(admin==None):
                Log_model_services.Log_Model_Service.update_response(
                logid, {"Message": "admin code missing", "response_code": "0"})
                return Response({"message":"admin id does not exist", "Response code":"0"},status=status.HTTP_404_NOT_FOUND)
            query = request.data.get("query")
            if(admin.is_encrypt==True):
                decrypted_query = auth.AESCipher(admin.auth_key,admin.auth_iv).decrypt(query)
                query = ast.literal_eval(str(decrypted_query))
            mode=query.get("mode")
            min_amount=query.get("min_amount")
            max_amount=query.get("max_amount")
            charge_percentage_or_fix=query.get("charge_percentage_or_fix")
            charge=query.get("charge")
            merchant_id=query.get("merchant_id")
            merchant = Client_model_service.Client_Model_Service.fetch_by_id(id=merchant_id,created_by="admin :: "+adminId,client_ip_address=request.META['REMOTE_ADDR'])
            if(merchant==None):
                Log_model_services.Log_Model_Service.update_response(
                logid, {"Message": "merchant code missing", "response_code": "0"})
                return Response({"message":"merchant id does not exist", "Response code":"0"},status=status.HTTP_404_NOT_FOUND)
            service = charge_model_service(merchant_id=merchant_id,mode=mode,min_amount=min_amount,max_amount=max_amount,charge_percentage_or_fix=charge_percentage_or_fix,charge=charge)
            resp = service.save(client_ip_address=request.META['REMOTE_ADDR'])
            Log_model_services.Log_Model_Service.update_response(
                logid, {"Message": "data saved","data":str(resp), "response_code": "1"})
            return Response({"message":"data saved", "response_code": "1"},status=status.HTTP_200_OK)
        except Exception as e:
            import traceback
            print(traceback.format_exc())
            Log_model_services.Log_Model_Service.update_response(logid,{"message":"Some error occured","Error_Code":e.args,"response_code":"2"})
            return Response({"Message":"some error","Error":e.args})



class fetchCharges(APIView):
    def post(self,request):
        request_obj = "path:: "+request.path+" :: headers::" + \
            str(request.headers)+" :: meta_data:: " + \
            str(request.META)+"data::"+str(request.data)
        log = Log_model_services.Log_Model_Service(log_type="fetchCharges request at "+request.path+" slug",
                                                   client_ip_address=request.META['REMOTE_ADDR'], server_ip_address=const.server_ip, full_request=request_obj)
        logid = log.save()
        try:
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
            print("....... ",clientModel.is_encrypt)
            if(clientModel.is_encrypt==False):
                return Response({"message":"data found","data":str(response),"response_code":"1"},status=status.HTTP_200_OK)
            authKey = clientModel.auth_key
            authIV = clientModel.auth_iv
            encResp = auth.AESCipher(authKey,authIV).encrypt(str(response))
            return Response({"message":"data found","data":str(encResp),"response_code":"1"},status=status.HTTP_200_OK)
        except Exception as e:
            import traceback
            print(traceback.format_exc())
            Log_model_services.Log_Model_Service.update_response(logid,{"message":"Some error occured","Error_Code":e.args,"response_code":"2"})
            return Response({"Message":"some error","Error":e.args})

