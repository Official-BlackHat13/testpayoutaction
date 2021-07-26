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
# from rest_framework.parsers import JSONParser
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
class bankApiPaymentView(APIView):
    # permission_classes = (IsAuthenticated, )
    @swagger_auto_schema(request_body=payout_docs.request,responses=payout_docs.response_schema_dict)
    def post(self,req):
        try:
            request_obj = "path::"+req.path+"headers::"+str(req.headers)+"meta_data::"+str(req.META)+"data::"+str(req.data)
            # payment_service=IFDC_service.payment.Payment()
            api_key = req.headers['auth_token']
            merchant_id=auth.AESCipher(const.AuthKey,const.AuthIV).decrypt(api_key)
            encrypted_code=req.data["encrypted_code"]
            
            log = Log_model_services.Log_Model_Service(log_type="Post request at "+req.path+" slug",client_ip_address=req.META['REMOTE_ADDR'],server_ip_address=const.server_ip,full_request=request_obj)
            logid=log.save()
            client = Client_model_service.Client_Model_Service.fetch_by_id(merchant_id,req.META['REMOTE_ADDR'],"merchant id :: "+merchant_id)
            print("client bank::"+str(client.bank_id))
            bank = Bank_model_services.Bank_model_services.fetch_by_id(client.bank_id,req.META['REMOTE_ADDR'],"merchant id :: "+merchant_id)
            # print("bank::"+str(bank))
            payout=payout_service.PayoutService(merchant_id=merchant_id,encrypted_code=encrypted_code,client_ip_address=req.META['REMOTE_ADDR'])
            if(bank.bank_name=="ICICI"):
             res = payout.excuteICICI()
            elif bank.bank_name=="PAYTM":
                res = payout.excutePAYTM()
            else:
                res = payout.excuteIDFC()
            
            if(res[0]=="Payout Done"):
                # merchant=MerchantModel.objects.get(id=merchant_id)
                # role = RoleModel.objects.get(id=merchant.role)
                enc_str=res[1]
                if client.is_encrypt:
                 enc_str=str(auth.AESCipher(client.auth_key,client.auth_iv).encrypt(str(res[1])))[2:].replace("'","")
                
                Log_model_services.Log_Model_Service.update_response(logid,{"Message":res,"response_code":"1"})
                return Response({"Message":"Payout Done",'resData':enc_str,"response_code":"1"},status=status.HTTP_200_OK)
            elif not res[2]:
                Log_model_services.Log_Model_Service.update_response(logid,{"Message":res,"response_code":"0"})
                return Response({"Message":res[0],"response_code":"0"},status=status.HTTP_400_BAD_REQUEST)
            elif res[0]==False:
                Log_model_services.Log_Model_Service.update_response(logid,{"Message":"credential not matched","response_code":"3"})
                return Response({"Message":"credential not matched","response_code":"3"},status=status.HTTP_401_UNAUTHORIZED)
            else:
                Log_model_services.Log_Model_Service.update_response(logid,{"Message":res,"response_code":"2"})
                return Response({"Message":res,"response_code":"2"},status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
         import traceback
         print(traceback.format_exc())
         Log_model_services.Log_Model_Service.update_response(logid,{"Message":e.args,"response_code":"2"})
         return Response({"Message":"Some Technical error","response_code":"2"},status=status.HTTP_204_NO_CONTENT)



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
            # merchant=MerchantModel.objects.get(id=merchant_id)
            # role = RoleModel.objects.get(id=merchant.role)
            if clientModel.is_encrypt :
             encResp = auth.AESCipher(authKey, authIV).decrypt(data)
            customer_ref = encResp.split(":")[1].replace('"','')
            recs =enquiry_service.get_enc(merchant_id,customer_ref,req.META['REMOTE_ADDR'],created_by="Merchant id :: "+str(merchant_id))
            response = []
            if recs!=None:
                for rec in recs:
                    
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
                            'payment_mode_id': rec.payment_mode_id
                        }
                    response.append(res)
                    
                enc = response
                # print("roleName :: "+role.role_name)
                if clientModel.is_encrypt:
                 enc = str(auth.AESCipher(authKey,authIV).encrypt(str(res)))[2:].replace("'","")
                # elif not const.test_merchants:
                #     enc = str(auth.AESCipher(authKey,authIV).encrypt(str(res)))[2:].replace("'","")
                return Response({"message": "data found","resData": enc,"responseCode": "1"})
            else:
                return Response({"message":"NOT_FOUND","response_code":"0"})
        except Exception as e:
            import traceback
            print(traceback.format_exc())
            return Response({"message":e.args})

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
        role = RoleModel.objects.get(id=clientModel.role_id)
        if clientModel.is_encrypt==False :
            print("hello")
            decResp = request.data.get("query")
            print(decResp)
            res = ast.literal_eval(str(decResp))
            response = Ledger_Model_Service.addBal(res,client_ip_address=request.META['REMOTE_ADDR'],merchant = decMerchant,clientCode = clientModel.client_code)
            return Response({"data":str(response),"responseCode":"1"})
        #end
        decResp = auth.AESCipher(authKey, authIV).decrypt(str(query))
        res = ast.literal_eval(decResp)
        response = Ledger_Model_Service.addBal(res,client_ip_address=request.META['REMOTE_ADDR'],merchant = decMerchant,clientCode = clientModel.client_code)
        print(authKey+" "+authIV)
        encResponse = auth.AESCipher(authKey, authIV).encrypt(response)
        Log_model_services.Log_Model_Service.update_response(
            logid, {"Message": str(encResponse), "response_code": "1"})
        return Response({"message": "data saved succefully", "data": str(encResponse), "response_code": "1"}, status=status.HTTP_200_OK)
