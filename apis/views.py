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
from .API_docs import payout_docs,auth_docs,login_docs,payoutTransactionEnquiry_docs,addBalance_docs,addBeneficiary_docs,log_docs
from datetime import datetime
from .serializersFolder.serializers import LogsSerializer
#from .serializers import *
# from .models import *
import ast
from .other_service import payout_service
from .database_models import LedgerModel,ModeModel
from apis.database_service.Ledger_model_services import *
from django.http.response import JsonResponse
from apis.other_service.enquiry_service import *
from apis.database_service.Beneficiary_model_services import *
from .database_service import Client_model_service,Bank_model_services
from rest_framework.parsers import JSONParser
from .database_service import Client_model_service,Bank_model_services,IpWhitelisting_model_service
from django.contrib.auth.models import User
# from .database_service import Client_model_service,Ledger_model_services
from rest_framework.permissions import IsAuthenticated
from . import const
from .Utils import randomstring
from .database_service import BO_user_services

from .models import MerchantModel,RoleModel







# from .models import MerchantModel,RoleModel
from sabpaisa import auth

from datetime import datetime

from .bank_services import ICICI_service

from .other_service import login_service,signup_service

from . import const
from sabpaisa import auth

# from .models import TestModel

# class getTest(APIView):
#     # @swagger_auto_schema(responses=api_docs.response_schema_dict,request_body=api_docs.val)
#     def get(self,req):
#         print(req.data)
#         t = TestModel()
#         t.save()
        
#         return JsonResponse({"obj":"save"})
# class updateTest(APIView):
#     def get(self,req,id):

#         print(req.data)

#         t = TestModel.objects.get(id=id)
#         t.updated_at=datetime.now()
#         t.save()
#         return JsonResponse({"obj":"save"})
# class GetRoles(APIView):
#     def get(self,req):
#         pass
class AuthAdmin(APIView):
    @swagger_auto_schema(request_body=auth_docs.request_admin,responses=auth_docs.admin_response_dict)
    def post(self,req):
        request_obj = "path:: "+req.path+" :: headers::"+str(req.headers)+" :: meta_data:: "+str(req.META)+"data::"+str(req.data)
        user = req.data
        print("req data::"+str(req.data))
        log = Log_model_services.Log_Model_Service(log_type="Post request at "+req.path+" slug",client_ip_address=req.META['REMOTE_ADDR'],server_ip_address=const.server_ip,full_request=request_obj)
        logid=log.save()
        print("log::"+str(logid))
        try:
            val=signup_service.Signup_Service(user=user,client_ip_address=req.META['REMOTE_ADDR']).AdminSignup()
            Log_model_services.Log_Model_Service.update_response(logid,{"Message":"user created","user_id":val['merchant_id'],"response_code":"1","CLIENT_AUTH_KEY":val['client'].auth_key,"CLIENT_AUTH_IV":val['client'].auth_iv,"token":val['token'].json()})
            return Response({"Message":"user created","response_code":"1","user_id":val['merchant_id'],"CLIENT_AUTH_KEY":val['client'].auth_key,"CLIENT_AUTH_IV":val['client'].auth_iv,"token":val['token'].json()},status=status.HTTP_200_OK)
        except Exception as e:
            import traceback
            print(traceback.format_exc())
            Log_model_services.Log_Model_Service.update_response(logid,{"Message":"some error","error":e.args,"trace_back":e.with_traceback(e.__traceback__)})
            
            return Response({"Message":"some error","error":e.args},status=status.HTTP_400_BAD_REQUEST)
class Auth(APIView):
    @swagger_auto_schema(request_body=auth_docs.request,responses=auth_docs.response_schema_dict)
    def post(self,req):
        request_obj = "path:: "+req.path+" :: headers::"+str(req.headers)+" :: meta_data:: "+str(req.META)+"data::"+str(req.data)
        user = req.data
        print("req data::"+str(req.data))
        log = Log_model_services.Log_Model_Service(log_type="Post request at "+req.path+" slug",client_ip_address=req.META['REMOTE_ADDR'],server_ip_address=const.server_ip,full_request=request_obj)
        logid=log.save()
        print("log::"+str(logid))
        try:
            val=signup_service.Signup_Service(user=user,client_ip_address=req.META['REMOTE_ADDR']).SignUp()
            Log_model_services.Log_Model_Service.update_response(logid,{"Message":"user created","merchant_id":val['merchant_id'],"response_code":"1","CLIENT_AUTH_KEY":val['client'].auth_key,"CLIENT_AUTH_IV":val['client'].auth_iv,"token":val['token'].json()})
            return Response({"Message":"user created","response_code":"1","merchant_id":val['merchant_id'],"CLIENT_AUTH_KEY":val['client'].auth_key,"CLIENT_AUTH_IV":val['client'].auth_iv,"token":val['token'].json()},status=status.HTTP_200_OK)
        except Exception as e:
            import traceback
            print(traceback.format_exc())
            Log_model_services.Log_Model_Service.update_response(logid,{"Message":"some error","error":e.args,"trace_back":e.with_traceback(e.__traceback__)})
            
            return Response({"Message":"some error","error":e.args},status=status.HTTP_400_BAD_REQUEST)
