# from django.shortcuts import render
# Create your views here.
from http import client
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
#from .serializers import *
# from .models import *

from .other_service import payout_service
from .database_models import LedgerModel
from apis.database_service.Ledger_model_services import *
from django.http.response import JsonResponse
from apis.other_service.enquiry_service import *
from .database_service import Client_model_service,Bank_model_services
from django.contrib.auth.models import User
from .database_service import Client_model_service,Ledger_model_services
from rest_framework.permissions import IsAuthenticated
from . import const
from .Utils import randomstring
import requests
from sabpaisa import auth

# class bankApiViewtest(APIView):
#     @swagger_auto_schema(responses=api_docs.response_schema_dict,request_body=api_docs.val)
#     def post(self,req):
#         print(req.data)
#         return Response({"test":"some"})

class Auth(APIView):
    @swagger_auto_schema(request_body=auth_docs.request,responses=auth_docs.response_schema_dict)
    def post(self,req):
        user = req.data
        try:
            if(len(Client_model_service.Client_Model_Service.fetch_all_by_clientcode(user["client_code"]))>0):
                raise Exception("Client Code Already Present")
            user_client =User.objects.create_user(user["username"], user["email"],user["password"])
            bank=Bank_model_services.Bank_model_services.fetch_by_bankcode(user["bank_code"])
            client = Client_model_service.Client_Model_Service(user=user_client.id,client_id=user['client_id'],client_code=user["client_code"],auth_key=randomstring.randomString(),auth_iv=randomstring.randomString(),bank_id=bank.id,client_username=user["username"],client_password=user["password"])
            client.save()
            
           
            res = requests.post(const.domain+"api/token/",json={"username":user["username"],"password":user["password"]})
            print(res.json())
            return Response({"message":"user created","response_code":"1","CLIENT_AUTH_KEY":client.auth_key,"CLIENT_AUTH_IV":client.auth_iv,"token":res.json()},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message":"some error","error":e.args},status=status.HTTP_409_CONFLICT)
class bankApiPaymentView(APIView):
    permission_classes = (IsAuthenticated, )
    @swagger_auto_schema(request_body=payout_docs.request,responses=payout_docs.response_schema_dict)
    def post(self,req):
        # payment_service=IFDC_service.payment.Payment()
        client_code = req.data["client_code"]
        encrypted_code=req.data["encrypted_code"]
        client = Client_model_service.Client_Model_Service.fetch_by_clientcode(client_code=client_code)
        bank = Bank_model_services.Bank_model_services.fetch_by_id(client.bank)
        payout=payout_service.PayoutService(client_code=client_code,encrypted_code=encrypted_code)
        if(bank.bank_name=="ICICI"):
         res = payout.excuteICICI()
        else:
            res = payout.excuteIDFC()
        if(res=="Payout Done"):
            return Response({"message":res,"response_code":"1"},status=status.HTTP_200_OK)
        elif (res=="Not Sufficent Balance"):
            return Response({"message":res,"response_code":"0"},status=status.HTTP_402_PAYMENT_REQUIRED)
        elif res==False:
            return Response({"message":"credential not matched","response_code":"3"},status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({"message":res,"response_code":"2"},status=status.HTTP_204_NO_CONTENT)
            
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
    permission_classes = (IsAuthenticated, )
    def post(self,request):
        print(request.data.get("client"))
        service = Ledger_Model_Service(
            trans_amount_type=request.data.get("trans_amount_type"),
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
        resp = service.save()
        if(resp == "0"):
            return Response({"message": "nothing to show", "data": None, "response_code": "0"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"message": "data found", "data": resp, "response_code": "1"}, status=status.HTTP_200_OK)



class getLedgers(APIView):
    permission_classes = (IsAuthenticated, )
    def get(self,request):
        clientCode = request.data.get("client_code")
        resp = ICICI_service.fetchAll(clientCode)
        if(resp == "0"):
            return Response({"message": "nothing to show", "data":None,"response_code": "0"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"message": "data found","data":resp, "response_code": "1"}, status=status.HTTP_200_OK)


class DeleteLedger(APIView):
    permission_classes = (IsAuthenticated, )
    def delete(self,request):
        id = request.data.get("id")
        deletedBy = request.data.get("deletedBy")
        print("id===== ",id)
        resp = Ledger_Model_Service.deleteById(id, deletedBy)

        if(resp == True):
            return JsonResponse({"Message": "delete successfully"}, status=status.HTTP_200_OK)
        else:
            return JsonResponse({"Message": "Id not found"}, status=status.HTTP_404_NOT_FOUND)
# class Test(APIView):
#     def get(self,req):
#         val=Ledger_model_services.Ledger_Model_Service.getBalance("FDC12")
#         print(val)
#         return Response({"message":val})
class UpdateLedger(APIView):
    permission_classes = (IsAuthenticated, )
    def put(self,request):
        id = request.data.get("id")
        ledger = LedgerModel.objects.filter(id=id)
        print("update function")
        if(len(ledger) > 0 and ledger[0].client_code == request.data.get("client_code")):
            ledgermodel = LedgerModel()
            ledgerModel = ledger[0]
            print("....... ", ledgermodel.created_at)
            print("....... ", ledgermodel.deleted_at)
            service = Ledger_Model_Service(
                id=request.data.get("id"),
                trans_amount_type = request.data.get("trans_amount_type"),
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
            res = service.update()
            return JsonResponse({"Message": "updated successfully"}, status=status.HTTP_200_OK)
        return JsonResponse({"Message": "something went wrong!!!!"}, status=status.HTTP_400_BAD_REQUEST)


class findByClientCode(APIView):
    permission_classes = (IsAuthenticated, )
    def get(self,request):
        resp = ICICI_service.findByClientCodeService(request.data.get("client_code"))
        if(resp != "0"):
            return Response({"message": "data found","data":resp, "response_code": "1"}, status=status.HTTP_200_OK)
        return Response({"message": "credential not matched", "data":None,"response_code": "3"}, status=status.HTTP_404_NOT_FOUND)

class findByClientId(APIView):
    permission_classes = (IsAuthenticated, )
    def get(self,request):
        resp = ICICI_service.findByClientIdService(request.data.get("client_id"), request.data.get("client_code"))
        if(resp != "0"):
            return Response({"message": "data found", "data": resp, "response_code": "1"}, status=status.HTTP_200_OK)
        return Response({"message": "credential not matched", "data": None, "response_code": "3"}, status=status.HTTP_404_NOT_FOUND)

class findByTransTime(APIView):
    permission_classes = (IsAuthenticated, )
    def get(self, request):
        resp = ICICI_service.findByTransTimeService(request.data.get(
            "startTransTime"), request.data.get("endTransTime"), request.data.get("client_code"))
        if(resp != "0"):
            return Response({"message": "data found", "data": resp, "response_code": "1"}, status=status.HTTP_200_OK)
        return Response({"message": "No data found", "data": None, "response_code": "3"}, status=status.HTTP_404_NOT_FOUND)


class findByCustomerReference(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        print("hello")
        resp = ICICI_service.findByCustomerReferenceService(
            request.data.get("customer_ref_no"), request.data.get("client_code"))
        if(resp != "0"):
            return Response({"message": "data found", "data": resp, "response_code": "1"}, status=status.HTTP_200_OK)
        return Response({"message": "credential not matched", "data": None, "response_code": "3"}, status=status.HTTP_404_NOT_FOUND)

class encryptJSON(APIView):
    def post(self, request):
        clientCode = request.data.get("client_code")
        query      = request.data.get("query")
        print(query)
        print(str(query))
        print(type(str(query)))
        # return Response({"message": "credential not matched", "data": None, "response_code": "3"}, status=status.HTTP_404_NOT_FOUND)

        clientModelService = Client_model_service.Client_Model_Service()
        clientModel = clientModelService.fetch_by_clientcode(clientCode)
        authKey = clientModel.auth_key
        authIV = clientModel.auth_iv
        encResp = auth.AESCipher(authKey, authIV).encrypt(str(query))
        print(encResp)
        return Response({"message": "credential not matched", "data": encResp, "response_code": "3"}, status=status.HTTP_404_NOT_FOUND)

# class decryptJson(APIView):
#     def post(self,request):
#         clientCode = request.data.get("client_code")
#         query = request.data.get("query")