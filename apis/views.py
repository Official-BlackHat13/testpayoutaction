# from django.shortcuts import render
# Create your views here.
from http import client
from django.db.models import query
from requests.sessions import merge_hooks
from rest_framework.exceptions import server_error
# from apis.bank_services.IFDC_service import payment
from django.http import *
from rest_framework import generics
from django.shortcuts import *
from rest_framework.views import APIView
from rest_framework.response import *
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from .API_docs import payout_docs,auth_docs
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
from .database_service import Client_model_service,Bank_model_services

from rest_framework.parsers import JSONParser
from .database_service import Client_model_service,Bank_model_services,IpWhitelisting_model_service

from django.contrib.auth.models import User
# from .database_service import Client_model_service,Ledger_model_services
from rest_framework.permissions import IsAuthenticated
from . import const
from .Utils import randomstring

import requests
from sabpaisa import auth
from datetime import datetime
# class bankApiViewtest(APIView):
#     @swagger_auto_schema(responses=api_docs.response_schema_dict,request_body=api_docs.val)
#     def post(self,req):
#         print(req.data)
#         return Response({"test":"some"})

class Auth(APIView):
    @swagger_auto_schema(request_body=auth_docs.request,responses=auth_docs.response_schema_dict)
    def post(self,req):
        request_obj = "path:: "+req.path+" :: headers::"+str(req.headers)+" :: meta_data:: "+str(req.META)+"data::"+str(req.data)
        user = req.data
        log = Log_model_services.Log_Model_Service(log_type="Post request at "+req.path+" slug",client_ip_address=req.META['REMOTE_ADDR'],server_ip_address=const.server_ip,full_request=request_obj)
        logid=log.save()
        try:
            if(len(Client_model_service.Client_Model_Service.fetch_all_by_clientcode(user["client_code"],client_ip_address=req.META['REMOTE_ADDR'],created_by="client added"))>0):
                raise Exception("Client Code Already Present")
            user_client =User.objects.create_user(user["username"], user["email"],user["password"])
            bank=Bank_model_services.Bank_model_services.fetch_by_bankcode(user["bank_code"],client_ip_address=req.META['REMOTE_ADDR'],created_by="client added")
            client = Client_model_service.Client_Model_Service(user=user_client.id,client_id=user['client_id'],client_code=user["client_code"],auth_key=randomstring.randomString(),auth_iv=randomstring.randomString(),bank_id=bank.id,client_username=user["username"],client_password=user["password"])
            merchant_id=client.save(client_ip_address=req.META['REMOTE_ADDR'],created_by="client added")
            print("requesting api "+const.domain+"api/token/")
            res = requests.post(const.domain+"api/token/",json={"username":user["username"],"password":user["password"]})
            print("response from json")
            print(res.json())
            IpWhitelisting_model_service.IpWhiteListing_Model_Service.saveMultipleIp(merchant_id=merchant_id,ips=user["ip_addresses"],clientip=req.META['REMOTE_ADDR'])
            Log_model_services.Log_Model_Service.update_response(logid,{"Message":"user created","merchant_id":merchant_id,"response_code":"1","CLIENT_AUTH_KEY":client.auth_key,"CLIENT_AUTH_IV":client.auth_iv,"token":res.json()})
            return Response({"Message":"user created","response_code":"1","merchant_id":merchant_id,"CLIENT_AUTH_KEY":client.auth_key,"CLIENT_AUTH_IV":client.auth_iv,"token":res.json()},status=status.HTTP_200_OK)
        except Exception as e:
            Log_model_services.Log_Model_Service.update_response(logid,{"Message":"some error","error":e.args,"trace_back":e.with_traceback(e.__traceback__)})
            
            return Response({"Message":"some error","error":e.args},status=status.HTTP_409_CONFLICT)
class bankApiPaymentView(APIView):
    permission_classes = (IsAuthenticated, )
    @swagger_auto_schema(request_body=payout_docs.request,responses=payout_docs.response_schema_dict)
    def post(self,req):
        request_obj = "path::"+req.path+"headers::"+req.headers+"meta_data::"+str(req.META)+"data::"+req.data
        # payment_service=IFDC_service.payment.Payment()
        client_code = req.data["client_code"]
        encrypted_code=req.data["encrypted_code"]
        log = Log_model_services.Log_Model_Service(log_type="Post request at "+req.path+" slug",client_ip_address=req.META['REMOTE_ADDR'],server_ip_address=const.server_ip,full_request=request_obj)
        logid=log.save()
        client = Client_model_service.Client_Model_Service.fetch_by_clientcode(client_code=client_code)
        bank = Bank_model_services.Bank_model_services.fetch_by_id(client.bank)
        payout=payout_service.PayoutService(client_code=client_code,encrypted_code=encrypted_code,client_ip_address=req.META['REMOTE_ADDR'])
        if(bank.bank_name=="ICICI"):
         res = payout.excuteICICI()
        else:
            res = payout.excuteIDFC()
        if(res=="Payout Done"):
            Log_model_services.Log_Model_Service.update_response(logid,{"Message":res,"response_code":"1"})
            return Response({"Message":res,"response_code":"1"},status=status.HTTP_200_OK)
        elif (res=="Not Sufficent Balance"):
            Log_model_services.Log_Model_Service.update_response(logid,{"Message":res,"response_code":"1"})
            return Response({"Message":res,"response_code":"0"},status=status.HTTP_402_PAYMENT_REQUIRED)
        elif res==False:
            Log_model_services.Log_Model_Service.update_response(logid,{"Message":res,"response_code":"1"})
            return Response({"Message":"credential not matched","response_code":"3"},status=status.HTTP_401_UNAUTHORIZED)
        else:
            Log_model_services.Log_Model_Service.update_response(logid,{"Message":res,"response_code":"1"})
            return Response({"Message":res,"response_code":"2"},status=status.HTTP_204_NO_CONTENT)
            
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
        