# class icicBankRequest(APIView):
#     def post(self,req):

class bankApiPaymentView(APIView):
    # permission_classes = (IsAuthenticated, )
    @swagger_auto_schema(request_body=payout_docs.request,responses=payout_docs.response_schema_dict)
    def post(self,req):
        request_obj = "path::"+req.path+"headers::"+str(req.headers)+"meta_data::"+str(req.META)+"data::"+str(req.data)
        # payment_service=IFDC_service.payment.Payment()
        api_key = req.headers['auth_token']
        merchant_id=auth.AESCipher(const.AuthKey,const.AuthIV).decrypt(api_key)
        encrypted_code=req.data["encrypted_code"]
        
        log = Log_model_services.Log_Model_Service(log_type="Post request at "+req.path+" slug",client_ip_address=req.META['REMOTE_ADDR'],server_ip_address=const.server_ip,full_request=request_obj)
        logid=log.save()
        client = Client_model_service.Client_Model_Service.fetch_by_id(merchant_id,req.META['REMOTE_ADDR'],"merchant id :: "+merchant_id)
        print("client bank::"+str(client.bank))
        bank = Bank_model_services.Bank_model_services.fetch_by_id(client.bank,req.META['REMOTE_ADDR'],"merchant id :: "+merchant_id)
        # print("bank::"+str(bank))
        payout=payout_service.PayoutService(merchant_id=merchant_id,encrypted_code=encrypted_code,client_ip_address=req.META['REMOTE_ADDR'])
        if(bank.bank_name=="ICICI"):
         res = payout.excuteICICI()
        elif bank.bank_name=="PAYTM":
            res = payout.excutePAYTM()
        else:
            res = payout.excuteIDFC()
        if(res[0]=="Payout Done"):
            merchant=MerchantModel.objects.get(id=merchant_id)
            role = RoleModel.objects.get(id=merchant.role)
            enc_str=res[1]
            if const.test_merchants and role.role_name!="test":
             enc_str=str(auth.AESCipher(client.auth_key,client.auth_iv).encrypt(str(res[1])))[2:].replace("'","")
            elif not const.test_merchants:
                enc_data = str(auth.AESCipher(client.auth_key, client.auth_iv).encrypt(str(res[1])))[2:].replace("'","")
            Log_model_services.Log_Model_Service.update_response(logid,{"Message":res,"response_code":"1"})
            return Response({"Message":"Payout Done",'resData':enc_str,"response_code":"1"},status=status.HTTP_200_OK)
        elif res[2]:
            Log_model_services.Log_Model_Service.update_response(logid,{"Message":res,"response_code":"0"})
            return Response({"Message":res[1],"response_code":"0"},status=status.HTTP_402_PAYMENT_REQUIRED)
        elif res[0]==False:
            Log_model_services.Log_Model_Service.update_response(logid,{"Message":"credential not matched","response_code":"3"})
            return Response({"Message":"credential not matched","response_code":"3"},status=status.HTTP_401_UNAUTHORIZED)
        else:
            Log_model_services.Log_Model_Service.update_response(logid,{"Message":res,"response_code":"2"})
            return Response({"Message":res[0],"response_code":"2"},status=status.HTTP_204_NO_CONTENT)
            
        # return Response(payment_service.hit())

class bankApiEnquiryView(APIView):
    @swagger_auto_schema()
    def post(self,req):
        pass


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

class encryptJSON(APIView):
    def post(self, request):
        query = str(request.data.get("query"))
        authKey = request.data.get("authkey")
        authIV = request.data.get("authiv")
        normal=request.data.get("yo")
        print("..... ",normal)
        encResp = auth.AESCipher(authKey,authIV).encrypt(query)
        return Response({"message": "data", "data": str(encResp), "response_code": "3"}, status=status.HTTP_200_OK)

