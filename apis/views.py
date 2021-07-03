# from django.shortcuts import render
# Create your views here.
from apis.database_models.Test import TestModel
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

from .other_service import payout_service
from .database_models import LedgerModel
from apis.database_service.Ledger_model_services import *
from apis.serializersFolder.serializers import LedgerSerializer, CreateLedgerSerializer
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from .database_service import Client_model_service,Bank_model_services,IpWhitelisting_model_service
from django.contrib.auth.models import User
# from .database_service import Client_model_service,Ledger_model_services
from rest_framework.permissions import IsAuthenticated
from . import const
from .Utils import randomstring
from .other_service import login_service
from . import const
from sabpaisa import auth
import requests
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
            client = Client_model_service.Client_Model_Service(role_id=user['role_id'],user=user_client.id,client_id=user['client_id'],client_code=user["client_code"],auth_key=randomstring.randomString(),auth_iv=randomstring.randomString(),bank_id=bank.id,client_username=user["username"],client_password=user["password"])
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
class addBalanceApi(APIView):
    pass
class bankApiEnquiryView(APIView):
    @swagger_auto_schema()
    def post(self,req):
        pass


# class AllLedgers(generics.ListAPIView):
#     queryset = fetchAllLedgersService.fetchAll()
#     serializer_class = LedgerSerializer
#     # serializer_class = serializers.LedgerSerializer

class LedgerSaveRequest(APIView):
    def post(self,request):
        print(request.data.get("client"))
        service = Ledger_Model_Service(
                                       client_id=request.data.get("client"),
                                       client_code=request.data.get("client_code"),
                                       type_status=request.data.get("type_status"),
                                       amount=request.data.get("amount"),
            van= request.data.get("van"),
                                       trans_type=request.data.get("trans_type"),
                                       trans_status=request.data.get("trans_status"),
            bank_ref_no= request.data.get("bank_ref_no"),
            customer_ref_no= request.data.get("customer_ref_no"),
                                       bank_id=request.data.get("bank"),
            trans_time=datetime.now(),
            bene_account_name=request.data.get("bene_account_name"),
                                       bene_account_number=request.data.get("bene_account_number"),
                                       bene_ifsc=request.data.get("bene_ifsc"),
                                       request_header=request.data.get("request_header"),
                                      mode =  request.data.get("mode"),
                                       charge = request.data.get("charge"),
            createdBy=request.data.get("createdBy"),
            updatedBy=request.data.get("updatedBy"),
            deletedBy=request.data.get("deletedBy"),
            created_at=datetime.now()
                                       )
        res = service.save()
        if(res>0):
            return Response({"Message": "success","id":res}, status=status.HTTP_201_CREATED)
        return Response({"Message": "something went wrong"}, status = status.HTTP_400_BAD_REQUEST)


class getLedger(APIView):
    def get(self,request):
        queryset = fetchAllLedgersService.fetchAll().values()
        print("..........",queryset)
        return JsonResponse({"data": list(queryset)},status=status.HTTP_201_CREATED)


class DeleteLedger(APIView):
    def delete(self,request):
        id = request.GET.get("id")
        deletedBy = request.GET.get("deletedBy")
        print("id===== ",id)
        resp = deleteById(id,deletedBy)
        if(resp == True):
            return JsonResponse({"Message": "delete successfully"}, status=status.HTTP_200_OK)
        else:
            return JsonResponse({"Message": "Id not found"}, status=status.HTTP_404_NOT_FOUND)
