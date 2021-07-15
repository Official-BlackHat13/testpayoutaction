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