class decryptJson(APIView):
    def post(self,request):
        query = request.data.get("query")
        authKey = request.data.get("authkey")
        authIV = request.data.get("authiv")
        encResp = auth.AESCipher(authKey,authIV).decrypt(query)
        return Response({"message": "data", "data": str(encResp), "response_code": "3"}, status=status.HTTP_200_OK)

class GetLogs(APIView):
    @swagger_auto_schema(responses=log_docs.response_dict)
    def get(self,req,page,length):
        authKey = const.AuthKey
        authIV = const.AuthIV
        resp = req.headers["auth_token"]
        
        merchant = auth.AESCipher(authKey,authIV).decrypt(resp)
        clientModel=BO_user_services.BO_User_Service.fetch_by_id(id=merchant)
        print(clientModel,"clientModel")
        if clientModel == None:
            return  Response({"message":"client not found"},status=status.HTTP_401_UNAUTHORIZED)
        # clientModel = Client_model_service.Client_Model_Service.fetch_by_id(
        #     id=merchant, created_by=str(merchant), client_ip_address=req.META['REMOTE_ADDR'])
        authKey = clientModel.auth_key
        authIV = clientModel.auth_iv
        request_obj = "path:: "+req.path+" :: headers::"+str(req.headers)+" :: meta_data:: "+str(req.META)+"data::"+str(req.data)
        logs = Log_model_services.Log_Model_Service(log_type="get request on "+req.path,client_ip_address=req.META['REMOTE_ADDR'],server_ip_address=const.server_ip,full_request=request_obj,remarks="get request on "+req.path+" for fetching the log records")
        logid=logs.save()
        # merchant=MerchantModel.objects.get(id=merchant)
        role = RoleModel.objects.get(id=clientModel.role)
        try:
            if page=="all" and length != "all":
                return JsonResponse({"Message":"page and length format does not match"},status=status.HTTP_406_NOT_ACCEPTABLE)
            logs = Log_model_services.Log_Model_Service.fetch_all_logs_in_parts(length)
            #auth.AESCipher(authKey, authIV).encrypt(logsser.data)
            print(logs)
            if page == "all":
                logsser=LogsSerializer(logs,many=True)
                enc_data=logsser.data
                print(role.role_name)
                if const.test_merchants and role.role_name!="test" :
                  enc_data = auth.AESCipher(authKey, authIV).encrypt(str(logsser.data))
                elif not const.test_merchants:
                  enc_data = auth.AESCipher(authKey, authIV).encrypt(str(logsser.data))
                print(enc_data)
                print(authKey,authIV,"AUTH KEY , AUTH IV")
                return Response({"data_length": len(logs), "data": auth.AESCipher(authKey, authIV).encrypt(str(logsser.data))})
            page=int(page)
            if page>logs[1]:
             page=logs[1]-1
            logsser=LogsSerializer(logs[0][page],many=True)
            print(logs[0][page])
            Log_model_services.Log_Model_Service.update_response(logid, str({"data_length": len(
                logs[0][page]), "data": logsser.data}))
            
            # print(merchant.id)
            enc_data=logsser.data
            print(enc_data)
            print(role.role_name)
            if const.test_merchants and role.role_name!="test" :
             print("if")
             enc_data = auth.AESCipher(authKey, authIV).encrypt(str(logsser.data))
            elif not const.test_merchants:
                print("else")
                enc_data = auth.AESCipher(authKey, authIV).encrypt(str(logsser.data))
            print(enc_data)
            print(authKey,authIV,"AUTH KEY , AUTH IV")
            return Response({"data_length": len(logs[0][page]), "data": enc_data})
        except Exception as e:
            import traceback
            print(traceback.format_exc())
            Log_model_services.Log_Model_Service.update_response(logid, str({"data_length": len(
                logs[0][page]), "data": logsser.data}))
            return Response({"Message":"some error","Error":e.args})
        
