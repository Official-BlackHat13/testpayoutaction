# from django.shortcuts import render
# Create your views here.
from http import client
from rest_framework.exceptions import server_error
from apis.bank_services.IFDC_service import payment
from django.http import *
from rest_framework import generics
from django.shortcuts import *
from rest_framework.views import APIView
from rest_framework.response import *
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from .API_docs import payout_docs
from datetime import datetime
#from .serializers import *
# from .models import *

from .bank_services import IFDC_service
from .database_models import LedgerModel
from apis.database_service.Ledger_model_services import *
from apis.serializersFolder.serializers import LedgerSerializer, CreateLedgerSerializer
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
# class bankApiViewtest(APIView):
#     @swagger_auto_schema(responses=api_docs.response_schema_dict,request_body=api_docs.val)
#     def post(self,req):
#         print(req.data)
#         return Response({"test":"some"})


class bankApiPaymentView(APIView):
    @swagger_auto_schema(request_body=payout_docs.request)
    def post(self,req):
        payment_service=IFDC_service.payment.Payment()
        return Response(payment_service.hit())
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
            return Response({"message": "success","id":res}, status=status.HTTP_201_CREATED)
        return Response({"message": "something went wrong"}, status = status.HTTP_400_BAD_REQUEST)


class getLedger(APIView):
    def get(self,request):
        queryset = fetchAllLedgersService.fetchAll().values()
        print("..........",queryset)
        return JsonResponse({"data": list(queryset)},status=status.HTTP_201_CREATED)


class DeleteLedger(APIView):
    def delete(self,request):
        id = request.data.get("id")
        deletedBy = request.data.get("deletedBy")
        print("id===== ",id)
        resp = deleteById(id,deletedBy)
        if(resp == True):
            return JsonResponse({"Message": "delete successfully"}, status=status.HTTP_200_OK)
        else:
            return JsonResponse({"Message": "Id not found"}, status=status.HTTP_404_NOT_FOUND)

class UpdateLedger(APIView):
    def put(self,request):
        id = request.data.get("id")
        ledger = LedgerModel.objects.filter(id=id)
        print("update function")
        if(len(ledger) > 0 and ledger[0].client_code == request.data.get("client_code")):
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


class findByClientCode(APIView):
    def get(self,request):
        queryset=findByClientCodeService(request.data.get("clientCode"))
        if(len(queryset)>0):
            return Response({"data": queryset.values()}, status=status.HTTP_200_OK)
        return Response({"Message": "No records found for the given client code"}, status=status.HTTP_404_NOT_FOUND)

class findByClientId(APIView):
    def get(self,request):
        queryset = findByClientIdService(request.data.get("clientId"))
        if(len(queryset) > 0):
            return Response({"data": queryset.values()}, status=status.HTTP_200_OK)
        return Response({"Message": "No records found for the given client ID"}, status=status.HTTP_404_NOT_FOUND)

class findByTransTime(APIView):
    def get(self, request):
        queryset = findByTransTimeService(request.data.get("startTransTime"), request.data.get("endTransTime"))
        if(len(queryset) > 0):
            return Response({"data": queryset.values()}, status=status.HTTP_200_OK)
        return Response({"Message": "No records found for the given time range"}, status=status.HTTP_404_NOT_FOUND)