class getLedgers(APIView):
    permission_classes = (IsAuthenticated, )
    def get(self,request):
        clientCode = request.data.get("client_code")
        createdBy = request.data.get("createdBy")
        ip = request.data.get("ip_address")
        resp = ICICI_service.fetchAll(clientCode,createdBy,ip)
        if(resp == "0"):
            return Response({"message": "nothing to show", "data":None,"response_code": "0"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"message": "data found","data":resp, "response_code": "1"}, status=status.HTTP_200_OK)


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
                deletedBy=res.get("deletedBy"),
                updated_at=datetime.now()
            )
            Log_model_services.Log_Model_Service.update_response(
                logid, {"Message": "updated successfully", "response_code": "1"})
            res = service.update(id=id, merchant=merchant,
                                 client_ip_address=request.META['REMOTE_ADDR'], createdBy=createdBy)
            return JsonResponse({"Message": "updated successfully", "response_code": "1"}, status=status.HTTP_200_OK)
        Log_model_services.Log_Model_Service.update_response(
            logid, {"Message": "something went wrong!!!!", "response_code": "0"})
        return JsonResponse({"Message": "something went wrong!!!!", "response_code": "0"}, status=status.HTTP_400_BAD_REQUEST)

class encryptJSON(APIView):
    def post(self, request):
        id = request.data.get("id")
        query      = request.data.get("query")
        createdBy = request.data.get("createdBy")
        ip = request.data.get("ip")
        print(query)
        print(str(query))
        print(type(str(query)))
        # return Response({"message": "credential not matched", "data": None, "response_code": "3"}, status=status.HTTP_404_NOT_FOUND)
        clientModel = Client_model_service.Client_Model_Service.fetch_by_id(
            client_ip_address=ip, id = id, created_by=createdBy)
        
        authKey = clientModel.auth_key
        authIV = clientModel.auth_iv
        encResp = auth.AESCipher(authKey, authIV).encrypt(str(query))
        print(encResp)
        return Response({"message": "data", "data": encResp, "response_code": "3"}, status=status.HTTP_200_OK)

class decryptJson(APIView):
    def post(self,request):
        id = request.data.get("id")
        query = request.data.get("query")
        createdBy = request.data.get("createdBy")
        ip = request.data.get("ip")
        clientModel = Client_model_service.Client_Model_Service.fetch_by_id(
            client_ip_address=ip, id=id, created_by=createdBy)

        authKey = clientModel.auth_key
        authIV = clientModel.auth_iv
        encResp = auth.AESCipher(authKey, authIV).decrypt(query)
        res = ast.literal_eval(encResp)
        print("...... ",res)
        return Response({"message": "data", "data":str(encResp),"response_code": "3"}, status=status.HTTP_404_NOT_FOUND)

class GetLogs(APIView):
    def get(self,req,page,length):
        authKey = const.AuthKey
        authIV = const.AuthIV
        resp = req.headers["merchant"]
        merchant = auth.AESCipher(authKey,authIV).decrypt(resp)
        clientModel = Client_model_service.Client_Model_Service.fetch_by_id(
            id=merchant, created_by=str(merchant), client_ip_address=req.META['REMOTE_ADDR'])
        authKey = clientModel.auth_key
        authIV = clientModel.auth_iv
        request_obj = "path:: "+req.path+" :: headers::"+str(req.headers)+" :: meta_data:: "+str(req.META)+"data::"+str(req.data)
        logs = Log_model_services.Log_Model_Service(log_type="get request on "+req.path,client_ip_address=req.META['REMOTE_ADDR'],server_ip_address=const.server_ip,full_request=request_obj,remarks="get request on "+req.path+" for fetching the log records")
        logid=logs.save()
        try:
            if page=="all" and length != "all":
                return JsonResponse({"Message":"page and length format does not match"},status=status.HTTP_406_NOT_ACCEPTABLE)
            logs = Log_model_services.Log_Model_Service.fetch_all_logs_in_parts(length)
            #auth.AESCipher(authKey, authIV).encrypt(logsser.data)
            print(logs)
            if page == "all":
                logsser=LogsSerializer(logs,many=True)
                return Response({"data_length": len(logs), "data": auth.AESCipher(authKey, authIV).encrypt(str(logsser.data))})
            page=int(page)
            if page>logs[1]:
             page=logs[1]-1
            logsser=LogsSerializer(logs[0][page],many=True)
            print(logs[0][page])
            Log_model_services.Log_Model_Service.update_response(logid, str({"data_length": len(
                logs[0][page]), "data": logsser.data}))
            return Response({"data_length": len(logs[0][page]), "data": auth.AESCipher(authKey, authIV).encrypt(str(logsser.data))})
        except Exception as e:
            Log_model_services.Log_Model_Service.update_response(logid, str({"data_length": len(
                logs[0][page]), "data": logsser.data}))
            return Response({"Message":"some error","Error":e.args})
        