class fetch(APIView):
    #permission_classes = (IsAuthenticated, )
    def post(self,request,page,length):
        request_obj = "path:: "+request.path+" :: headers::" + \
            str(request.headers)+" :: meta_data:: " + \
            str(request.META)+"data::"+str(request.data)
        log = Log_model_services.Log_Model_Service(log_type="Post request at "+request.path+" slug", table_name="apis_ledgermodel",
                                                   client_ip_address=request.META['REMOTE_ADDR'], server_ip_address=const.server_ip, full_request=request_obj)
        logid = log.save()
        authKey = const.AuthKey
        authIV = const.AuthIV
        resp = request.headers["auth_token"]
        if(resp == ""):
            Log_model_services.Log_Model_Service.update_response(
                logid, {"Message": "merchant code missing", "response_code": "3"})
            return Response({"message": "merchant code missing", "data": None, "response_code": "3"}, status=status.HTTP_400_BAD_REQUEST)
        if page == "all" and length != "all":
            Log_model_services.Log_Model_Service.update_response(
                logid, {"Message": "page and length format does not match", "response_code": "3"})
            return JsonResponse({"Message": "page and length format does not match", "data": None, "response_code": "3"}, status=status.HTTP_406_NOT_ACCEPTABLE)
        if(int(page)!= 1 and length == "all"):
            Log_model_services.Log_Model_Service.update_response(
                logid, {"Message": "page and length format not compatible", "response_code": "3"})
            return JsonResponse({"Message": "page and length format not compatible", "data": None, "response_code": "3"}, status=status.HTTP_406_NOT_ACCEPTABLE)
        if(resp == ""):
            Log_model_services.Log_Model_Service.update_response(
                logid, {"Message": "merchant code missing", "response_code": "3"})
            return Response({"message": "merchant code missing", "data": None, "response_code": "3"}, status=status.HTTP_400_BAD_REQUEST)
        decMerchant = auth.AESCipher(authKey, authIV).decrypt(resp)
        clientModel = Client_model_service.Client_Model_Service.fetch_by_id(
                id=decMerchant, created_by="merchant id :: "+decMerchant, client_ip_address=request.META['REMOTE_ADDR'])
        authKey = clientModel.auth_key
        authIV = clientModel.auth_iv
        query = auth.AESCipher(authKey,authIV).decrypt(request.data.get("query")).split("'")
        key = query[1]
        value = query[3]
        clientCode = None
        customer_ref_no = None
        trans_type=None
        startTime=None
        endTime = None
        if(len(query)>5):
            customer_ref_no=query[3]
            trans_type=query[7]
            clientCode=query[11]
        elif(key=="startTime"):
            startTime = value
            if(query[5]=="endTime"):
                endTime=query[7]
        elif(key=="clientCode"):
            clientCode = value
        elif(key=="orderId"):
            customer_ref_no = value
        elif(key=="trans_type"):
            trans_type = value
        resp = enquiry_service.fetchLedgerByParams(client_code = clientCode,
        startTime=startTime,endTime=endTime,page=page,length=length,
        merchant = decMerchant,customer_ref_no=customer_ref_no,trans_type=trans_type,created_by="merchant id :: "+decMerchant,client_ip_address=request.META['REMOTE_ADDR'])
        if(resp=="-2"):
            Log_model_services.Log_Model_Service.update_response(
                logid, {"Message": "length of page is greater then the result length", "response_code": "2"})
            return Response({"message": "length of page is greater then the result length", "data": None, "response_code": "2"}, status=status.HTTP_404_NOT_FOUND)

        if(resp=="0"):
            Log_model_services.Log_Model_Service.update_response(
                logid, {"Message": "no data for the given credentials", "response_code": "2"})
            return Response({"message": "no data for the given credentials", "data": None, "response_code": "2"}, status=status.HTTP_404_NOT_FOUND)
        if(resp=="-1"):
            Log_model_services.Log_Model_Service.update_response(
                logid, {"Message": "missing mandatory parameters", "response_code": "3"})
            return Response({"message": "missing mandatory parameters", "data": None, "response_code": "3"}, status=status.HTTP_400_BAD_REQUEST)
        result = list()
        if(len(resp)>0):
            for r in resp:
                res = { 
                        "id":r.get("id"),
                        'payoutTransactionId':r.get("payout_trans_id"),
                        'amount': r.get("amount"),
                        'transType': r.get("trans_type"),
                        'statusType': r.get("type_status"),
                        'bankRefNo': r.get("bank_ref_no"),
                        'orderId': r.get("customer_ref_no"),
                        'beneficiaryAccountName': r.get("bene_account_name"),
                        'beneficiaryAccountNumber': r.get("bene_account_number"),
                        'beneficiaryIFSC': r.get("bene_ifsc"),
                        'transStatus': r.get("trans_status"),
                        'mode': r.get("mode")
                    }
                result.append(res)
        
        encResult = auth.AESCipher(authKey,authIV).encrypt(str(result))
        Log_model_services.Log_Model_Service.update_response(
            logid, {"Message": str(resp), "response_code": "1"})
        return Response({"message": "data found", "data": encResult, "response_code": "1"}, status=status.HTTP_200_OK)

