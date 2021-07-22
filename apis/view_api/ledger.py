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
from ..database_service.BO_user_services import BO_User_Service
# from 

from sabpaisa import auth

class GetLedgerForMerchant(APIView):
    def post(self,req,page,length):
        try:
            auth_token = req.headers["auth_token"]
            id=auth.AESCipher(const.AuthKey,const.AuthIV).decrypt(auth_token)
            if BO_User_Service.fetch_by_id(id)==None:
                return Response({"message":"user not valid","response_code":"0"})
            data=Ledger_Model_Service.getLedgers(page,length,req.META['REMOTE_ADDR'],"Admin Id :: "+str(id))
            
            return Response({"message":"date found","data":data,"response_code":"1"})
        except Exception as e:
         import traceback
         print(traceback.format_exc())
        #  Log_model_services.Log_Model_Service.update_response(logid,{"Message":e.args,"response_code":"2"})
         return Response({"Message":"Some Technical error","response_code":"2"},status=status.HTTP_204_NO_CONTENT)

class GetLedger(APIView):
    def post(self,req,page,length):
        try:
            auth_token = req.headers["auth_token"]
            id=auth.AESCipher(const.AuthKey,const.AuthIV).decrypt(auth_token)
            if BO_User_Service.fetch_by_id(id)==None:
                return Response({"message":"user not valid","response_code":"0"})
            data=Ledger_Model_Service.getLedgers(page,length,req.META['REMOTE_ADDR'],"Admin Id :: "+str(id))
            
            return Response({"message":"date found","data":data,"response_code":"1"})
        except Exception as e:
         import traceback
         print(traceback.format_exc())
        #  Log_model_services.Log_Model_Service.update_response(logid,{"Message":e.args,"response_code":"2"})
         return Response({"Message":"Some Technical error","response_code":"2"},status=status.HTTP_204_NO_CONTENT)

class LedgerSaveRequest(APIView):
    #permission_classes = (IsAuthenticated, )
    def post(self,request):
        # print(request.data.get("client"))
        merchant= request.data.get("merchant")
        query = request.data.get("query")
        ip = request.data.get("client_ip_address")
        createdBy = request.data.get("created_by")
        clientModel = Client_model_service.Client_Model_Service.fetch_by_id(
            id=merchant, created_by=createdBy, client_ip_address=ip)
        authKey = clientModel.auth_key
        authIV = clientModel.auth_iv
        encResp = auth.AESCipher(authKey, authIV).decrypt(query)
        res = ast.literal_eval(encResp)
        print("res......... ", res)
        print(type(res))
        service = Ledger_Model_Service(
            trans_amount_type=res.get("trans_amount_type"),
            merchant=res.get("merchant"),
            client_code=res.get("client_code"),
            type_status=res.get("type_status"),
            amount=res.get("amount"),
            van=res.get("van"),
            trans_type=res.get("trans_type"),
            trans_status=res.get("trans_status"),
            bank_ref_no= res.get("bank_ref_no"),
            customer_ref_no= res.get("customer_ref_no"),
            bank_id=res.get("bank"),
            trans_time=datetime.now(),
            bene_account_name=res.get("bene_account_name"),
            bene_account_number=res.get("bene_account_number"),
            bene_ifsc=res.get("bene_ifsc"),
            request_header=res.get("request_header"),
            mode =  res.get("mode"),
            charge = res.get("charge"),
            createdBy=res.get("createdBy"),
            updatedBy=res.get("updatedBy"),
            deletedBy=res.get("deletedBy"),
            created_at=datetime.now()
                                       )
        resp = service.save(client_ip_address=ip,
                            merchant=merchant, createdBy=createdBy)
        if(resp == "0"):
            return Response({"message": "nothing to show", "data": None, "response_code": "0"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"message": "data found", "data": resp, "response_code": "1"}, status=status.HTTP_200_OK)
        