# class Test(APIView):
#     def get(self,req):
#         val=Ledger_model_services.Ledger_Model_Service.getBalance("FDC12")
#         print(val)
#         return Response({"Message":val})
class UpdateLedger(APIView):
    def put(self,request):
        id = request.data.get("id")
        ledger = LedgerModel.objects.filter(id=id)
        print("update function")
        if(len(ledger) > 0):
            ledgermodel = LedgerModel()
            ledgerModel = ledger[0]
            print("....... ", ledgermodel.created_at)
            print("....... ", ledgermodel.deleted_at)
            service = Ledger_update_Model_Service(
                id=request.data.get("id"),
                client_id=request.data.get("client"),
                client_code=request.data.get("client_code"),
                type_status=request.data.get("type_status"),
                amount=request.data.get("amount"),
                van=request.data.get("van"),
                trans_type=request.data.get("trans_type"),
                trans_status=request.data.get("trans_status"),
                bank_ref_no=request.data.get("bank_ref_no"),
                customer_ref_no=request.data.get("customer_ref_no"),
                bank_id=request.data.get("bank"),
                trans_time=ledgerModel.trans_time,
                bene_account_name=request.data.get("bene_account_name"),
                bene_account_number=request.data.get("bene_account_number"),
                bene_ifsc=request.data.get("bene_ifsc"),
                request_header=request.data.get("request_header"),
                mode=request.data.get("mode"),
                charge=request.data.get("charge"),
                createdBy=request.data.get("createdBy"),
                updatedBy=request.data.get("updatedBy"),
                deletedBy=request.data.get("deletedBy"),
                # created_at = ledgerModel.created_at,
                # deleted_at = ledgermodel.deleted_at,
                updated_at=datetime.now()
            )
            res = service.save()
            return JsonResponse({"Message": "updated successfully"}, status=status.HTTP_200_OK)
        return JsonResponse({"Message": "something went wrong!!!!"}, status=status.HTTP_400_BAD_REQUEST)


class GetLogs(APIView):
    def get(self,req,page,length):
        request_obj = "path:: "+req.path+" :: headers::"+str(req.headers)+" :: meta_data:: "+str(req.META)+"data::"+str(req.data)
        logs = Log_model_services.Log_Model_Service(log_type="get request on "+req.path,client_ip_address=req.META['REMOTE_ADDR'],server_ip_address=const.server_ip,full_request=request_obj,remarks="get request on "+req.path+" for fetching the log records")
        logid=logs.save()
        try:
            if page=="all" and length != "all":
                return JsonResponse({"Message":"page and length format does not match"},status=status.HTTP_406_NOT_ACCEPTABLE)
            logs = Log_model_services.Log_Model_Service.fetch_all_logs_in_parts(length)
            print(logs)
            if page == "all":
                logsser=LogsSerializer(logs,many=True)
                return Response({"data_length":len(logs),"data":logsser.data})
            page=int(page)
            if page>logs[1]:
             page=logs[1]-1
            logsser=LogsSerializer(logs[0][page],many=True)
            print(logs[0][page])
            Log_model_services.Log_Model_Service.update_response(logid,str({"data_length":len(logs[0][page]),"data":logsser.data}))
            return Response({"data_length":len(logs[0][page]),"data":logsser.data})
        except Exception as e:
            Log_model_services.Log_Model_Service.update_response(logid,str({"data_length":len(logs[0][page]),"data":logsser.data}))
            return Response({"Message":"some error","Error":e.args})


class LoginRequestAPI(APIView):
    def post(self,req):
        try:
            print(req.data)
            login=login_service.Login_service(username=req.data["username"],password=req.data["password"],client_ip_address=req.META['REMOTE_ADDR'])
            res = login.login_request()
            if(res==False):
                return Response({"message":"User Not Found"})
            else:
                return Response({"verification_token":res})
        except Exception as e:
            return Response({"Error_Code":e.args})
class LoginVerificationAPI(APIView):
    def post(self,req):
        try:
            print(req.data)
            login=login_service.Login_service.login_verification(req.data['verification_code'],req.data["otp"])
            print('done')
            if(login=="OTP Expired"):
                return Response({"message":"OTP Expired"})
            elif login==False:
                return Response({"message":"OTP or Verification token is not valid"})
            else:
                api_key=auth.AESCipher(const.AuthKey,const.AuthIV).encrypt(str(login))
                return Response({"api_key":str(api_key)[2:].replace("'","")})
        except Exception as e:
            return Response({"Error_Code":e.args})
class ResendLoginOTP(APIView):
    def post(self,req):
        try:
         login=login_service.Login_service.resend_otp(req.data["verification_code"])
         api_key=auth.AESCipher(const.AuthKey,const.AuthIV).encrypt(login)
         return Response({"api_key":api_key})
         
        except Exception as e:
            return Response({"Error":e.args})
        