class paymentEnc(APIView):
    @swagger_auto_schema(request_body=payoutTransactionEnquiry_docs.request,responses=payoutTransactionEnquiry_docs.response_schema_dict)

    def post(self,req):       

        try:
            data = req.data["query"]
            auth_token = req.headers["auth_token"]
            print("auth token :: "+auth_token)
            merchant_id = auth.AESCipher(const.AuthKey,const.AuthIV).decrypt(auth_token)
            print("merchant id :: "+merchant_id)
            clientModel = Client_model_service.Client_Model_Service.fetch_by_id(id=merchant_id, created_by="Merchant :: "+str(merchant_id), client_ip_address=req.META['REMOTE_ADDR'])
            authKey = clientModel.auth_key
            authIV = clientModel.auth_iv
            encResp=data
            merchant=MerchantModel.objects.get(id=merchant_id)
            role = RoleModel.objects.get(id=merchant.role)
            if const.merchant_check and role.role_name!="test" :
             encResp = auth.AESCipher(authKey, authIV).decrypt(data)
            customer_ref = encResp.split(":")[1].replace('"','')
            rec =enquiry_service.get_enc(customer_ref,req.META['REMOTE_ADDR'],created_by="Merchant id :: "+str(merchant_id))
            if rec!=None:
                res = {
                        'payoutTransactionId':rec.payout_trans_id,
                        'amount': rec.amount,
                        'transType': rec.trans_type,
                        'statusType': rec.type_status,
                        'bankRefNo': rec.bank_ref_no,
                        'orderId': rec.customer_ref_no,
                        'beneficiaryAccountName': rec.bene_account_name,
                        'beneficiaryAccountNumber': rec.bene_account_number,
                        'beneficiaryIFSC': rec.bene_ifsc,
                        'transStatus': rec.trans_status,
                        'mode': rec.mode
                    }
                enc = res
                print("roleName :: "+role.role_name)
                if const.test_merchants and role.role_name!="test":
                 enc = str(auth.AESCipher(authKey,authIV).encrypt(str(res)))[2:].replace("'","")
                elif not const.test_merchants:
                    enc = str(auth.AESCipher(authKey,authIV).encrypt(str(res)))[2:].replace("'","")
                return Response({"message": "data found","resData": enc,"responseCode": "1"})
            else:
                return Response({"message":"NOT_FOUND","response_code":"0"})
        except Exception as e:
            import traceback
            print(traceback.format_exc())
            return Response({"message":e.args})

class tester(APIView):
    def get(self,request):
        authKey = const.AuthKey
        authIV = const.AuthIV
        resp = request.headers["merchant"]
        decMerchant = auth.AESCipher(authKey, authIV).decrypt(resp)
        return Response({"header": decMerchant, "authkey": authKey, "authIV": authIV})

class addBalanceApi(APIView):
    @swagger_auto_schema(request_body=addBalance_docs.request,responses=addBalance_docs.response_schema_dict)
    def post(self,request):
        request_obj = "path:: "+request.path+" :: headers::" + \
            str(request.headers)+" :: meta_data:: " + \
            str(request.META)+"data::"+str(request.data)
        log = Log_model_services.Log_Model_Service(log_type="Post request at "+request.path+" slug",
                                                    client_ip_address=request.META['REMOTE_ADDR'], server_ip_address=const.server_ip, full_request=request_obj)
        logid=log.save()
        authKey = const.AuthKey
        authIV = const.AuthIV
        merchant = request.headers["auth_token"]
        if(merchant == ""):
            Log_model_services.Log_Model_Service.update_response(
                logid, {"Message": "merchant code missing", "response_code": "3"})
            return Response({"message": "merchant code missing", "data": None, "response_code": "3"}, status=status.HTTP_400_BAD_REQUEST)
        decMerchant = auth.AESCipher(authKey, authIV).decrypt(merchant)
        created_by = "merchant ::"+decMerchant
        query = request.data.get("query")
        clientModel = Client_model_service.Client_Model_Service.fetch_by_id(
            id=decMerchant, created_by=created_by, client_ip_address=request.META['REMOTE_ADDR'])
        authKey = clientModel.auth_key
        authIV = clientModel.auth_iv
        #start
        role = RoleModel.objects.get(id=clientModel.role)
        if role.role_name=="test" :
            print("hello")
            decResp = request.data.get("query")
            res = ast.literal_eval(str(decResp))
            response = Ledger_Model_Service.addBal(res,client_ip_address=request.META['REMOTE_ADDR'],merchant = decMerchant,clientCode = clientModel.client_code)
            return Response({"data":str(response),"responseCode":"1"})
        #end
        decResp = auth.AESCipher(authKey, authIV).decrypt(query)
        res = ast.literal_eval(decResp)
        response = Ledger_Model_Service.addBal(res,client_ip_address=request.META['REMOTE_ADDR'],merchant = decMerchant,clientCode = clientModel.client_code)
        print(authKey+" "+authIV)
        encResponse = auth.AESCipher(authKey, authIV).encrypt(response)
        Log_model_services.Log_Model_Service.update_response(
            logid, {"Message": str(encResponse), "response_code": "1"})
        return Response({"message": "data saved succefully", "data": str(encResponse), "response_code": "1"}, status=status.HTTP_200_OK)