class fetch(APIView):
    #permission_classes = (IsAuthenticated, )
    def get(self,request,page,length):
        request_obj = "path:: "+request.path+" :: headers::" + \
            str(request.headers)+" :: meta_data:: " + \
            str(request.META)+"data::"+str(request.data)
        log = Log_model_services.Log_Model_Service(log_type="Get request at "+request.path+" slug", table_name="apis_ledgermodel",
                                                   client_ip_address=request.META['REMOTE_ADDR'], server_ip_address=const.server_ip, full_request=request_obj)
        logid = log.save()
        print(page," ",length)
        authKey = const.AuthKey
        authIV = const.AuthIV
        resp = request.headers["merchant"]
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
        clientCode = request.data.get("clientCode")
        merchant = decMerchant
        customer_ref_no = request.data.get("customer_ref_no")
        startTime = request.data.get("startTime")
        endTime = request.data.get("endTime")
        trans_type = request.data.get("trans_type")
        created_by = request.data.get("created_by")
        resp = ICICI_service.fetchLedgerByParams(client_code = clientCode,
        startTime=startTime,endTime=endTime,page=page,length=length,
        merchant = merchant,customer_ref_no=customer_ref_no,trans_type=trans_type,created_by=created_by,client_ip_address=request.META['REMOTE_ADDR'])
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
        Log_model_services.Log_Model_Service.update_response(
            logid, {"Message": str(resp), "response_code": "1"})
        return Response({"message": "data found", "data": str(resp), "response_code": "1"}, status=status.HTTP_200_OK)

class encHeader(APIView):
    def get(self,request):
        authKey = const.AuthKey
        authIV = const.AuthIV
        resp = request.data.get("header")
        encResp = auth.AESCipher(authKey, authIV).encrypt(resp)
        return Response({"header": encResp, "authkey": authKey, "authIV": authIV})

class tester(APIView):
    def get(self,request):
        authKey = const.AuthKey
        authIV = const.AuthIV
        resp = request.headers["merchant"]
        if(resp == ""):
            print("yo..............")
        decMerchant = auth.AESCipher(authKey, authIV).decrypt(resp)
        return Response({"header": decMerchant, "authkey": authKey, "authIV": authIV})


class addMode(APIView):
    def post(self,request):
        m = ModeModel()
        m.mode = "credit"
        m.created_at = datetime.now()
        m.save()

class addBalanceApi(APIView):
    def post(self,request):
        request_obj = "path:: "+request.path+" :: headers::" + \
            str(request.headers)+" :: meta_data:: " + \
            str(request.META)+"data::"+str(request.data)
        log = Log_model_services.Log_Model_Service(log_type="Post request at "+request.path+" slug",
                                                    client_ip_address=request.META['REMOTE_ADDR'], server_ip_address=const.server_ip, full_request=request_obj)
        logid=log.save()

        authKey = const.AuthKey
        authIV = const.AuthIV
        merchant = request.headers["merchant"]
        if(merchant == ""):
            Log_model_services.Log_Model_Service.update_response(
                logid, {"Message": "merchant code missing", "response_code": "3"})
            return Response({"message": "merchant code missing", "data": None, "response_code": "3"}, status=status.HTTP_400_BAD_REQUEST)
        decMerchant = auth.AESCipher(authKey, authIV).decrypt(merchant)
        created_by = request.data.get("created_by")
        query = request.data.get("query")
        clientModel = Client_model_service.Client_Model_Service.fetch_by_id(
            id=decMerchant, created_by=created_by, client_ip_address=request.META['REMOTE_ADDR'])
        authKey = clientModel.auth_key
        authIV = clientModel.auth_iv
        decResp = auth.AESCipher(authKey, authIV).decrypt(query)
        res = ast.literal_eval(decResp)
        response = Ledger_Model_Service.addBal(res,client_ip_address=request.META['REMOTE_ADDR'])
        encResponse = auth.AESCipher(authKey, authIV).encrypt(response)
        Log_model_services.Log_Model_Service.update_response(
            logid, {"Message": str(encResponse), "response_code": "1"})
        return Response({"message": "data saved succefully", "data": str(encResponse), "response_code": "1"}, status=status.HTTP_200_OK)
