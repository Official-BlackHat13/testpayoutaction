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
from ..serializersFolder.serializers import BeneSerializer, LogsSerializer
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

class adminFetchBeneficiary(APIView):
    @swagger_auto_schema(request_body=addBeneficiary_docs.fetch_request,responses=addBeneficiary_docs.fetch_response)
    def post(self,request,page,length):
        request_obj = "path:: "+request.path+" :: headers::" + \
            str(request.headers)+" :: meta_data:: " + \
            str(request.META)+"data::"+str(request.data)
        log = Log_model_services.Log_Model_Service(log_type="fetchBeneficiary request at "+request.path+" slug",
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
            if page=="all" and length != "all":
                return JsonResponse({"Message":"page and length format does not match"},status=status.HTTP_406_NOT_ACCEPTABLE)
            if(admin.is_encrypt==True):
                merchant_id = auth.AESCipher(admin.auth_key,admin.auth_iv).decrypt(request.data.get("query")).split(":")[1]
            else:
                merchant_id = str(request.data.get("query")).split(":")[1]
            bene_response = Beneficiary_Model_Services.fetchBeneficiaryByParams(client_ip_address=request.META['REMOTE_ADDR'],created_by="admin :: "+adminId,page=page,length=length,merchant_id=merchant_id)
            if(len(bene_response)==0):
                return Response({"message":"data not found","data":None},status=status.HTTP_404_NOT_FOUND)
            if(admin.is_encrypt==True):
                encResp = auth.AESCipher(admin.auth_key,admin.auth_iv).encrypt(str(bene_response))
                return Response({"message":"data found","data":encResp,"response_code":"1"},status=status.HTTP_200_OK) 
            else:
                return Response({"message":"data found","data":bene_response,"response_code":"1"},status=status.HTTP_200_OK)  
        except Exception as e:
            import traceback
            print(traceback.format_exc())
            Log_model_services.Log_Model_Service.update_response(logid, str({"Message":"some error","Error":e.args,"response_code":"2"}))
            return Response({"Message":"some error","Error":e.args,"response_code":"2"})


class merchantFetchBeneficiary(APIView):
    @swagger_auto_schema(request_body=addBeneficiary_docs.fetch_request,responses=addBeneficiary_docs.fetch_response)
    def post(self,request,page,length):
        request_obj = "path:: "+request.path+" :: headers::" + \
            str(request.headers)+" :: meta_data:: " + \
            str(request.META)+"data::"+str(request.data)
        log = Log_model_services.Log_Model_Service(log_type="fetchBeneficiary request at "+request.path+" slug",
                                                   client_ip_address=request.META['REMOTE_ADDR'], server_ip_address=const.server_ip, full_request=request_obj)
        logid = log.save()
        try:
            auth_token = request.headers.get("auth_token")
            merchantId = auth.AESCipher(const.AuthKey,const.AuthIV).decrypt(auth_token)
            clientModel = Client_model_service.Client_Model_Service.fetch_by_id(
                id=merchantId, created_by="merchantid :: "+merchantId, client_ip_address=request.META['REMOTE_ADDR'])
            if(clientModel==None):
                Log_model_services.Log_Model_Service.update_response(
                logid, {"Message": "merchant code missing", "response_code": "0"})
                return Response({"message":"merchant id does not exist", "Response code":"0"},status=status.HTTP_404_NOT_FOUND)
            if page=="all" and length != "all":
                return JsonResponse({"Message":"page and length format does not match"},status=status.HTTP_406_NOT_ACCEPTABLE)
            
            bene_response = Beneficiary_Model_Services.fetchBeneficiaryByParams(client_ip_address=request.META['REMOTE_ADDR'],created_by="merchant :: "+merchantId,page=page,length=length,merchant_id=merchantId)
            if(len(bene_response)==0):
                return Response({"message":"data not found","data":None},status=status.HTTP_404_NOT_FOUND) 
            if(clientModel.is_encrypt==True):
                encResp = auth.AESCipher(clientModel.auth_key,clientModel.auth_iv).encrypt(str(bene_response))
                return Response({"message":"data found","data":encResp},status=status.HTTP_200_OK) 
            else:
                return Response({"message":"data found","data":bene_response},status=status.HTTP_200_OK)  
        except Exception as e:
            import traceback
            print(traceback.format_exc())
            Log_model_services.Log_Model_Service.update_response(logid, str({"Message":"some error","Error":e.args}))
            return Response({"Message":"some error","Error":e.args})

               

class updateBeneficiary(APIView):
    def put(self,request):
        auth_token = request.headers.get("auth_token")
        merchantId = auth.AESCipher(const.AuthKey,const.AuthIV).decrypt(auth_token)
        clientModel = Client_model_service.Client_Model_Service.fetch_by_id(
                id=merchantId, created_by="merchantid :: "+merchantId, client_ip_address=request.META['REMOTE_ADDR'])
        authKey = clientModel.auth_key
        authIV = clientModel.auth_iv
        decResp = str(request.data.get("query"))
        if  clientModel.is_encrypt  :
                decResp = auth.AESCipher(authKey, authIV).decrypt(decResp)
        res = ast.literal_eval(decResp)
        id = res.get("id")
        bene = BeneficiaryModel.objects.filter(id=id)
        if(len(bene)==0):
            return Response({"msg":"not found","response_code":'0'},status=status.HTTP_404_NOT_FOUND)
        full_name = res.get("full_name")
        account_number = res.get("account_number")
        ifsc_code = res.get("ifsc_code")
        upi_id=res.get("upi_id")
        merchant_id = res.get("merchant_id")
        updated_by = res.get("updated_by")
        created_at = bene[0].created_at
        updated_at = datetime.now()
        service = Beneficiary_Model_Services(upiId=upi_id,full_name=full_name,account_number=account_number,ifsc_code=ifsc_code,merchant_id=merchant_id)
        service.update(id=id,updated_at=updated_at,updated_by=updated_by,created_at=created_at)
        return Response({"msg":"done","response_code":'1'},status=status.HTTP_200_OK)

class deleteBeneficiary(APIView):
    def delete(self,request):
        auth_token = request.headers.get("auth_token")
        merchantId = auth.AESCipher(const.AuthKey,const.AuthIV).decrypt(auth_token)
        clientModel = Client_model_service.Client_Model_Service.fetch_by_id(
                id=merchantId, created_by="merchantid :: "+merchantId, client_ip_address=request.META['REMOTE_ADDR'])
        authKey = clientModel.auth_key
        authIV = clientModel.auth_iv
        decResp = str(request.data.get("query"))
        if  clientModel.is_encrypt  :
                decResp = auth.AESCipher(authKey, authIV).decrypt(decResp)
        res = ast.literal_eval(decResp)
        id = res.get("id")
        bene = BeneficiaryModel.objects.filter(id=id)
        if(len(bene)==0):
            return Response({"msg":"not found","response_code":'0'},status=status.HTTP_404_NOT_FOUND)
        
        Beneficiary_Model_Services.soft_delete_by_id(id)
        return Response({"msg":"done","response_code":'1'},status=status.HTTP_200_OK)

class addSingleBeneficiary(APIView):
    @swagger_auto_schema(request_body=addBeneficiary_docs.single_bene,responses=addBeneficiary_docs.single_bene_response)
    def post(self, request):
        request_obj = "path:: "+request.path+" :: headers::" + \
            str(request.headers)+" :: meta_data:: " + \
            str(request.META)+"data::"+str(request.data)
        log = Log_model_services.Log_Model_Service(log_type="addSingleBeneficiary request at "+request.path+" slug",
                                                   client_ip_address=request.META['REMOTE_ADDR'], server_ip_address=const.server_ip, full_request=request_obj)
        logid = log.save()
        try:
            auth_token = request.headers.get("auth_token")
            merchantId = auth.AESCipher(const.AuthKey,const.AuthIV).decrypt(auth_token)
            clientModel = Client_model_service.Client_Model_Service.fetch_by_id(
                id=merchantId, created_by="merchantid :: "+merchantId, client_ip_address=request.META['REMOTE_ADDR'])
            authKey = clientModel.auth_key
            authIV = clientModel.auth_iv
            decResp = str(request.data.get("query"))
            if  clientModel.is_encrypt  :
                decResp = auth.AESCipher(authKey, authIV).decrypt(decResp)
            res = ast.literal_eval(decResp)
            print(res.get("full_name"))
            resultSet = BeneficiaryModel.objects.filter(merchant_id=int(merchantId),account_number=res.get("account_number"),ifsc_code=res.get("ifsc_code"),upi_id=res.get("upi_id"))
            if(len(resultSet)>0):
                return Response({"Message":"data already exist","response_code":'0'},status=status.HTTP_406_NOT_ACCEPTABLE)
            
            service = Beneficiary_Model_Services(upiId=res.get("upi_id"),full_name=res.get("full_name"),account_number=res.get("account_number"),ifsc_code=res.get("ifsc_code"),merchant_id=merchantId)
            resp = service.save()
            return Response({"msg":"data saved to database","response_code":'1'},status=status.HTTP_200_OK)
        except Exception as e:
            import traceback
            print(traceback.format_exc())
            Log_model_services.Log_Model_Service.update_response(logid,{"message":"Some error occured","Error_Code":e.args,"response_code":"2"})
            return Response({"Message":"some error","Error":e.args})
 
class saveBeneficiary(APIView):
    @swagger_auto_schema(request_body=addBeneficiary_docs.request,responses=addBeneficiary_docs.response_schema_dict)
    def post(self, request, format=None):
        request_obj = "path:: "+request.path+" :: headers::" + \
            str(request.headers)+" :: meta_data:: " + \
            str(request.META)+"data::"+str(request.data)
        log = Log_model_services.Log_Model_Service(log_type="saveBeneficiary request at "+request.path+" slug",
                                                   client_ip_address=request.META['REMOTE_ADDR'], server_ip_address=const.server_ip, full_request=request_obj)
        logid = log.save()
        api_key = str(request.headers['auth_token'])
        merchantId =auth.AESCipher(const.AuthKey,const.AuthIV).decrypt(api_key)
        clientModel = Client_model_service.Client_Model_Service.fetch_by_id(
                id=merchantId, created_by="merchantid :: "+merchantId, client_ip_address=request.META['REMOTE_ADDR'])
        if(clientModel == None):
            return Response({"message":"merchant id not found","Response_code":"0"},status=status.HTTP_400_BAD_REQUEST)
        authKey = clientModel.auth_key
        authIV = clientModel.auth_iv
        try:
            excel_file = request.FILES["files"]
        except MultiValueDictKeyError:
            return Response({"msg":"check format of the file uploaded","response_code":'0'},status=status.HTTP_400_BAD_REQUEST)
        try:
            if (str(excel_file).split(".")[-1] == "xls"):
                data = xls_get(excel_file, column_limit=10)
            elif (str(excel_file).split(".")[-1] == "xlsx"):
                data = xlsx_get(excel_file, column_limit=10)
            datas = data["Sheet1"]
            full_name = str()
            account_number=str()
            ifsc_code=str()
            merchant_id=str()
            for d in datas:
                if(d[0]!="full_name"):
                    full_name = d[0]
                    account_number = d[1]
                    ifsc_code = d[2]
                    merchant_id = d[3]
                    upi_id=d[4]
                    resultSet = BeneficiaryModel.objects.filter(merchant_id=int(merchantId),account_number=account_number,ifsc_code=ifsc_code,upi_id=upi_id)
                    if(len(resultSet)==0 and merchant_id==int(merchantId)):
                        print("true")
                        service = Beneficiary_Model_Services(full_name=full_name,account_number=account_number,ifsc_code=ifsc_code,merchant_id=merchant_id,upiId=upi_id)
                        service.save()
            return Response({"msg":"data parsed and saved to database","response_code":'1'},status=status.HTTP_200_OK)
        except Exception as e:
            import traceback
            print(traceback.format_exc())
            Log_model_services.Log_Model_Service.update_response(logid,{"message":"Some error occured","Error_Code":e.args,"response_code":"2"})
            return Response({"Message":"some error","Error":e.args})

#new beneficiary
class addingSingleBeneficiary(APIView):
    @swagger_auto_schema(request_body=addBeneficiary_docs.single_bene,responses=addBeneficiary_docs.single_bene_response)
    def post(self, request):
        request_obj = "path:: "+request.path+" :: headers::" + \
            str(request.headers)+" :: meta_data:: " + \
            str(request.META)+"data::"+str(request.data)
        log = Log_model_services.Log_Model_Service(log_type="addSingleBeneficiary request at "+request.path+" slug",
                                                   client_ip_address=request.META['REMOTE_ADDR'], server_ip_address=const.server_ip, full_request=request_obj)
        logid = log.save()
        try:
            auth_token = request.headers.get("auth_token")
            merchantId = auth.AESCipher(const.AuthKey,const.AuthIV).decrypt(auth_token)
            clientModel = Client_model_service.Client_Model_Service.fetch_by_id(
                id=merchantId, created_by="merchantid :: "+merchantId, client_ip_address=request.META['REMOTE_ADDR'])
            authKey = clientModel.auth_key
            authIV = clientModel.auth_iv
            decResp = str(request.data.get("query"))
            if  clientModel.is_encrypt  :
                decResp = auth.AESCipher(authKey, authIV).decrypt(decResp)
            res = ast.literal_eval(decResp)
            resultSet = BeneficiaryModel.objects.filter(merchant_id=int(merchantId),account_number=res.get("account_number"),ifsc_code=res.get("ifsc_code"),upi_id=res.get("upi_id"))
            if(len(resultSet)>0):
                return Response({"Message":"data already exist","response_code":'0'},status=status.HTTP_406_NOT_ACCEPTABLE)
            
            service = Beneficiary_Model_Services(upiId=res.get("upiId"),full_name=res.get("fullName"),account_number=res.get("accountNumber"),ifsc_code=res.get("ifsCode"),merchant_id=merchantId)
            resp = service.save()
            return Response({"msg":"data saved to database","response_code":'1'},status=status.HTTP_200_OK)
        except Exception as e:
            import traceback
            print(traceback.format_exc())
            Log_model_services.Log_Model_Service.update_response(logid,{"message":"Some error occured","Error_Code":e.args,"response_code":"2"})
            return Response({"Message":"some error","Error":e.args})



class FetchBeniAdminAPIView(APIView):
    def get(self,req,merchantId):
        try:
            merchant_id=merchantId
            rec=Beneficiary_Model_Services.fetchBeneficiaryByMerchantId(merchant_id)
            serl = BeneSerializer(rec,many=True)
            if rec==None:
                return Response({"data":[],"message":"NO DATA FOUND","response_code":0},status=status.HTTP_200_OK)
            return Response({"data":serl.data,"message":"DATA FOUND","response_code":1},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message":"some technical error","error":e.args,"response_code":2},status=status.HTTP_400_BAD_REQUEST)


class addSingleBeneficiaryfor(APIView):
    @swagger_auto_schema(request_body=addBeneficiary_docs.single_bene,responses=addBeneficiary_docs.single_bene_response)
    def post(self, request):
        request_obj = "path:: "+request.path+" :: headers::" + \
            str(request.headers)+" :: meta_data:: " + \
            str(request.META)+"data::"+str(request.data)
        log = Log_model_services.Log_Model_Service(log_type="addSingleBeneficiary request at "+request.path+" slug",
                                                   client_ip_address=request.META['REMOTE_ADDR'], server_ip_address=const.server_ip, full_request=request_obj)
        logid = log.save()
        try:
            merchantId = request.data.get("merchant_id")
            
            decResp = str(request.data.get("query"))
            
            res = ast.literal_eval(decResp)
            print(res.get("full_name"))
            resultSet = BeneficiaryModel.objects.filter(merchant_id=int(merchantId),account_number=res.get("account_number"),ifsc_code=res.get("ifsc_code"),upi_id=res.get("upi_id"))
            if(len(resultSet)>0):
                return Response({"Message":"data already exist","response_code":'0'},status=status.HTTP_406_NOT_ACCEPTABLE)
            
            service = Beneficiary_Model_Services(upiId=res.get("upi_id"),full_name=res.get("full_name"),account_number=res.get("account_number"),ifsc_code=res.get("ifsc_code"),merchant_id=merchantId)
            resp = service.save()
            return Response({"msg":"data saved to database","response_code":'1'},status=status.HTTP_200_OK)
        except Exception as e:
            import traceback
            print(traceback.format_exc())
            Log_model_services.Log_Model_Service.update_response(logid,{"message":"Some error occured","Error_Code":e.args,"response_code":"2"})
            return Response({"Message":"some error","Error":e.args})
 