class LoginRequestAdminAPI(APIView):
    @swagger_auto_schema(request_body=login_docs.request_admin,responses=login_docs.response_login_request)
    def post(self,req):
        request_obj = "path:: "+req.path+" :: headers::"+str(req.headers)+" :: meta_data:: "+str(req.META)+"data::"+str(req.data)
        logs = Log_model_services.Log_Model_Service(log_type="post request on "+req.path,client_ip_address=req.META['REMOTE_ADDR'],server_ip_address=const.server_ip,full_request=request_obj,remarks="get request on "+req.path+" for fetching the log records")
        logid=logs.save()
        try:
            print(req.data)
            login=login_service.Login_service(username=req.data["username"],password=req.data["password"],client_ip_address=req.META['REMOTE_ADDR'])
            res = login.login_request_admin()
            if(res==False):
                Log_model_services.Log_Model_Service.update_response(logid,{"message":"User Not Found","response_code":"0"})
                return Response({"message":"User Not Found","response_code":"0"},status=status.HTTP_400_BAD_REQUEST)
            else:
                Log_model_services.Log_Model_Service.update_response(logid,{"message":"OTP sent","verification_token":res,"response_code":"1"})
                return Response({"message":"OTP sent ","verification_token":res,"response_code":"1"},status=status.HTTP_200_OK)
        except Exception as e:
            Log_model_services.Log_Model_Service.update_response(logid,{"message":"Some error occured","Error_Code":e.args,"response_code":"2"})
            return Response({"message":"Some error occured","Error_Code":e.args,"response_code":"2"},status=status.HTTP_409_CONFLICT)

class LoginRequestAPI(APIView):
    @swagger_auto_schema(request_body=login_docs.request,responses=login_docs.response_login_request)
    def post(self,req):
        request_obj = "path:: "+req.path+" :: headers::"+str(req.headers)+" :: meta_data:: "+str(req.META)+"data::"+str(req.data)
        logs = Log_model_services.Log_Model_Service(log_type="post request on "+req.path,client_ip_address=req.META['REMOTE_ADDR'],server_ip_address=const.server_ip,full_request=request_obj,remarks="get request on "+req.path+" for fetching the log records")
        logid=logs.save()
        try:
            print(req.data)
            login=login_service.Login_service(username=req.data["username"],password=req.data["password"],client_ip_address=req.META['REMOTE_ADDR'])
            res = login.login_request()
            if(res==False):
                Log_model_services.Log_Model_Service.update_response(logid,{"message":"User Not Found","response_code":"0"})
                return Response({"message":"User Not Found","response_code":"0"},status=status.HTTP_400_BAD_REQUEST)
            else:
                Log_model_services.Log_Model_Service.update_response(logid,{"message":"OTP sent","verification_token":res,"response_code":"1"})
                return Response({"message":"OTP sent ","verification_token":res,"response_code":"1"},status=status.HTTP_200_OK)
        except Exception as e:
            Log_model_services.Log_Model_Service.update_response(logid,{"message":"Some error occured","Error_Code":e.args,"response_code":"2"})
            return Response({"message":"Some error occured","Error_Code":e.args,"response_code":"2"},status=status.HTTP_409_CONFLICT)