class DeleteLedger(APIView):
    #permission_classes = (IsAuthenticated, )
    def delete(self,request):
        request_obj = "path:: "+request.path+" :: headers::" + \
            str(request.headers)+" :: meta_data:: " + \
            str(request.META)+"data::"+str(request.data)
        
        log = Log_model_services.Log_Model_Service(log_type="Delete request at "+request.path+" slug",
                                                   client_ip_address=request.META['REMOTE_ADDR'], server_ip_address=const.server_ip, full_request=request_obj)
        logid = log.save()
        id = request.data.get("id")
        deletedBy = request.data.get("deletedBy")
        m = request.headers["merchant"]
        aKey = const.AuthKey
        aIV = const.AuthIV
        merchant = auth.AESCipher(aKey, aIV).decrypt(m)
        print("id===== ",id)
        resp = Ledger_Model_Service.deleteById(
            id, deletedBy, merchant, request.META['REMOTE_ADDR'], deletedBy)

        if(resp == True):
            Log_model_services.Log_Model_Service.update_response(
                logid, {"Message": "delete successfully", "response_code": "1"})
            return JsonResponse({"Message": "delete successfully","response_code": "1"}, status=status.HTTP_200_OK)
        else:
            Log_model_services.Log_Model_Service.update_response(
                logid, {"Message": "Id not found", "response_code": "2"})
            return JsonResponse({"Message": "Id not found", "response_code": "2"}, status=status.HTTP_404_NOT_FOUND)

class UpdateLedger(APIView):
    #permission_classes = (IsAuthenticated, )
    def put(self,request):
        request_obj = "path:: "+request.path+" :: headers::" + \
            str(request.headers)+" :: meta_data:: " + \
            str(request.META)+"data::"+str(request.data)
        m = request.headers["merchant"]
        if(m == ""):
            return Response({"message": "merchant code missing", "data": None, "response_code": "3"}, status=status.HTTP_400_BAD_REQUEST)
        aKey = const.AuthKey
        aIV = const.AuthIV
        merchant = auth.AESCipher(aKey, aIV).decrypt(m)
        query = request.data.get("query")
        createdBy = request.data.get("created_by")
        log = Log_model_services.Log_Model_Service(log_type="update request at "+request.path+" slug",
                                                   client_ip_address=request.META['REMOTE_ADDR'], server_ip_address=const.server_ip, full_request=request_obj)
        logid = log.save()
        clientModel = Client_model_service.Client_Model_Service.fetch_by_id(
            id=merchant, created_by=createdBy, client_ip_address=request.META['REMOTE_ADDR'])
        authKey = clientModel.auth_key
        authIV = clientModel.auth_iv
        encResp = auth.AESCipher(authKey, authIV).decrypt(query)
        res = ast.literal_eval(encResp)
        id = res.get("id")
        ledger = LedgerModel.objects.filter(id=id,merchant=merchant,status=True)
        if(len(ledger) ==  0):
            Log_model_services.Log_Model_Service.update_response(
                logid, {"Message": res, "response_code": "0"})
            return JsonResponse({"Message": "id or merchantcode or status miss matched", "response_code": "0"}, status=status.HTTP_404_NOT_FOUND)
        if(len(ledger) > 0):
            ledgermodel = ledger[0]
            d = ledger[0].created_at
            service = Ledger_Model_Service(
                id=request.data.get("id"),
                trans_amount_type=res.get("trans_amount_type"),
                merchant=res.get("merchant"),
                client_code=res.get("client_code"),
                type_status=res.get("type_status"),
                amount=res.get("amount"),
                van=res.get("van"),
                trans_type=res.get("trans_type"),
                trans_status=res.get("trans_status"),
                bank_ref_no=res.get("bank_ref_no"),
                customer_ref_no=res.get("customer_ref_no"),
                bank_id=res.get("bank"),
                trans_time=datetime.now(),
                bene_account_name=res.get("bene_account_name"),
                bene_account_number=res.get("bene_account_number"),
                bene_ifsc=res.get("bene_ifsc"),
                request_header=res.get("request_header"),
                mode=res.get("mode"),
                charge=res.get("charge"),
                created_at=d,
                # deleted_at=ledgermodel.deleted_at,
                createdBy=res.get("createdBy"),
                updatedBy=res.get("updatedBy"),
                updated_at=datetime.now()
            )
            Log_model_services.Log_Model_Service.update_response(
                logid, {"Message": "updated successfully", "response_code": "1"})
            res = service.update(id=id, merchant=merchant,
                                 client_ip_address=request.META['REMOTE_ADDR'], created_by=createdBy)
            return JsonResponse({"Message": "updated successfully", "response_code": "1"}, status=status.HTTP_200_OK)
        Log_model_services.Log_Model_Service.update_response(
            logid, {"Message": "something went wrong!!!!", "response_code": "0"})
        return JsonResponse({"Message": "something went wrong!!!!", "response_code": "0"}, status=status.HTTP_400_BAD_REQUEST)