class LoginVerificationAPI(APIView):
    @swagger_auto_schema(request_body=login_docs.verification,responses=login_docs.response_login_verification)
    def post(self,req):
        request_obj = "path:: "+req.path+" :: headers::"+str(req.headers)+" :: meta_data:: "+str(req.META)+"data::"+str(req.data)
        logs = Log_model_services.Log_Model_Service(log_type="post request on "+req.path,client_ip_address=req.META['REMOTE_ADDR'],server_ip_address=const.server_ip,full_request=request_obj,remarks="get request on "+req.path+" for fetching the log records")
        logid=logs.save()
        try:
            login=login_service.Login_service.login_verification(req.data['verification_code'],req.data["otp"],req.META['REMOTE_ADDR'],req.data['geo_location'],req.data["type"])
            if(login=="OTP Expired"):
                Log_model_services.Log_Model_Service.update_response(logid,{"message":"OTP Expired","response_code":"0"})
                return Response({"message":"OTP Expired","response_code":"0"},status=status.HTTP_400_BAD_REQUEST)
            elif login==False:
                Log_model_services.Log_Model_Service.update_response(logid,{"message":"OTP or Verification token is not valid","response_code":"0"})
                return Response({"message":"OTP or Verification token is not valid","response_code":"0"},status=status.HTTP_400_BAD_REQUEST)
            else:
                # print(str(login[0]))
                api_key=auth.AESCipher(const.AuthKey,const.AuthIV).encrypt(str(login["user_id"]))
                Log_model_services.Log_Model_Service.update_response(logid,{"auth_token":str(api_key)[2:].replace("'",""),"response_code":"1"})
                return Response({"auth_token":str(api_key)[2:].replace("'",""),"jwt_token":login["jwt_token"],"user_token":login['user_token'],"response_code":"1"},status=status.HTTP_200_OK)
        except Exception as e:
            import traceback
            print(traceback.format_exc())
            Log_model_services.Log_Model_Service.update_response(logid,{"Error_Code":e.args,"response_code":"2"})
            return Response({"Error_Code":e.args,"response_code":"2"},status=status.HTTP_400_BAD_REQUEST)
class ResendLoginOTP(APIView):
    @swagger_auto_schema(request_body=login_docs.resend_otp_request,responses=login_docs.response_login_request)
    def post(self,req):
        request_obj = "path:: "+req.path+" :: headers::"+str(req.headers)+" :: meta_data:: "+str(req.META)+"data::"+str(req.data)
        logs = Log_model_services.Log_Model_Service(log_type="post request on "+req.path,client_ip_address=req.META['REMOTE_ADDR'],server_ip_address=const.server_ip,full_request=request_obj,remarks="get request on "+req.path+" for fetching the log records")
        logid=logs.save()
        try:
         login=login_service.Login_service.resend_otp(req.data["verification_code"],req.META['REMOTE_ADDR'],req.data["type"])
        #  api_key=auth.AESCipher(const.AuthKey,const.AuthIV).encrypt(login)
         Log_model_services.Log_Model_Service.update_response(logid,{"verification_token":login,"response_code":"1"})
         return Response({"verification_token":login,"response_code":"1"},status=status.HTTP_200_OK)
        except Exception as e:
            import traceback
            print(traceback.format_exc())
            Log_model_services.Log_Model_Service.update_response(logid,{"Error":e.args,"response_code":'2'})
            return Response({"Error":e.args,"response_code":'2'},status=status.HTTP_400_BAD_REQUEST)
        
class fetchBeneficiary(APIView):
    @swagger_auto_schema(request_body=addBeneficiary_docs.fetch_request,responses=addBeneficiary_docs.fetch_response)
    def post(self,request):
        auth_token = request.headers["auth_token"]
        merchantId = auth.AESCipher(const.AuthKey,const.AuthIV).decrypt(auth_token)
        clientModel = Client_model_service.Client_Model_Service.fetch_by_id(
            id=merchantId, created_by="merchantid :: "+merchantId, client_ip_address=request.META['REMOTE_ADDR'])
        authKey = clientModel.auth_key
        authIV = clientModel.auth_iv
        query = request.data.get("query")
        role = RoleModel.objects.get(id=clientModel.role)
        decResp = str(request.data.get("query"))
        account_number=None
        ifsc_code=None
        merchant_id=None
        #"query":"CARw8RxXinePTv1Chqa/r5EFTapOpkhtv1MrYXrgalG/X2UIFH8XCek14Bn7uv/Wkq/uf3VlWgLoA4F1oY6RXv7A6qFYNQzdac5nS8oylt0="
        role = RoleModel.objects.get(id=clientModel.role)
        if role.role_name=="test" :
            account_number = request.data.get("account_number")
            ifsc_code = request.data.get("ifsc_code")
            merchant_id = request.data.get("merchant_id")
            service = Beneficiary_Model_Services(account_number=account_number,ifsc_code=ifsc_code,merchant_id=merchant_id)
            response= list(service.fetchBeneficiaryByParams())
            return Response({"data":str(response),"responseCode":"1"})
        decQuery = auth.AESCipher(authKey,authIV).decrypt(query).split("'")
        print(".......... ",decQuery)
        if(decQuery[1] == "account_number"):
            account_number = decQuery[3]
        if(decQuery[5]=="ifsc_code"):
            ifsc_code=decQuery[7]
        if(decQuery[9]=="merchant_id"):
            merchant_id=decQuery[11]
        service = Beneficiary_Model_Services(account_number=account_number,ifsc_code=ifsc_code,merchant_id=merchant_id)
        response= list(service.fetchBeneficiaryByParams())
        encResponse = auth.AESCipher(authKey,authIV).encrypt(str(response))
        return Response({"data":str(encResponse),"responseCode":"1"})

class updateBeneficiary(APIView):
    def put(self,request):
        id = request.data.get("id")
        bene = BeneficiaryModel.objects.filter(id=id)
        if(len(bene)==0):
            return Response({"msg":"not found","response_code":'0'},status=status.HTTP_404_NOT_FOUND)
        full_name = request.data.get("full_name")
        account_number = request.data.get("account_number")
        ifsc_code = request.data.get("ifsc_code")
        merchant_id = request.data.get("merchant_id")
        updated_by = request.data.get("updated_by")
        created_at = bene[0].created_at
        updated_at = datetime.now()
        service = Beneficiary_Model_Services(full_name=full_name,account_number=account_number,ifsc_code=ifsc_code,merchant_id=merchant_id)
        service.update(id=id,updated_at=updated_at,updated_by=updated_by,created_at=created_at)
        return Response({"msg":"done","response_code":'1'},status=status.HTTP_200_OK)

class deleteBeneficiary(APIView):
    def delete(self,request):
        id = request.data.get("id")
        bene = BeneficiaryModel.objects.filter(id=id)
        if(len(bene)==0):
            return Response({"msg":"not found","response_code":'0'},status=status.HTTP_404_NOT_FOUND)
        
        BeneficiaryModel.objects.filter(id=id).delete()
        return Response({"msg":"done","response_code":'1'},status=status.HTTP_200_OK)

class addSingleBeneficiary(APIView):
    @swagger_auto_schema(request_body=addBeneficiary_docs.single_bene,responses=addBeneficiary_docs.single_bene_response)
    def post(self, request):
        auth_token = request.headers.get("auth_token")
        merchantId = auth.AESCipher(const.AuthKey,const.AuthIV).decrypt(auth_token)
        clientModel = Client_model_service.Client_Model_Service.fetch_by_id(
            id=merchantId, created_by="merchantid :: "+merchantId, client_ip_address=request.META['REMOTE_ADDR'])
        authKey = clientModel.auth_key
        authIV = clientModel.auth_iv
        role = RoleModel.objects.get(id=clientModel.role)
        decResp = str(request.data.get("query"))
        if role.role_name!="test" :
            decResp = auth.AESCipher(authKey, authIV).decrypt(decResp)
        res = ast.literal_eval(decResp)
        print(res.get("full_name"))
        service = Beneficiary_Model_Services(full_name=res.get("full_name"),account_number=res.get("account_number"),ifsc_code=res.get("ifsc_code"),merchant_id=res.get("merchant_id"))
        service.save()
        return Response({"msg":"data saved to database","response_code":'1'},status=status.HTTP_200_OK)
        
class saveBeneficiary(APIView):
    @swagger_auto_schema(request_body=addBeneficiary_docs.request,responses=addBeneficiary_docs.response_schema_dict)
    def post(self, request, format=None):
        api_key = str(request.headers['auth_token'])
        merchantId =auth.AESCipher(const.AuthKey,const.AuthIV).decrypt(api_key)
        try:
            excel_file = request.FILES["files"]
        except MultiValueDictKeyError:
            return Response({"msg":"not done","response_code":'0'},status=status.HTTP_400_BAD_REQUEST)
        try:
            if (str(excel_file).split(".")[-1] == "xls"):
                data = xls_get(excel_file, column_limit=4)
            elif (str(excel_file).split(".")[-1] == "xlsx"):
                data = xlsx_get(excel_file, column_limit=4)
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
                    resultSet = BeneficiaryModel.objects.filter(merchant_id=int(merchantId),account_number=account_number,ifsc_code=ifsc_code)
                    if(len(resultSet)==0 and merchant_id==int(merchantId)):
                        service = Beneficiary_Model_Services(full_name=full_name,account_number=account_number,ifsc_code=ifsc_code,merchant_id=merchant_id)
                        service.save()
            return Response({"msg":"data parsed and saved to database","response_code":'1'},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"Message":"some error","Error":e.args})